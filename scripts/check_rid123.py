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
    for r in range(130):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if rid == 123:
            cur = offset + 16
            cur += 1 + dec[cur]
            cur += 1 + dec[cur]
            s1 = dec[cur:cur+l1]; cur += l1
            s2 = dec[cur:cur+l2]; cur += l2
            print(f"RID 123: l1={l1}, l2={l2}, l3={l3}, rlen={rlen}")
            print(f"s2 raw first 20 bytes: {s2[:20].hex()}")
            print(f"s2 raw last 20 bytes: {s2[-20:].hex()}")
        offset += rlen

if __name__ == "__main__":
    main()
