import pyotp
import json
import sys
from ..common.config import *


def generate_totp(key):
    authkey = pyotp.TOTP(key)
    totp = authkey.now()
    print(totp)
    return


f = open(AUTH_FILE)
data = json.load(f)
f.close()

if len(sys.argv) > 1:
    platform = sys.argv[1]
    # print(platform)
    key = data[platform]
    generate_totp(key)
else:
    for i, v in data.items():
        print(i, end=" ")
        generate_totp(v)
