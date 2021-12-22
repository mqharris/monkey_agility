from detectron2.structures import instances
import torch
import math
import numpy as np
from collections import Counter


def distance(p, q):
    return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))


def instance_to_numpy(instance):
    instance_as_np = instance.copy()
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
    else:
        return "nothing_seen"


def choose_obstacle(instance):
    instance_as_np = instance_to_numpy(instance)
    instance_case = which_instance_case(instance_as_np)
    if instance_case == "staging_and_one_obstacle":
        index = int(np.where(instance_as_np["pred_classes"] == 1)[0])
    elif instance_case == "only_staging" or instance_case == "staging_and_multiple_obstacles":
        index = int(np.where(instance_as_np["pred_classes"] == 0)[0])
    elif instance_case == "only_obstacles":
        center_of_the_screen = [int(1920/2), int(1080/2)]
        centers = instance["pred_boxes"].get_centers()
        distances = [distance(center_of_the_screen, x)
                     for x in instance["pred_boxes"].get_centers()]
        index = distances.index(min(distances))
    else:
        raise Exception(instance_case)
    return {key: value[index]
            for key, value in instance_as_np.items()}
