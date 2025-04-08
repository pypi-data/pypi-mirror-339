import sys
sys.path.append("./PaddleScience/")
sys.path.append('/home/aistudio/3rd_lib')
sys.path.append("./model")
import argparse
import os
import csv
from timeit import default_timer
from typing import List
import numpy as np
import paddle
import yaml
from paddle.optimizer.lr import LRScheduler
from src.data import instantiate_datamodule
from src.networks import instantiate_network
from src.utils.average_meter import AverageMeter
from src.utils.dot_dict import DotDict
from src.utils.dot_dict import flatten_dict

class StepDecay(LRScheduler):
    def __init__(
        self, learning_rate, step_size, gamma=0.1, last_epoch=-1, verbose=False
    ):
        if not isinstance(step_size, int):
            raise TypeError(
                "The type of 'step_size' must be 'int', but received %s."
                % type(step_size)
            )
        if gamma >= 1.0:
            raise ValueError("gamma should be < 1.0.")

        self.step_size = step_size
        self.gamma = gamma
        super().__init__(learning_rate, last_epoch, verbose)

    def get_lr(self):
        i = self.last_epoch // self.step_size
        return self.base_lr * (self.gamma**i)


def instantiate_scheduler(config):
    if config.opt_scheduler == "CosineAnnealingLR":
        scheduler = paddle.optimizer.lr.CosineAnnealingDecay(
            config.lr, T_max=config.opt_scheduler_T_max
        )
    elif config.opt_scheduler == "StepLR":
        scheduler = StepDecay(
            config.lr, step_size=config.opt_step_size, gamma=config.opt_gamma
        )
    else:
        raise ValueError(f"Got {config.opt_scheduler=}")
    return scheduler


# loss function with rel/abs Lp loss
class LpLoss(object):
    def __init__(self, d=2, p=2, size_average=True, reduction=True):
        super(LpLoss, self).__init__()
        # Dimension and Lp-norm type are postive
        assert d > 0 and p > 0

        self.d = d
        self.p = p
        self.reduction = reduction
        self.size_average = size_average

    def abs(self, x, y):
        num_examples = x.size()[0]

        # Assume uniform mesh
        h = 1.0 / (x.size()[1] - 1.0)

        all_norms = (h ** (self.d / self.p)) * paddle.norm(
            x.reshape((num_examples, -1)) - y.reshape((num_examples, -1)), self.p, 1
        )

        if self.reduction:
            if self.size_average:
                return paddle.mean(all_norms)
            else:
                return paddle.sum(all_norms)

        return all_norms

    def rel(self, x, y):
        diff_norms = paddle.norm(x-y, 2)
        y_norms = paddle.norm(y, self.p)

        if self.reduction:
            if self.size_average:
                return paddle.mean(diff_norms / y_norms)
            else:
                return paddle.sum(diff_norms / y_norms)

        return diff_norms / y_norms

    def __call__(self, x, y):
        return self.rel(x, y)


def set_seed(seed: int = 0):
    paddle.seed(seed)
    np.random.seed(seed)
    import random

    random.seed(seed)


def str2intlist(s: str) -> List[int]:
    return [int(item.strip()) for item in s.split(",")]


def parse_args(yaml="UnetShapeNetCar.yaml"):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=str,
        default="configs/"+ yaml,
        help="Path to the configuration file",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        help="Device to use for training (cuda or cpu)",
    )
    parser.add_argument("--lr", type=float, default=None, help="Learning rate")
    parser.add_argument("--batch_size", type=int, default=None, help="Batch size")
    parser.add_argument("--num_epochs", type=int, default=None, help="Number of epochs")
    parser.add_argument(
        "--checkpoint",
        type=str,
        default=None,
        help="Path to the checkpoint file to resume training",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./output",
        help="Path to the output directory",
    )
    parser.add_argument(
        "--log",
        type=str,
        default="log",
        help="Path to the log directory",
    )
    parser.add_argument("--logger_types", type=str, nargs="+", default=None)
    parser.add_argument("--seed", type=int, default=0, help="Random seed for training")
    parser.add_argument("--model", type=str, default=None, help="Model name")
    parser.add_argument(
        "--sdf_spatial_resolution",
        type=str2intlist,
        default=None,
        help="SDF spatial resolution. Use comma to separate the values e.g. 32,32,32.",
    )

    args, _ = parser.parse_known_args()
    return args


