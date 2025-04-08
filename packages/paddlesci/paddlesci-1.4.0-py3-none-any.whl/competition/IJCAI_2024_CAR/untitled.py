
import os
import re
 
def extract_numbers(s):
    return [digit for digit in re.findall(r'\d+', s)]

file_dir ="/home/aistudio/data/data_test_B/"
file_names = os.listdir(file_dir)

for name in file_names:
    print(name[-3:])
    if (name[-3:] == "npy") or (name[-3:] == "ply"):
        old_num = extract_numbers(name)[0]
        new_num = old_num.zfill(3)
        new_name = name.replace(old_num, new_num)
        os.rename(file_dir + name, file_dir + new_name)
        print(name)
        print(new_name)
        print(old_num)
        print(new_num)