import math
import os
import random
import string
from pathlib import Path
from typing import Tuple, Union, Any, Optional, List

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from datasets import Dataset
from pytorch_lightning.utilities.types import STEP_OUTPUT
from torch.cuda.amp import autocast
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader
from torchmetrics import MeanMetric
from tqdm import tqdm
from transformers import PreTrainedModel, AutoModel, TrainingArguments, Trainer, \
    AutoTokenizer, PreTrainedTokenizer, BertForSequenceClassification
from transformers.modeling_outputs import SequenceClassifierOutput
import pytorch_lightning as pl
from mindify.nn import RDropLoss
from mindify.nn.collator import DataCollatorWithPaddingAndFeatures
from mindify.nn.loss import LCMLoss
from mindify.utilities import TrainArchive
from mindify.utilities.train_metrics import TrainMetrics


class AttentionBlock(nn.Module):
    def __init__(self, embed_dim, num_attention_heads,
                 feed_forward_hidden_size=1024,
                 feed_forward_layers=0,
                 dropout=0.1):
        super().__init__()

        self.layer_norm_1 = torch.nn.LayerNorm(normalized_shape=embed_dim)

        self.attention = torch.nn.MultiheadAttention(
            embed_dim=embed_dim,
            num_heads=num_attention_heads,
            dropout=dropout)

        self.layer_norm_2 = torch.nn.LayerNorm(normalized_shape=embed_dim)

        self.feed_forward = MultiLayerPerceptron(embed_dim, embed_dim, feed_forward_hidden_size, feed_forward_layers, dropout)
        self.dropout = torch.nn.Dropout(dropout)

    def forward(self, x):
        a, _ = self.attention(x, x, x)
        a = self.dropout(a)
        x = self.layer_norm_1(a + x)

        f = self.feed_forward(x)
        f = self.dropout(f)
        x = self.layer_norm_2(f + x)

        return x


class AttentionLayer(nn.Module):
    def __init__(self, embed_dim, num_attention_heads, num_attention_layers,
                 feed_forward_hidden_size=1024,
                 feed_forward_layers=0,
                 dropout=0.1):
        super().__init__()

        self.layer_norm = torch.nn.LayerNorm(embed_dim)

        self.attention_blocks = nn.ModuleList(
            [AttentionBlock(embed_dim, num_attention_heads, feed_forward_hidden_size, feed_forward_layers, dropout)
             for _ in range(num_attention_layers)]
        )

    def forward(self, x, *other_embeddings):
        for embeddings in other_embeddings:
            x = x + embeddings
        x = self.layer_norm(x)

        for block in self.attention_blocks:
            x = block(x)

        return x


class PositionalEmbeddings(nn.Module):
    def __init__(self, embed_dim, mode, max_len=70):
        super().__init__()

        self.mode = mode

        pe = torch.zeros(max_len, embed_dim)
        position = torch.arange(0, max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, embed_dim, 2) * -(math.log(10000.0) / embed_dim))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        self.register_buffer('pe', pe)

    def forward(self, x):
        if self.mode != 'complex-order':
            return torch.autograd.Variable(self.pe[:x.size(0)], requires_grad=False).to(x.device)
        else:
            position_size, embed_dim = x.size()

            position_j = 1. / torch.pow(10000., 2 * torch.arange(0, embed_dim, dtype=torch.float32) / embed_dim)
            position_j = torch.unsqueeze(position_j, 0)

            position_i = torch.arange(0, position_size, dtype=torch.float32)
            position_i = torch.unsqueeze(position_i, 1)
            position_ij = torch.matmul(position_i, position_j)
            position_embedding = position_ij

            return torch.autograd.Variable(position_embedding, requires_grad=False).to(x.device)


class LinearBlock(nn.Module):
    def __init__(self, input_dim, output_dim, dropout):
        super().__init__()

        self.model = torch.nn.Sequential(
            torch.nn.Linear(input_dim, output_dim),
            torch.nn.GELU(),
            torch.nn.Dropout(dropout)
        )

    def forward(self, x):
        return self.model(x)


