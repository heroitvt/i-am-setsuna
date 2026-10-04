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
    mismatches = []
    for r in range(1403):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        cur = offset + 16
        n_len = dec[cur]; cur += 1 + n_len
        q_len = dec[cur]; cur += 1 + q_len
        cur += l1 + l2 + l3
        consumed = cur - offset
        if consumed != rlen:
            mismatches.append((rid, consumed, rlen))
        offset += rlen
        
    print(f"Total mismatches between (16 + 1 + n_len + 1 + q_len + l1 + l2 + l3) and rlen: {len(mismatches)}")
    if mismatches:
        for m in mismatches[:10]:
            print(f"  RID {m[0]}: consumed {m[1]} vs rlen {m[2]}")

if __name__ == "__main__":
    main()
