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
    for r in range(1403):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if rid == 123:
            cur = offset + 16
            cur += 1 + dec[cur]
            cur += 1 + dec[cur]
            s1 = dec[cur:cur+l1]; cur += l1
            s2 = dec[cur:cur+l2]; cur += l2
            s3 = dec[cur:cur+l3]; cur += l3
            print("s2 raw len:", len(s2))
            print("s2 first 16 bytes:", list(s2[:16]))
            # Let's decode s2 from index 1, 2, 3, 4, 5
            for i in range(6):
                try:
                    txt = s2[i:].decode('utf-16le')
                    print(f"Index {i} decoded clean! len={len(txt)} chars, sample: {repr(txt[:20])}")
                except Exception as e:
                    pass
            break
        offset += rlen

if __name__ == "__main__":
    main()