class MultiLayerPerceptron(nn.Module):
    """
    MLP 多层感知机
    """
    def __init__(self, in_features, out_features, hidden_dim: Union[int, List[int]] = None, num_blocks: int = 1, dropout: float = None):
        super().__init__()

        num_blocks = 1 if num_blocks is None else num_blocks

        if hidden_dim is None:
            hidden_dim = out_features

        if not isinstance(hidden_dim, list):
            hidden_dim = [hidden_dim] * num_blocks

        assert len(hidden_dim) == num_blocks, "hidden_dim and num_blocks must be equal"
        assert num_blocks > 0, "num_blocks must be greater than 0"

        dropout = 0.1 if dropout is None else dropout

        self.model = torch.nn.Sequential(
            LinearBlock(in_features, hidden_dim[0], dropout),
            torch.nn.Sequential(
                *[LinearBlock(hidden_dim[idx], hidden_dim[idx+1], dropout) for idx in range(num_blocks-1)]
            ),
            nn.Linear(hidden_dim[-1], out_features),
        )

    def forward(self, x):
        return self.model(x)


class ClassifierModel(nn.Module):
    def __init__(self, hidden_size: int, num_labels: int, dropout: float = 0.1):
        super().__init__()
        self.model = nn.Sequential(
            nn.Tanh(),
            MultiLayerPerceptron(hidden_size, out_features=num_labels, num_blocks=1, dropout=dropout)
        )

    def forward(self, x):
        return self.model(x)


class RDropModel(nn.Module):
    def __init__(self, model: Union[PreTrainedModel, str], num_labels, label_smoothing: float = 0., label_weight=None):
        """

        :param model: AutoModel
        :param label_smoothing:
        :param label_weight:
        """
        super().__init__()
        self.model = model if isinstance(model, PreTrainedModel) else AutoModel.from_pretrained(model)

        self.classifier = ClassifierModel(self.model.config.hidden_size, num_labels=num_labels)
        self.loss_fct = RDropLoss(label_smoothing, label_weight)

    def forward(
            self, input_ids, attention_mask=None, token_type_ids=None, labels=None
    ) -> Union[SequenceClassifierOutput, Tuple[torch.Tensor, torch.Tensor]]:
        outputs_1 = self.model(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids
        )
        outputs_2 = self.model(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            return_dict=True,
        )

        logits_1 = self.classifier(outputs_1['last_hidden_state'][:, 0, :])
        logits_2 = self.classifier(outputs_2['last_hidden_state'][:, 0, :])

        logits = (logits_1 + logits_2) / 2

        if labels is not None:
            loss = self.loss_fct(logits_1, logits_2, labels)
        else:
            loss = None

        return SequenceClassifierOutput(loss=loss, logits=logits)


class CoTeaching(nn.Module):
    def __init__(self):
        super().__init__()


