from typing import Any

import paddle

reductions = ["sum", "add", "mean", "min", "max"]

dtypes = [paddle.float32, paddle.float64, paddle.int32, paddle.int64]
dtypes_half = []
ind_dtypes = [paddle.int32, paddle.int64]
grad_dtypes = [paddle.float32, paddle.float64]

places = ["cpu"]
if paddle.device.is_compiled_with_cuda():
    places.append("gpu")

device = (
    paddle.CUDAPlace(0) if paddle.device.is_compiled_with_cuda() else paddle.CPUPlace()
)
if paddle.amp.is_float16_supported(device):
    dtypes_half.append(paddle.float16)
if paddle.amp.is_bfloat16_supported(device):
    dtypes_half.append(paddle.bfloat16)


def tensor(x: Any, dtype: paddle.dtype):
    return None if x is None else paddle.to_tensor(x).astype(dtype)
