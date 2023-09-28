import json
import sys
from ..common.config import *
import pyotp


def generate_totp(key):
    authkey = pyotp.TOTP(key)
    totp = authkey.now()
    print(totp)
    return


if __name__ == "__main__":
    default_arg1 = "y"
    arg1 = sys.argv[1] if len(sys.argv) > 1 else default_arg1
    # print(f"arg1: {arg1}")
    auth_dict = {"y": AUTH_YASH, "m": AUTH_MOHAN}

    f = open(auth_dict[arg1])
    data = json.load(f)
    f.close()

    for i, v in data.items():
        print(i, end=" ")
        generate_totp(v)