def load_config(config_path):
    def include_constructor(loader, node):
        # Get the path of the current YAML file
        current_file_path = loader.name

        # Get the folder containing the current YAML file
        base_folder = os.path.dirname(current_file_path)

        # Get the included file path, relative to the current file
        included_file = os.path.join(base_folder, loader.construct_scalar(node))

        # Read and parse the included file
        with open(included_file, "r") as file:
            return yaml.load(file, Loader=yaml.Loader)

    # Register the custom constructor for !include
    yaml.Loader.add_constructor("!include", include_constructor)

    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.Loader)

    # Convert to dot dict
    config_flat = flatten_dict(config)
    config_flat = DotDict(config_flat)
    return config_flat



import re
 
def extract_numbers(s):
    return [int(digit) for digit in re.findall(r'\d+', s)]


def write_to_vtk(out_dict, point_data_pos="press on mesh points", mesh_path=None):
    import meshio
    p = out_dict["pressure"]
    index = extract_numbers(mesh_path.name)[0]
    index = str(index).zfill(3)
        
    if point_data_pos == "press on mesh points":
        mesh = meshio.read(mesh_path)
        mesh.point_data["p"] = p.numpy()
        if "pred wss_x" in out_dict:
            wss_x = out_dict["pred wss_x"]
            mesh.point_data["wss_x"] = wss_x.numpy()
    elif point_data_pos == "press on mesh cells":
        points = np.load(mesh_path.parent / f"centroid_{index}.npy")
        npoint = points.shape[0]
        mesh = meshio.Mesh(
            points=points, cells=[("vertex", np.arange(npoint).reshape(npoint, 1))]
        )
        mesh.point_data = {"p":p.numpy()}

    print(f"write : ./output/{mesh_path.parent.name}_{index}.vtk")
    mesh.write(f"./output/{mesh_path.parent.name}_{index}.vtk") 


