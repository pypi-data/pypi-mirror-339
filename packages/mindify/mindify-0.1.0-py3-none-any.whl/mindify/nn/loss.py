import torch
import torch.nn as nn
import torch.nn.functional as F


class FocalLoss(nn.Module):
    """Multi-class Focal loss implementation"""
    def __init__(self, gamma=2, weight=None, reduction='mean', ignore_index=-100):
        super(FocalLoss, self).__init__()
        self.gamma = gamma
        self.weight = weight
        self.ignore_index = ignore_index
        self.reduction = reduction

    def forward(self, input, target):
        """
        input: [N, C]
        target: [N, ]
        """
        log_pt = torch.log_softmax(input, dim=1)
        pt = torch.exp(log_pt)
        log_pt = (1 - pt) ** self.gamma * log_pt
        loss = torch.nn.functional.nll_loss(log_pt, target, self.weight, reduction=self.reduction, ignore_index=self.ignore_index)
        return loss


class RDropLoss(nn.Module):
    """
    https://github.com/dropreg/R-Drop
    """
    def __init__(self):
        super(RDropLoss, self).__init__()
        self.ce = FocalLoss(reduction='none')
        self.kld = nn.KLDivLoss(reduction='none')

    def forward(self, logits1, logits2, target, kl_weight=1.):
        """
        Args:
            logits1: One output of the classification model.
            logits2: Another output of the classification model.
            target: The target labels.
            kl_weight: The weight for `kl_loss`.

        Returns:
            loss: Losses with the size of the batch size.
        """
        ce_loss = (self.ce(logits1, target) + self.ce(logits2, target)) / 2
        kl_loss1 = self.kld(F.log_softmax(logits1, dim=-1), F.softmax(logits2, dim=-1)).sum(-1)
        kl_loss2 = self.kld(F.log_softmax(logits2, dim=-1), F.softmax(logits1, dim=-1)).sum(-1)
        kl_loss = (kl_loss1 + kl_loss2) / 2
        loss = ce_loss + kl_weight * kl_loss
        return torch.mean(loss)


class RDropPlusLoss(nn.Module):
    """
    https://github.com/dropreg/R-Drop
    """
    def __init__(self, label_smoothing: float = 0., label_weight=None, alpha=0.8, t=2):
        super().__init__()
        self.ce = nn.CrossEntropyLoss(label_smoothing=label_smoothing, weight=label_weight, reduction='none')
        self.kld = nn.KLDivLoss(reduction='none')
        self.alpha = alpha
        self.t = t

    def forward(self, logits1, logits2, target):
        """
        Args:
            logits1: One output of the classification model.
            logits2: Another output of the classification model.
            target: The target labels.
            kl_weight: The weight for `kl_loss`.

        Returns:
            loss: Losses with the size of the batch size.
        """
        ce_loss = (self.ce(logits1, target) + self.ce(logits2, target)) / 2
        kl_loss1 = self.kld(F.log_softmax(logits1, dim=-1), F.softmax(logits2, dim=-1)).sum(-1)
        kl_loss2 = self.kld(F.log_softmax(logits2, dim=-1), F.softmax(logits1, dim=-1)).sum(-1)
        kl_loss = (kl_loss1 + kl_loss2) / 2
        # ce_loss=hard_loss, kl_loss=soft_loss
        loss = kl_loss * self.alpha * (self.t ** 2) + ce_loss * (1.0 - self.alpha)
        return torch.mean(loss)


class LCMLoss(nn.Module):
    def __init__(self, num_labels, alpha=2):
        super().__init__()
        self.num_labels = num_labels
        self.alpha = alpha

    def forward(self, y_true, y_pred, label_distribution):
        label_distribution = F.softmax(label_distribution, dim=-1)
        pred_log_probs = F.log_softmax(y_pred, dim=-1)
        simulated_y_true = F.softmax(label_distribution + self.alpha * F.one_hot(y_true, self.num_labels), dim=-1)
        loss = nn.KLDivLoss(reduction='batchmean')(pred_log_probs, simulated_y_true)
        return loss