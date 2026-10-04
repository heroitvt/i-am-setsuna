import os
import glob
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def main():
    pdir = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter"
    for ch in ["ScenarioMessageData_Chapter_2", "ScenarioMessageData_Chapter_3", "ScenarioMessageData_Chapter_4"]:
        fpath = os.path.join(pdir, ch)
        with open(fpath, "rb") as f:
            d = f.read()
        dec = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend()).decryptor().update(d)
        offset = 0
        max_p = 0
        while offset + 16 <= len(dec):
            magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
            if magic != -1:
                break
            cur = offset + 16
            cur += 1 + dec[cur]
            cur += 1 + dec[cur]
            for l in [l1, l2, l3]:
                s_bytes = dec[cur:cur+l]
                cur += l
                if len(s_bytes) > 0:
                    num_p = s_bytes[0]
                    c_p = 1
                    for _ in range(num_p):
                        plen = s_bytes[c_p]
                        if plen > max_p:
                            max_p = plen
                        c_p += 1 + plen
            offset += rlen
        print(f"{ch}: max page length = {max_p}")

if __name__ == "__main__":
    main()
