from typing import Union, List

import numpy as np
import torch
from sklearn.metrics import classification_report, confusion_matrix


class ConfusionMatrix:
    def __init__(self, labels, text=None):
        self.labels = labels
        self.text = text
        self.y_preds = []
        self.y_reals = []

    def reset(self):
        self.y_preds = []
        self.y_reals = []

    def update(
            self,
            y_preds: Union[torch.Tensor, np.ndarray, List[List[int]]],
            y_reals: Union[torch.Tensor, np.ndarray, List[int]]):
        if isinstance(y_preds, torch.Tensor):
            if y_preds.requires_grad:
                y_preds = y_preds.detach()

            y_preds = y_preds.cpu().numpy()

        if isinstance(y_reals, torch.Tensor):
            if y_reals.requires_grad:
                y_reals = y_reals.detach()

            y_reals = y_reals.cpu().numpy()

        y_preds = np.array(y_preds)
        y_reals = np.array(y_reals)

        pred_shape = y_preds.shape
        real_shape = y_reals.shape
        if len(pred_shape) > len(real_shape):
            y_preds = np.argmax(y_preds, axis=-1)

        self.y_preds.extend(y_preds)
        self.y_reals.extend(y_reals)

    def __repr__(self):
        if self.text is not None and len(self.text) == len(self.y_preds):
            for idx, b in enumerate(self.text):
                if b and self.y_preds[idx] == 2:
                    self.y_preds[idx] = 0

        y_reals = [self.labels[id] for id in self.y_reals]
        y_preds = [self.labels[id] for id in self.y_preds]

        cls_report = classification_report(y_reals, y_preds, labels=self.labels)
        cm_report = confusion_matrix(y_reals, y_preds, labels=self.labels)

        return str(cls_report) + "\n" + str(cm_report)