@paddle.no_grad()
def eval(model, datamodule, config, loss_fn=None):
    model.eval()
    test_loader = datamodule.test_dataloader(
        batch_size=config.eval_batch_size, shuffle=False, num_workers=0
    )
    data_list = []
    averaged_output_dict = {}
    os.makedirs("./output/", exist_ok=True)

    for i, data_dict in enumerate(test_loader):
        out_dict = model.eval_dict(
            data_dict, loss_fn=loss_fn, decode_fn=datamodule.decode
        )

        if 'c_p truth' in out_dict:
            if i == 0:
                data_list.append(['id', 'c_d', 'c_d ref', 'c_f', 'c_f ref', 'c_p', 'c_p ref'])
            # load c_d from file
            data_path = config["data_dir"]
            index = str.zfill(str(i + 1), 3)
            c_d = paddle.load(data_path + "/test/drag_history_" + index + ".pdtensor")
            c_p = float(c_d["c_p"][-1])
            c_f = float(c_d["c_f"][-1])
            c_d = c_p + c_f
            
            # print(f"\nc_p abs error = {100 * float(paddle.abs(out_dict['c_p pred'] - out_dict['c_p truth']) / out_dict['c_p truth']):3f}%")
            # print(f"c_f abs error = {100 * float(paddle.abs(out_dict['c_f pred'] - out_dict['c_f truth']) / out_dict['c_f truth']):3f}%")
            # print(f"c_d abs error = {100 * float(paddle.abs(out_dict['c_d pred'] - out_dict['c_d truth']) / out_dict['c_d truth']):3f}%")
            data_list.append([i, c_d, float(out_dict['c_d pred']), c_f, float(out_dict['c_f pred']), c_p, float(out_dict['c_p pred'])])
        # if 'c_p pred' in out_dict:
            # print(f"c_p Pred = {out_dict['c_p pred'].item():3f}")
            # print(f"c_f Pred = {out_dict['c_f pred'].item():3f}")
            # print(f"c_d Pred = {out_dict['c_d pred'].item():3f}")

        if'l2 decoded pressure' in out_dict: #Ahmed
            # print(f"l2 error decoded pressure =  {100 * float(out_dict['l2 decoded pressure']):3f}%")
            if i == 0:
                data_list.append(['id', 'l2 p decoded'])
            data_list.append([i, float(out_dict['l2_decoded'])])
        if 'l2_decoded' in out_dict: #Shape Net Car
            # print(f"l2 error decoded pressure =  {100 * float(out_dict['l2_decoded']):3f}%")
            if i == 0:
                data_list.append(['id', 'l2 p decoded'])
            data_list.append([i, float(out_dict['l2_decoded'])])
        
        if config.write_to_vtk is True:
            print("datamodule.test_mesh_paths = ", datamodule.test_mesh_paths)
            write_to_vtk(out_dict, config.point_data_pos, datamodule.test_mesh_paths[i])
        

        with open(f"./output/{config.project_name}.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data_list)
            
    data_list = np.array(data_list)[:,1:]

    for i, k in enumerate(data_list[0]):
        averaged_output_dict[k] = data_list[1:, i].astype(np.float32).mean() #average l2
    return averaged_output_dict


def train(config):
    # Initialize the model
    model = instantiate_network(config)

    # Initialize the dataloaders
    datamodule = instantiate_datamodule(config)

    train_loader = datamodule.train_dataloader(
        batch_size=config.batch_size, shuffle=False
    )

    # Initialize the optimizer
    scheduler = instantiate_scheduler(config)
    optimizer = paddle.optimizer.Adam(
        parameters=model.parameters(), learning_rate=scheduler, weight_decay=1e-4
    )

    # Initialize the loss function
    loss_fn = LpLoss(size_average=True)
    L2 = []
    for ep in range(config.num_epochs):
        model.train()
        t1 = default_timer()
        train_l2_meter = AverageMeter()
        # train_reg = 0
        for i, data_dict in enumerate(train_loader):
            optimizer.clear_grad()
            loss_dict = model.loss_dict(data_dict, loss_fn=loss_fn)
            loss = 0
            for k, v in loss_dict.items():
                loss = loss + v.mean()
            loss.backward()
            optimizer.step()
            train_l2_meter.update(loss.item())
        print("train/lr", scheduler.get_lr(), ep)
        print("train/loss", loss.item(), ep)
        scheduler.step()
        t2 = default_timer()
        print(
            f"Training epoch {ep} took {t2 - t1:.2f} seconds. L2 loss: {train_l2_meter.avg:.4f}"
        )

        L2.append(train_l2_meter.avg)
        if ep % config.eval_interval == 0 or ep == config.num_epochs - 1:
            eval_dict = eval(model, datamodule, config, loss_fn)
            for k, v in eval_dict.items():
                print(f"Epoch: {ep} {k}: {v.item():.4f}")
        # Save the weights
        if ep % config.save_interval == 0 or ep == config.num_epochs - 1 and ep > 1:
            paddle.save(
                model.state_dict(),
                os.path.join("./output/", f"model-{config.model}-{ep}.pdparams"),
            )


if __name__ == "__main__":
    args = parse_args("UnetShapeNetCar.yaml")
    # print command line args
    config = load_config(args.config)

    # Update config with command line arguments
    for key, value in vars(args).items():
        if key != "config" and value is not None:
            config[key] = value

    # pretty print the config
    if paddle.distributed.get_rank() == 0:
        print("\n--------------- Config yaml Table----------------")
        for key, value in config.items():
            print("Key: {:<30} Val: {}".format(key, value))
        print("--------------- Config yaml Table----------------\n")

    # Set the random seed
    if config.seed is not None:
        set_seed(config.seed)
        
    # train(config)

    model = instantiate_network(config)
    checkpoint = paddle.load(f"./output/model-UNet-{config.num_epochs - 1}.pdparams")
    model.load_dict(checkpoint)

    # validation over track A
    print("\n-------Starting Evaluation over [track A]--------")
    config.n_train = 1
    t1 = default_timer()
    eval_dict = eval(
        model, instantiate_datamodule(config), config, loss_fn=LpLoss(size_average=True)
    )
    t2 = default_timer()
    print(f"Inference over [track A] took {t2 - t1:.2f} seconds.")

    # validation over track B
    print("\n-------Starting Evaluation over [track B]--------")
    config.n_train = 1
    config.data_module = "CarDataModule"
    config.test_data_dir = "/home/aistudio/data/data_test_B/"
    config.point_data_pos = "press on mesh cells"
    t1 = default_timer()
    eval_dict = eval(
        model, instantiate_datamodule(config), config, loss_fn=LpLoss(size_average=True)
    )
    t2 = default_timer()
    print(f"Inference over [track B] took {t2 - t1:.2f} seconds.")

