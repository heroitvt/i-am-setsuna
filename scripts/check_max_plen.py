from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def main():
    p = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter_backup_before_MASTER_FINAL\ScenarioMessageData_Chapter_1.backup_before_CH1_LOOSE_TEST"
    with open(p, "rb") as f:
        d = f.read()
    c = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    dec = c.decryptor().update(d)
    
    offset = 0
    max_lens = [0, 0, 0]
    
    for r in range(1403):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        cur = offset + 16
        cur += 1 + dec[cur]
        cur += 1 + dec[cur]
        
        for idx, l in enumerate([l1, l2, l3]):
            s_bytes = dec[cur:cur+l]
            cur += l
            if len(s_bytes) > 0:
                num_p = s_bytes[0]
                c_p = 1
                for _ in range(num_p):
                    plen = s_bytes[c_p]
                    if plen > max_lens[idx]:
                        max_lens[idx] = plen
                    c_p += 1 + plen
        offset += rlen
        
    print(f"Max page length in pristine Chapter 1: s1={max_lens[0]}, s2={max_lens[1]}, s3={max_lens[2]}")

if __name__ == "__main__":
    main()
