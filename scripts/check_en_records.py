from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def main():
    p = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter\ScenarioMessageData_Chapter_1"
    with open(p, "rb") as f:
        d = f.read()
    c = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    dec = c.decryptor().update(d)
    
    offset = 0
    for r in range(1403):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if rid in (350, 600, 900, 1200):
            cur = offset + 16
            n_len = dec[cur]; cur += 1 + n_len
            q_len = dec[cur]; cur += 1 + q_len
            cur += l1
            s2 = dec[cur:cur+l2]
            print(f"RID {rid}: l2={l2}, prefix={s2[:4].hex()}, text={repr(s2.decode('utf-16le', errors='ignore')[:30])}")
        offset += rlen

if __name__ == "__main__":
    main()
