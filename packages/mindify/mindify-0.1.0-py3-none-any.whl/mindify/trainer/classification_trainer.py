import logging
import os
import random
import string
from pathlib import Path
from typing import Optional, Union, List

import numpy as np
import torch
from datasets import Dataset
from sklearn.model_selection import KFold
from torch import nn
from torch.cuda.amp import autocast
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader
from tqdm import tqdm

from mindify.nn.collator import DataCollatorWithPaddingAndFeatures
from mindify.utilities import TrainArchive, Alphabet
from mindify.utilities.train_metrics import TrainMetrics


def compute_label_weights(
        dataset: Union[Dataset, List[int]], return_tensor: str = 'pt'
) -> Union[torch.Tensor, np.ndarray]:
    """
    计算每个分类的权重 sum(sqrt(X)) / sqrt(x)

    @param dataset:
    @param return_tensor:
    @return:
    """
    if isinstance(dataset, Dataset):
        labels = dataset['label']
    else:
        labels = dataset

    vc = pd.value_counts(labels)

    label_weights = np.zeros(len(vc))
    for label, count in vc.items():
        label_weights[int(label)] = count

    label_weights = np.max(label_weights) / label_weights
    label_weights = label_weights / np.mean(label_weights)

    if return_tensor == 'pt':
        return torch.tensor(label_weights, dtype=torch.float)
    else:
        return label_weights


