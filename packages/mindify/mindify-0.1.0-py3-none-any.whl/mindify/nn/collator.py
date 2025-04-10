from dataclasses import dataclass
from typing import List, Dict, Any

from transformers import DataCollatorWithPadding


@dataclass
class DataCollatorWithPaddingAndFeatures(DataCollatorWithPadding):
    features: List[str] = None

    def __call__(self, features: List[Dict[str, Any]]) -> Dict[str, Any]:
        if self.features is None:
            self.features = ['input_ids', 'attention_mask', 'token_type_ids', 'labels', 'label']

        features = [{k: v for k, v in feature.items() if k in self.features} for feature in features]
        return super().__call__(features)
