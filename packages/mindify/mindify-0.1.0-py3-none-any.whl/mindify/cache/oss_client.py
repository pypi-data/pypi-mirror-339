import os
import pickle
from typing import Any, Union

import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

from mindify.cache.core import ENOVAL


# os.environ['OSS_ACCESS_KEY_ID'] = 'xx'
# os.environ['OSS_ACCESS_KEY_SECRET'] = 'xx'
# os.environ['OSS_BUCKET'] = 'clinify-cms'


class OssClient(object):
    def __init__(self, bucket_name: str = None, endpoint: str = None, region: str = None):
        bucket_name = os.getenv('OSS_BUCKET', '') if bucket_name is None else bucket_name
        endpoint = "https://oss-cn-beijing.aliyuncs.com" if not endpoint else endpoint
        region = "cn-beijing" if not region else region

        auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())
        self.bucket = oss2.Bucket(auth, endpoint, bucket_name, region=region)

    def put_object(self, object_name: str, content: Any):
        data = pickle.dumps(content, protocol=0)
        self.bucket.put_object(object_name, data)

    def get_object(self, object_name: str) -> Any:
        try:
            data = self.bucket.get_object(object_name).read()
            return pickle.loads(data)
        except:
            return ENOVAL

    def put_file(self, object_name: str, file_path: str):
        with open(file_path, 'rb') as fp:
            self.bucket.put_object(object_name, fp)

    def get_file(self, object_name: str, decoding: str = None) -> Union[bytes, str]:
        try:
            bdata = self.bucket.get_object(object_name).read()
            return bdata if not decoding else bdata.decode(decoding)
        except:
            return ENOVAL


if __name__ == '__main__':
    oss_client = OssClient()
    oss_client.put_file('temp/123', './requirements.txt')
    print(oss_client.get_file('temp/123', decoding='utf-8'))