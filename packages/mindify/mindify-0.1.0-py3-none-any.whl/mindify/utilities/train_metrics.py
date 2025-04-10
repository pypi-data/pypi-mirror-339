from typing import List

import pandas as pd
import torch
from torchmetrics import MeanMetric

from mindify.utilities import ConfusionMatrix


class TrainMetrics:
    def __init__(self, labels: List[str], device: str = 'cuda'):
        self.train_confusion_matrix = ConfusionMatrix(labels)
        self.valid_confusion_matrix = ConfusionMatrix(labels)

        self.loss = MeanMetric().to(device)
        self.acc = MeanMetric().to(device)
        self.val_loss = MeanMetric().to(device)
        self.val_acc = MeanMetric().to(device)

    def update_loss(self, loss: torch.Tensor, weight=None):
        self.loss.update(loss, weight)

    def update_acc(self, y_pred: torch.Tensor, y_true: torch.Tensor, weight=None):
        if len(y_pred.size()) > len(y_true.size()):
            y_pred = y_pred.argmax(dim=-1)

        acc = torch.eq(y_pred, y_true).float().mean()
        self.acc.update(acc, weight)
        self.train_confusion_matrix.update(y_pred, y_true)

    def update_val_loss(self, val_loss: torch.Tensor, weight=None):
        self.val_loss.update(val_loss, weight)

    def update_val_acc(self, y_pred: torch.Tensor, y_true: torch.Tensor, weight=None):
        if len(y_pred.size()) > len(y_true.size()):
            y_pred = y_pred.argmax(dim=-1)

        acc = torch.eq(y_pred, y_true).float().mean()
        self.val_acc.update(acc, weight)
        self.valid_confusion_matrix.update(y_pred, y_true)

    def to_dict(self):
        result = {
            'loss': self.loss.compute().item(),
            'acc': self.acc.compute().item()
        }

        if self.val_loss.weight != 0.:
            val_loss = self.val_loss.compute().item()
            if not pd.isna(val_loss):
                result['val_loss'] = val_loss
                result['val_acc'] = self.val_acc.compute().item()

        return result

    def reset(self):
        self.loss.reset()
        self.acc.reset()
        self.val_loss.reset()
        self.val_acc.reset()
        self.train_confusion_matrix.reset()
        self.valid_confusion_matrix.reset()
