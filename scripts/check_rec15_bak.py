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
    for r in range(20):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if rid == 15:
            cur = offset + 16
            cur += 1 + dec[cur]
            cur += 1 + dec[cur]
            s1 = dec[cur:cur+l1]; cur += l1
            s2 = dec[cur:cur+l2]; cur += l2
            s3 = dec[cur:cur+l3]; cur += l3
            print(f"Record 15 in backup:")
            print(f"  l1={l1}: prefix={s1[:2].hex()}")
            print(f"  l2={l2}: prefix={s2[:2].hex()}")
            print(f"  s2 hex: {s2.hex()}")
            print(f"  l3={l3}: prefix={s3[:2].hex()}")
        offset += rlen

if __name__ == "__main__":
    main()
