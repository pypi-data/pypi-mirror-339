import hashlib
import inspect
import json
import os
from functools import wraps

from mindify.cache.core import ENOVAL
from mindify.cache.oss_client import OssClient




def full_name(func):
    """Return full name of `func` by adding the module and function name."""
    return func.__module__ + '.' + func.__qualname__


def _hash_key(name: str, version: str, func, *args, **kwargs):
    sig = inspect.signature(func)
    func_name = full_name(func)
    params = sig.parameters

    # param_names = [key for key in params.keys()]
    param_dict = {'__func_name': func_name}
    param_dict.update(zip(params.keys(), args))
    param_dict.update(kwargs)

    for k in (params.keys() - param_dict.keys()):
        param_dict[k] = params[k].default

    key = list(sorted(param_dict.items()))

    m = hashlib.md5()
    m.update(json.dumps(key).encode("utf-8"))
    hashkey = m.hexdigest()

    path = [name, version, hashkey[0:2], hashkey]
    path = "/".join([p for p in path if p])

    return path


class DiskCache:
    def __init__(self, root_path=".cache"):
        self.root_path = root_path

    def bucket(self, name="default", version: str = "v1", expiration: int = 0):
        def decorator(func):
            @wraps(func)
            def decorated(*args, **kwargs):
                hash_path = _hash_key(name, version, func, *args, **kwargs)
                cache_file = os.path.join(self.root_path, hash_path)

                if os.path.exists(cache_file):
                    with open(cache_file, 'r', encoding='utf8') as fp:
                        try:
                            return json.load(fp)
                        except:
                            pass

                result = func(*args, **kwargs)
                if result is not None:
                    os.makedirs(os.path.dirname(cache_file), 0o777, exist_ok=True)

                    with open(cache_file, 'w', encoding='utf8') as fp:
                        fp.write(json.dumps(result))

                return result

            return decorated
        return decorator


class OssCache:
    def __init__(self, root_path=".cache"):
        self.root_path = root_path
        self.oss_client = OssClient()

    def bucket(self, name="default", version: str = "v1", expiration: int = 0):
        def decorator(func):
            @wraps(func)
            def decorated(*args, **kwargs):
                hash_path = _hash_key(name, version, func, *args, **kwargs)
                result = self.oss_client.get_object(hash_path)
                if result != ENOVAL:
                    return result

                result = func(*args, **kwargs)
                self.oss_client.put_object(hash_path, result)
                return result

            return decorated

        return decorator



if __name__ == '__main__':
    cache = OssCache()

    @cache.bucket("add")
    def add(a: int = 1):
        print(f"calling a={a}")
        return a + 1

    print(add(1))
    print(add(1))