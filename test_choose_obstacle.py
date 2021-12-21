import torch
import detectron2
from detectron2.structures import boxes, instances
import numpy as np
import choose_obstacle as co


def create_one_staging_one_obstacle():
    cuda0 = torch.device("cuda:0")
    pred_box_data = torch.tensor(
        [[479.2353, 769.0834, 572.7275, 829.9853],
         [888.4476, 515.3109, 987.8469, 615.1198]],
        device=cuda0)
    scores = torch.tensor(
        [0.9131, 0.8989],
        device=cuda0
    )
    pred_classes = torch.tensor(
        [0, 1],
        device=cuda0
    )
    pred_masks = torch.tensor(
        [[False, False], [False, False]],
        device=cuda0
    )
    fields = {
        "pred_boxes": boxes.Boxes(pred_box_data),
        "scores": scores,
        "pred_classes": pred_classes,
        "pred_masks": pred_masks
    }
    return fields


def create_only_one_obstacle():
    cuda0 = torch.device("cuda:0")
    pred_box_data = torch.tensor(
        [[888.4476, 515.3109, 987.8469, 615.1198]],
        device=cuda0)
    scores = torch.tensor(
        [0.8989],
        device=cuda0
    )
    pred_classes = torch.tensor(
        [1],
        device=cuda0
    )
    pred_masks = torch.tensor(
        [[False, False]],
        device=cuda0
    )
    fields = {
        "pred_boxes": boxes.Boxes(pred_box_data),
        "scores": scores,
        "pred_classes": pred_classes,
        "pred_masks": pred_masks
    }
    return fields


def test_which_instance_case():
    one_one = create_one_staging_one_obstacle()
    one_one = co.instance_to_numpy(one_one)
    returned = co.which_instance_case(one_one)
    assert co.which_instance_case(one_one) == "staging_and_one_obstacle"


def test_choose_obstacle():
    returned = co.choose_obstacle(create_one_staging_one_obstacle())
    expected = co.instance_to_numpy(create_only_one_obstacle())
    for key, value in returned.items():
        assert np.all(value == expected[key])


def test_instance_to_numpy():
    one_one = create_one_staging_one_obstacle()
    pred_box_data = np.array([[479.2353, 769.0834, 572.7275, 829.9853], [
                             888.4476, 515.3109, 987.8469, 615.1198]], dtype="float32")
    scores = np.array([0.9131, 0.8989], dtype="float32")
    pred_classes = np.array([0, 1])
    pred_masks = np.array([[False, False], [False, False]])
    expected = {
        "pred_boxes": pred_box_data,
        "scores": scores,
        "pred_classes": pred_classes,
        "pred_masks": pred_masks
    }
    returned = co.instance_to_numpy(one_one)
    for key, value in returned.items():
        assert np.all(value == expected[key])


if __name__ == "__main__":
    test_instance_to_numpy()
    test_choose_obstacle()
    test_which_instance_case()
