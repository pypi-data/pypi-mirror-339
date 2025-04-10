from typing import Union, List, Tuple

from transformers import PreTrainedTokenizer

from mindify.utilities import Alphabet


class DataTransformer:
    def __init__(self, batch_size: int = None):
        self.batch_size = batch_size

    def apply(self, dataset):
        return dataset.map(self, batched=self.batch_size is not None, batch_size=self.batch_size)


class DataTransformers:
    def __init__(self, transformers: Union[List[DataTransformer], Tuple[DataTransformer]]):
        self.transformers = transformers

    def apply(self, dataset):
        for transformer in self.transformers:
            dataset = transformer.apply(dataset)

        return dataset


class DataTransformerForAlphabetLabel(DataTransformer):
    def __init__(self, alphabet: Alphabet, batch_size: int = 128):
        super().__init__(batch_size)
        self.alphabet = alphabet

    def __call__(self, batch):
        batch['label_txt'] = batch['label']
        batch['label'] = self.alphabet.lookup(batch['label'])
        return batch


class DataTransformerForToken(DataTransformer):
    def __init__(self, tokenizer: PreTrainedTokenizer, max_length: int = 512, batch_size: int = 2):
        super().__init__(batch_size)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __call__(self, batch):
        encoding = self.tokenizer(batch['text'], truncation=True, max_length=self.max_length)
        batch['input_ids'] = encoding.input_ids
        batch['attention_mask'] = encoding.attention_mask
        return batch
