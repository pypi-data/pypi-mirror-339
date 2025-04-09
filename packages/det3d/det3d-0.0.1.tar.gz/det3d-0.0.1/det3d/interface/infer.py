import copy
import numpy as np
import torch
from collections import defaultdict
from ..types.PointCloud import PointCloud
from ..utils import move_to_cpu, load_data_to_gpu

def mask_points_out_of_range(pc, pc_range):
    pc_range = np.array(pc_range)
    pc_range[3:6] -= 0.01  # Avoid boundary issues
    mask_x = (pc[:, 0] > pc_range[0]) & (pc[:, 0] < pc_range[3])
    mask_y = (pc[:, 1] > pc_range[1]) & (pc[:, 1] < pc_range[4])
    mask_z = (pc[:, 2] > pc_range[2]) & (pc[:, 2] < pc_range[5])
    return pc[mask_x & mask_y & mask_z]

def collate_batch(batch_list):
    data_dict = defaultdict(list)
    for sample in batch_list:
        for key, val in sample.items():
            data_dict[key].append(val)
    ret = {}
    for key, val in data_dict.items():
        if key == 'points':
            coors = []
            for i, coor in enumerate(val):
                coor_pad = np.pad(coor, ((0, 0), (1, 0)), mode='constant', constant_values=i)
                coors.append(coor_pad)
            ret[key] = np.concatenate(coors, axis=0)
    ret['batch_size'] = len(batch_list)
    return ret

def infer_pointcloud_detection(model: torch.nn.Module, pointcloud: PointCloud) -> dict:
    """
    Perform inference on general point cloud using the provided model.

    Args:
        model (torch.nn.Module): The 3D object detection model (e.g., LD_base).
        pointcloud (PointCloud): Input point cloud with shape (N, 4) [x, y, z, intensity]

    Returns:
        dict: The prediction dictionary output by the model (moved to CPU).
    """
    offset_angle = 0.0  # degrees
    offset_ground = 1.8  # meters
    point_cloud_range = [0, -44.8, -2, 224, 44.8, 4]

    points_list = copy.deepcopy(pointcloud.points)

    # Preprocess
    points_list[:, 2] += points_list[:, 0] * np.tan(offset_angle / 180. * np.pi) + offset_ground
    points_list = mask_points_out_of_range(points_list, point_cloud_range)

    input_dict = {
        'points': points_list
    }

    data_batch = collate_batch([input_dict])
    load_data_to_gpu(data_batch)

    model.eval()
    with torch.no_grad():
        starter, ender = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)
        torch.cuda.synchronize()
        starter.record()
        pred_dicts = model.forward(data_batch)
        ender.record()
        torch.cuda.synchronize()
        elapsed_time_ms = starter.elapsed_time(ender)
        print(f"Inference time: {elapsed_time_ms:.2f} ms")


    pred_dicts = move_to_cpu(pred_dicts)

    return pred_dicts