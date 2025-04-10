import json
from typing import Union, List

import torch


class Alphabet:
    """
    字典工具类
    """

    def __init__(self):
        """

        @rtype: object
        """
        self.label2id = {}
        self.id2label = {}
        self.frozen = False

    @classmethod
    def from_json(cls, json_file, frozen: bool = True):
        alphabet = Alphabet()

        with open(json_file, 'r', encoding='utf-8') as fp:
            data = json.load(fp)

        alphabet.label2id = {label: int(index) for index, label in data.items()}
        alphabet.id2label = {int(index): label for index, label in data.items()}

        alphabet.frozen = frozen

        return alphabet

    def to_json(self, json_file):
        with open(json_file, 'w', encoding='utf-8') as fp:
            json.dump(self.id2label, fp)

    def contains(self, label):
        return label in self.label2id

    def lookup(self, label: Union[str, List[str]]):
        if isinstance(label, List):
            return [self.lookup(l) for l in label]

        if label not in self.label2id:
            if self.frozen:
                raise ValueError(f"{label} label not found")

            id = len(self.label2id)
            self.label2id[label] = id
            self.id2label[id] = label

        return self.label2id[label]

    def lookup_label(self, id: Union[torch.Tensor, int]):
        if isinstance(id, torch.Tensor):
            id = id.item()

        if id not in self.id2label:
            raise ValueError(f"{id} not in alphabet")

        return self.id2label.get(id)

    def freeze(self, frozen: bool = True):
        self.frozen = frozen
        return self

    @property
    def size(self):
        return len(self.label2id)

    @property
    def labels(self):
        return [self.id2label[i] for i in range(self.size)]

    def __len__(self):
        return len(self.label2id)

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.lookup(item)
        else:
            return self.lookup_label(item)


if __name__ == "__main__":
    alphabet = Alphabet()
    print(alphabet.lookup("llo"))
    print(alphabet["abc"])
    print(alphabet["abc1"])
    print(alphabet[1])
    print(alphabet.lookup_label(2))
