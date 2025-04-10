import os
import zipfile
from pathlib import Path
from typing import Union, Dict

import kaggle


class KaggleApi:
    @classmethod
    def uncompress_folder(cls, dataset_path):
        for file in os.listdir(dataset_path):
            if not file.lower().endswith(".zip"):
                continue

            extract_path = os.path.join(dataset_path, file[:-4])
            if os.path.exists(extract_path):
                continue

            zip_file = os.path.join(dataset_path, file)

            zip_file = zipfile.ZipFile(zip_file)
            zip_file.extractall(extract_path)

    @classmethod
    def get_dataset(cls, dataset, force=False, unzip=True, is_competition=False) -> Union[str, Dict[str, str]]:
        dataset_path = os.path.join(Path.home(), ".cache/kaggle", dataset)
        dataset_name = os.path.basename(dataset_path)

        zip_file = os.path.join(dataset_path, dataset_name + ".zip")
        if not os.path.exists(zip_file) or force:
            api = kaggle.KaggleApi()
            api.authenticate()

            if is_competition:
                api.competition_download_files(dataset, path=dataset_path, quiet=False)
            else:
                api.dataset_download_files(dataset, path=dataset_path, quiet=False, unzip=False, force=True)

        if unzip:
            filenames = {}
            do_unzip = False

            try:
                zip_file = zipfile.ZipFile(zip_file)
                for fileinfo in zip_file.filelist:
                    file = os.path.join(dataset_path, dataset_name, fileinfo.filename)
                    filenames[fileinfo.filename] = file
                    if not os.path.exists(file):
                        do_unzip = True
            except Exception as ex:
                os.unlink(zip_file)
                raise Exception(f"打开文件 {zip_file} 错误，请重试")

            if do_unzip:
                cls.uncompress_folder(dataset_path)

            return filenames
        else:
            return dataset_path

    @classmethod
    def get_competition(cls, competition, force=False, unzip=True):
        return cls.get_dataset(competition, force=force, unzip=unzip, is_competition=True)


if __name__ == '__main__':
    files = KaggleApi.get_dataset('xhlulu/general-language-understanding-evaluation')
    print(files)
