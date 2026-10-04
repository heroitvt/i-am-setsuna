from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def main():
    p = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter\ScenarioMessageData_Chapter_2"
    with open(p, "rb") as f:
        d = f.read()
    c = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    dec = c.decryptor().update(d)
    
    offset = 0
    while offset + 16 <= len(dec):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if rid in (2458, 2610):
            print(f"\n--- RID {rid} ---")
            cur = offset + 16
            cur += 1 + dec[cur]
            cur += 1 + dec[cur]
            s1 = dec[cur:cur+l1]; cur += l1
            s2 = dec[cur:cur+l2]; cur += l2
            s3 = dec[cur:cur+l3]; cur += l3
            print(f"s2 l2={l2}: hex={s2[:10].hex()}")
            print(f"s3 l3={l3}: hex={s3[:10].hex()}")
        offset += rlen

if __name__ == "__main__":
    main()
