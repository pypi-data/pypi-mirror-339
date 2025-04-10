from typing import Union, Dict, List
import numpy as np
from mindify.utilities import DictObject


class HyperParamGroup:
    """
    生成超参数的组合，参数组合调优

    HyperParamGroup({"learning_rate": [1e-5, 2e-5], "weight_decay": [0., 1e-3, 1e-5])
    """
    def __init__(self, config: Dict):
        for name, value in config.items():
            if not isinstance(value, List):
                config[name] = [value]

        self.config = config
        self.hparams_len = np.cumprod([len(v) for n, v in self.config.items()])[-1]

    def __len__(self):
        return self.hparams_len

    def __iter__(self):
        for index in range(self.hparams_len):
            yield self.__getitem__(index)

    def __getitem__(self, index):
        hparams = DictObject()

        index = index % self.hparams_len
        for n, v in self.config.items():
            hparams[n] = v[index % len(v)]
            index = index // len(v)

        return hparams


if __name__ == '__main__':
    hparams_group = HyperParamGroup({
        'learning_rate': [1e-3, 1e-5],
        'weight_decay': [0, 1e-3, 1e-4]
    })

    for hparams in hparams_group:
        print(hparams)
        print(hparams.learning_rate)