class LabelConfusionModel(nn.Module):
    def __init__(self, model: Union[PreTrainedModel, str], num_labels, hidden_size=None, alpha=2, label_dim=None):
        super().__init__()

        self.model = model if isinstance(model, PreTrainedModel) else AutoModel.from_pretrained(model)
        self.num_labels = num_labels

        if hidden_size is None:
            hidden_size = self.model.config.hidden_size

        if label_dim is None:
            label_dim = hidden_size

        self.model_fc1 = nn.Linear(self.model.config.hidden_size, hidden_size)
        self.model_fc2 = nn.Linear(hidden_size, num_labels)

        self.label_emb = nn.Embedding(num_labels, label_dim)
        self.label_fc = nn.Linear(label_dim, hidden_size)

        self.sim_fc = nn.Linear(num_labels, num_labels)
        self.loss_fct = LCMLoss(num_labels, alpha=alpha)

    def forward(self, input_ids=None, attention_mask=None, token_type_ids=None, labels=None):
        output = self.model(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        # (batch_size, model.config.hidden_size)
        text_emb = output['last_hidden_state'][:, 0, :]
        # 获取文本内容的表达, (batch_size, hidden_size)，范围 [-1, 1]
        text_emb = torch.tanh(self.model_fc1(text_emb))  # (b, v)
        # 获取预测分类的概率分布, (batch_size, num_labels)
        y_pred = self.model_fc2(text_emb)  # (b, n)

        label_inputs = torch.arange(self.num_labels)
        label_inputs = torch.stack([label_inputs] * input_ids.size(0), dim=0).to(input_ids.device)
        # 获取所有分类的embedding表达 (batch_size, num_labels, label_dim)
        label_emb = self.label_emb(label_inputs)  #
        # 获取所有分类的表达 (batch_size, num_labels, hidden_size)
        label_emb = torch.tanh(self.label_fc(label_emb))

        # (batch_size, num_labels, hidden_size) dot (batch_size, hidden_size, 1) -> (batch_size, num_labels, 1)
        doc_product = torch.bmm(label_emb, text_emb.unsqueeze(-1))  # (b,n,d) dot (b,d,1) --> (b,n,1)
        # (batch_size, num_labels, 1) -> (batch_size, num_labels) -> (batch_size, num_labels)
        label_distribution = self.sim_fc(doc_product.squeeze(-1))

        loss = None
        if labels is not None:
            loss = self.loss_fct(labels, y_pred, label_distribution)

        label_distribution = torch.softmax(label_distribution, dim=-1)
        return SequenceClassifierOutput(loss=loss, logits=y_pred, hidden_states=label_distribution)


def get_learning_rate(optimizer):
    return optimizer.param_groups[0]["lr"]


def compute_classifier_accuracy(preds, reals):
    preds = preds.argmax(dim=-1).view(-1)
    reals = reals.view(-1)

    return torch.sum(preds == reals) / preds.size(0)


class PLClassifierModel(pl.LightningModule):
    def __init__(self, model, learning_rate, weight_decay):
        super().__init__()
        self.model = model
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay

    def training_step(self, batch: Any, batch_idx: int) -> STEP_OUTPUT:
        output = self.mode(**batch)
        return output.loss

    def validation_step(self, batch: Any, batch_idx: int) -> Optional[STEP_OUTPUT]:
        output = self.mode(**batch)
        return output.loss

    def predict_step(self, batch: Any, batch_idx: int, dataloader_idx: int = 0) -> Any:
        output = self.mode(**batch)
        return output.logits

    def configure_optimizers(self) -> Any:
        no_decay = ['bias', 'LayerNorm.weight']
        optimizer_grouped_parameters = [
            {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
             'weight_decay': self.weight_decay},
            {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
             'weight_decay': 0.0}
        ]

        optimizer = AdamW(optimizer_grouped_parameters, lr=self.learning_rate, weight_decay=self.weight_decay)
        scheduler = ReduceLROnPlateau(optimizer, patience=3, factor=0.8)

        return optimizer, scheduler


def train_classifier_model(
        run_name,
        model: Union[PreTrainedModel, str], tokenizer: PreTrainedTokenizer,
        train_dataset, valid_dataset,
        output_dir=None,
        label_smoothing: float = 0.,
        learning_rate: float = 5e-5, weight_decay: float = 0.,
        batch_size: int = 64, gradient_accumulation_steps: int = 1,
        early_stop_metric: str = 'val_loss',
        early_stop_warmup_steps: int = 1,
        early_stop_patience: int = 2,
        max_epochs: int = 10,
        device: str = 'cuda'
):
    train_archive = TrainArchive(run_name)
    train_archive.log_hyperparameters(
        label_smoothing=label_smoothing,
        learning_rate=learning_rate,
        weight_decay=weight_decay,
        batch_size=batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps
    )

    if output_dir is None:
        output_dir_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        output_dir = os.path.join(Path.home(), ".cache/outputs", output_dir_name)
        print('output_dir', output_dir)

    model = AutoModel.from_pretrained(model) if isinstance(model, str) else model

    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
         'weight_decay': weight_decay},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
         'weight_decay': 0.0}
    ]

    optimizer = AdamW(optimizer_grouped_parameters, lr=learning_rate, weight_decay=weight_decay, eps=1e-8)
    scheduler = ReduceLROnPlateau(optimizer,
                                  patience=max(2, early_stop_patience // 2),
                                  factor=0.9,
                                  min_lr=learning_rate * 1e-3)

    data_collator = DataCollatorWithPaddingAndFeatures(
        tokenizer, features=['input_ids', 'attention_mask', 'label'])
    train_loader = DataLoader(train_dataset, batch_size=batch_size, collate_fn=data_collator)
    valid_loader = DataLoader(valid_dataset, batch_size=batch_size, collate_fn=data_collator)

    train_metrics = TrainMetrics(alphabet.labels)

    best_metric = -1e9
    worth_metric_patience = 0

    os.makedirs(output_dir, 0o777, exist_ok=True)
    checkpoint_file = os.path.join(output_dir, "checkpoint-best.pt")

    model = model.to(device)
    for epoch in range(max_epochs):
        pbar = tqdm(total=len(train_loader) + len(valid_loader), desc=f"{epoch}/{max_epochs}")
        pbar_data = {'wp_ratio': worth_metric_patience / early_stop_patience}

        train_metrics.reset()

        model.train()
        for batch_idx, batch in enumerate(train_loader):
            batch = {k: v.to(device) for k, v in batch.items()}

            with autocast():
                output = model(**batch)

            loss = output.loss / gradient_accumulation_steps
            loss.backward()

            if ((batch_idx + 1) % gradient_accumulation_steps == 0) or (batch_idx + 1 == len(train_loader)):
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

                optimizer.step()
                optimizer.zero_grad()

            train_metrics.update_loss(loss, batch['input_ids'].size(0) / batch_size)
            train_metrics.update_acc(output.logits, batch['labels'], batch['input_ids'].size(0) / batch_size)

            pbar_data.update({'lr': get_learning_rate(optimizer), **train_metrics.to_dict()})
            pbar.set_postfix(**pbar_data)
            pbar.update()

        model.eval()
        for batch_idx, batch in enumerate(valid_loader):
            batch = {k: v.to(device) for k, v in batch.items()}

            with torch.no_grad():
                with autocast():
                    output = model(**batch)

            train_metrics.update_val_loss(output.loss, batch['input_ids'].size(0) / batch_size)
            train_metrics.update_val_acc(output.logits, batch['labels'], batch['input_ids'].size(0) / batch_size)

            pbar_data.update(train_metrics.to_dict())
            pbar.set_postfix(**pbar_data)
            pbar.update()

        scheduler.step(train_metrics.val_loss.compute())
        pbar.close()

        metric_value = pbar_data[early_stop_metric]
        if 'loss' in early_stop_metric:
            metric_value = - metric_value

        if metric_value > best_metric:
            best_metric = metric_value
            torch.save(model.state_dict(), checkpoint_file)

            worth_metric_patience = 0
        elif epoch >= early_stop_warmup_steps:
            worth_metric_patience += 1

        if worth_metric_patience >= early_stop_patience:
            break

    print(f"saving model to {output_dir}")
    model.load_state_dict(torch.load(checkpoint_file), False)
    tokenizer.save_pretrained(output_dir)

    return model, tokenizer


def predict_classifier_model(model, tokenizer, input_ids):
    model = model.to('cuda')
    input_ids = torch.tensor(input_ids, device='cuda').unsqueeze(0)

    model.eval()
    with torch.no_grad():
        return model(input_ids=input_ids)


if __name__ == '__main__':
    from mindify.utilities.alphabet import Alphabet

    model_name = 'bert-base-chinese'

    dataset = Dataset.from_pandas(pd.read_excel(r'd:\datasets\poc\话务分析-旧.xlsx'))

    alphabet = Alphabet()
    dataset = dataset.map(lambda x: {'label_txt': x['label'], 'label': alphabet.lookup(x['label'])})

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    dataset = dataset.map(lambda x: tokenizer(x['text'], truncation=True, max_length=512))

    model = AutoModel.from_pretrained(model_name)
    model = LabelConfusionModel(model, alphabet.size)
    model.load_state_dict(torch.load(r'C:\Users\jameshu\.cache\outputs\0RUW57\checkpoint-best.pt'))

    for row_idx, row in dataset.to_pandas().iterrows():
        output = predict_classifier_model(model, tokenizer, row['input_ids'])

        matched = row['label_txt'] == row['ground_truth_label']
        if matched:
            continue

        print(matched, row['label_txt'], row['ground_truth_label'])
        print(row['label'], alphabet.lookup(row['ground_truth_label']),
              torch.argmax(output.hidden_states, dim=-1).item())
        print(output.hidden_states.cpu().numpy())

    # train_classifier_model(model, tokenizer, train_dataset=dataset, valid_dataset=dataset)
