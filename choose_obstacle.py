from detectron2.structures import instances
import torch
import numpy as np
from collections import Counter


def instance_to_numpy(instance):
    instance_as_np = instance
    instance_as_np["pred_boxes"] = instance_as_np["pred_boxes"].tensor
    return {key: value.cpu().detach().numpy() for key, value in instance_as_np.items()}


def which_instance_case(instance):
    instance_types = Counter(instance["pred_classes"])
    num_staging = instance_types.get(0, 0)
    num_obst = instance_types.get(1, 0)
    if num_staging == 0 and num_obst > 0:
        return "only_obstacles"
    elif num_staging == 1 and num_obst == 0:
        return "only_staging"
    elif num_staging == 1 and num_obst == 1:
        return "staging_and_one_obstacle"
    elif num_staging == 1 and num_obst > 1:
        return "staging_and_multiple_obstacles"


def choose_obstacle(instance):
    instance_as_np = instance_to_numpy(instance)
    instance_case = which_instance_case(instance_as_np)

    return_dict = {}
    if instance_case == "staging_and_one_obstacle":
        obst_index = int(np.where(instance_as_np["pred_classes"] == 1)[0])
        return {key: value[obst_index]
                for key, value in instance_as_np.items()}
    if instance_case == "only_staging" or instance_case == "staging_and_multiple_obstacles":
        obst_index = int(np.where(instance_as_np["pred_classes"] == 0)[0])
        return {key: value[obst_index]
                for key, value in instance_as_np.items()}
    return ""