class ClassificationTrainer:
    def __init__(
            self,
            alphabet: Alphabet,
            output_dir: Optional[str] = None,
            max_epochs: int = 20,
            batch_size: int = 16,
            gradient_accumulation_steps: int = 1,
            learning_rate: float = 2e-5,
            weight_decay: float = 0.,
            early_stop_warmup_steps: int = 0,
            early_stop_metric: str = 'val_loss',
            early_stop_patience: int = 2,
            device: str = 'cuda',
            archive: Optional[TrainArchive] = None
    ):
        self.alphabet = alphabet

        if output_dir is None:
            output_dir_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            output_dir = os.path.join(Path.home(), ".cache/outputs", output_dir_name)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, 0o777, exist_ok=True)
        logging.info(f"output_dir={self.output_dir}")

        self.max_epochs = max_epochs
        self.batch_size = batch_size
        self.gradient_accumulation_steps = gradient_accumulation_steps
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.early_stop_warmup_steps = early_stop_warmup_steps
        self.early_stop_metric = early_stop_metric
        self.early_stop_patience = early_stop_patience
        self.device = device

        if archive is None:
            self.archive = TrainArchive(name=None, output_dir=output_dir)

        self.archive.log_hyperparameters(
            max_epochs=max_epochs,
            batch_size=batch_size,
            gradient_accumulation_steps=gradient_accumulation_steps,
            learning_rate=learning_rate,
            weight_decay=weight_decay,
            early_stop_warmup_steps=early_stop_warmup_steps,
            early_stop_metric=early_stop_metric,
            early_stop_patience=early_stop_patience,
        )

    def train(self, model, tokenizer, train_dataset, valid_dataset, data_collator=None):
        if data_collator is None:
            data_collator = DataCollatorWithPaddingAndFeatures(
                tokenizer, features=['input_ids', 'attention_mask', 'label'])

        no_decay = ['bias', 'LayerNorm.weight']
        optimizer_grouped_parameters = [
            {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
             'weight_decay': self.weight_decay},
            {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
             'weight_decay': 0.0}
        ]

        optimizer = AdamW(optimizer_grouped_parameters, lr=self.learning_rate, weight_decay=self.weight_decay, eps=1e-8)
        scheduler = ReduceLROnPlateau(optimizer,
                                      patience=max(2, self.early_stop_patience // 2),
                                      factor=0.9,
                                      min_lr=self.learning_rate * 1e-3)

        train_loader = DataLoader(train_dataset, batch_size=self.batch_size, collate_fn=data_collator)
        valid_loader = DataLoader(valid_dataset, batch_size=self.batch_size, collate_fn=data_collator)

        train_metrics = TrainMetrics(self.alphabet.labels)

        best_metric = -1e9
        best_state_dict = None
        worth_metric_patience = 0

        model = model.to(self.device)
        for epoch in range(self.max_epochs):
            pbar = tqdm(total=len(train_loader) + len(valid_loader), desc=f"{epoch}/{self.max_epochs}")
            pbar_data = {'wp_ratio': worth_metric_patience / self.early_stop_patience}

            train_metrics.reset()

            model.train()
            for batch_idx, batch in enumerate(train_loader):
                batch = {k: v.to(self.device) for k, v in batch.items()}

                with autocast():
                    output = model(**batch)

                loss = output.loss / self.gradient_accumulation_steps
                loss.backward()

                if ((batch_idx + 1) % self.gradient_accumulation_steps == 0) or (batch_idx + 1 == len(train_loader)):
                    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

                    optimizer.step()
                    optimizer.zero_grad()

                train_metrics.update_loss(loss, batch['input_ids'].size(0) / self.batch_size)
                train_metrics.update_acc(output.logits, batch['labels'], batch['input_ids'].size(0) / self.batch_size)

                pbar_data.update({'lr': optimizer.param_groups[0]["lr"], **train_metrics.to_dict()})
                pbar.set_postfix(**pbar_data)
                pbar.update()

            model.eval()
            for batch_idx, batch in enumerate(valid_loader):
                batch = {k: v.to(self.device) for k, v in batch.items()}

                with torch.no_grad():
                    with autocast():
                        output = model(**batch)

                train_metrics.update_val_loss(output.loss, batch['input_ids'].size(0) / self.batch_size)
                train_metrics.update_val_acc(output.logits, batch['labels'], batch['input_ids'].size(0) / self.batch_size)

                pbar_data.update(train_metrics.to_dict())
                pbar.set_postfix(**pbar_data)
                pbar.update()

            scheduler.step(train_metrics.val_loss.compute())
            pbar.close()

            metric_value = train_metrics.to_dict()[self.early_stop_metric]
            if 'loss' in self.early_stop_metric:
                metric_value = - metric_value

            if metric_value >= best_metric:
                best_metric = metric_value
                best_state_dict = model.state_dict()

                worth_metric_patience = 0
            elif epoch >= self.early_stop_warmup_steps:
                worth_metric_patience += 1

            print("")
            print(train_metrics.train_confusion_matrix)
            print("")
            print(train_metrics.valid_confusion_matrix)

            if worth_metric_patience >= self.early_stop_patience:
                break

        model.load_state_dict(best_state_dict, False)
        return model

    def predict(self, model, tokenizer, valid_dataset, data_collator=None):
        if data_collator is None:
            data_collator = DataCollatorWithPaddingAndFeatures(
                tokenizer, features=['input_ids', 'attention_mask', 'label'])

        valid_loader = DataLoader(valid_dataset, batch_size=self.batch_size, collate_fn=data_collator)
        pbar = tqdm(total=len(valid_loader), desc=f"prediction")

        model = model.to(self.device)
        model.eval()

        predictions = []
        for batch_idx, batch in enumerate(valid_loader):
            batch = {k: v.to(self.device) for k, v in batch.items()}

            with torch.no_grad():
                with autocast():
                    output = model(**batch)

            predictions.extend(output.logits.cpu().numpy())
            pbar.update()

        pbar.close()

        return predictions

    def detect_noisy_samples(self, model: nn.Module, tokenizer, dataset):
        logging.info("保存模型原始权重")
        origin_state_dict = model.state_dict()

        logging.info("开始第一轮筛选")
        sample_probs = {}

        for random_state in [7, 8, 9]:
            kfold = KFold(n_splits=5, shuffle=True, random_state=random_state)
            kfold_iter = kfold.split(range(len(dataset)), y=dataset['label'])
            for fold_idx, (train_indices, valid_indices) in enumerate(kfold_iter):
                logging.info(f"第一轮 random_state#{random_state} fold#{fold_idx}")
                fold_train_dataset = dataset.select(train_indices)
                fold_valid_dataset = dataset.select(valid_indices)

                model.load_state_dict(origin_state_dict)
                model = self.train(model, tokenizer, fold_train_dataset, fold_valid_dataset)
                predictions = self.predict(model, tokenizer, fold_valid_dataset)

                for idx, sample_id in enumerate(fold_valid_dataset['id']):
                    if sample_id not in sample_probs:
                        sample_probs[sample_id] = []

                    sample_probs[sample_id].append(predictions[idx])

        error_sample_ids = []
        for idx, row in dataset.to_pandas().iterrows():
            preds = sample_probs[row['id']]
            if row['label'] not in preds:
                error_sample_ids.append(row['id'])

        logging.info(f"第一轮筛选出 {len(error_sample_ids)} 个错误样本")
        logging.info(f"错误样本 {error_sample_ids}")

        dataset = dataset.filter(lambda x: x['id'] not in error_sample_ids)

        logging.info("重新加载初始权重，开始第二轮筛选")
        model.load_state_dict(origin_state_dict)
        sample_probs = {}

        for random_state in [10, 11, 12]:
            kfold = KFold(n_splits=5, shuffle=True, random_state=random_state)
            kfold_iter = kfold.split(range(len(dataset)), y=dataset['label'])
            for fold_idx, (train_indices, valid_indices) in enumerate(kfold_iter):
                logging.info(f"第二轮 random_state#{random_state} fold#{fold_idx}")
                fold_train_dataset = dataset.select(train_indices)
                fold_valid_dataset = dataset.select(valid_indices)

                model.load_state_dict(origin_state_dict)
                model = self.train(model, tokenizer, fold_train_dataset, fold_valid_dataset)
                predictions = self.predict(model, tokenizer, fold_valid_dataset)

                for idx, sample_id in enumerate(fold_valid_dataset['id']):
                    if sample_id not in sample_probs:
                        sample_probs[sample_id] = []

                    sample_probs[sample_id].append(predictions[idx])

        for idx, row in dataset.to_pandas().iterrows():
            preds = sample_probs[row['id']]
            if row['label'] not in preds:
                error_sample_ids.append(row['id'])

        logging.info(f"第二轮筛选出 {len(error_sample_ids)} 个错误样本")
        logging.info(f"错误样本 {error_sample_ids}")

        return error_sample_ids
