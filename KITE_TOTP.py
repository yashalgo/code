import pyotp

authkey = pyotp.TOTP('AGFEGMUBAB2KIIKUGF3YSPRBVWXVQEJ4')
print(authkey.now())
