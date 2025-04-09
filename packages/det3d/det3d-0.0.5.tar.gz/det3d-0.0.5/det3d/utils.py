import torch
import numpy as np

# Convert outputs to CPU
def move_to_cpu(item):
    if isinstance(item, torch.Tensor):
        return item.cpu().numpy()
    elif isinstance(item, dict):
        return {k: move_to_cpu(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [move_to_cpu(i) for i in item]
    else:
        return item
    

def load_data_to_gpu(batch_dict:dict):
    for key, val in batch_dict.items():
        if isinstance(val, np.ndarray):
            batch_dict[key] = torch.from_numpy(val).float().cuda()