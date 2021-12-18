import torch
import detectron2
from detectron2.structures import boxes, instances
import numpy as np


def test_thing():

    cuda0 = torch.device("cuda:0")
    pred_box_data = torch.tensor(
        [[479.2353, 769.0834, 572.7275, 829.9853],
         [888.4476, 515.3109, 987.8469, 615.1198]],
        device=cuda0)
    scores = torch.tensor(
        [[0.9131, 0.8989]],
        device=cuda0
    )
    pred_classes = torch.tensor(
        [1, 0],
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
    print(fields)
    return


if __name__ == "__main__":
    test_thing()
