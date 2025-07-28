import base64
import os


def restore_from_env(var_name, path):
    b64 = os.environ.get(var_name)
    if b64 and not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(base64.b64decode(b64))
