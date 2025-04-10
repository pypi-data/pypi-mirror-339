import json
import os
import random
import string
from typing import Optional, Any


class TrainArchive:
    def __init__(self, name: Optional[str] = None, output_dir: str = r'/data/archives'):
        """

        :param name: 通常是文件名
        """
        if name is None:
            name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        elif name.endswith(".py"):
            name = name[:-3]

        name = "_".join(name.replace("\\", "/").split("/")[-3:])

        archive_base_output_dir = os.path.join(output_dir, name)
        for i in range(10000):
            archive_output_dir = os.path.join(archive_base_output_dir, f"0000{i}")
            if not os.path.exists(archive_output_dir):
                break

        os.makedirs(archive_output_dir, 0o777)
        self.archive_path = archive_output_dir
        # 超参数
        self.hyperparameters = {}
        # 指标数据
        self.metrics = []
        # 普通数据
        self.value_index = {}

    def log_hyperparameters(self, **kwargs):
        self.hyperparameters.update(**kwargs)
        with open(os.path.join(self.archive_path, "hyperparams.json"), "w", encoding="UTF-8") as fp:
            json.dump(self.hyperparameters, fp, ensure_ascii=False, indent=4)

    def log_metrics(self, flush: bool = True, **kwargs):
        if len(kwargs) > 0:
            self.metrics.append(kwargs)

        if flush:
            with open(os.path.join(self.archive_path, "metrics.json"), "w", encoding="UTF-8") as fp:
                json.dump(self.metrics, fp, ensure_ascii=False, indent=4)

    def log(self, name: str, value: Any):
        value_index = 1 + self.value_index.get(name, 0)
        with open(os.path.join(self.archive_path, f"{name}-{value_index}.json"), "w", encoding="UTF-8") as fp:
            try:
                json.dump(value, fp, ensure_ascii=False, indent=4)
            except:
                fp.write(value.__repr__())
