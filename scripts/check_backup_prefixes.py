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
    non_01_prefixes = []
    length_mismatches = []
    
    for r in range(1403):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        cur = offset + 16
        n_len = dec[cur]; cur += 1 + n_len
        q_len = dec[cur]; cur += 1 + q_len
        
        for s_idx, l in enumerate([l1, l2, l3], 1):
            s_bytes = dec[cur:cur+l]
            cur += l
            if l == 0:
                continue
            pre = s_bytes[0]
            if pre != 1:
                non_01_prefixes.append((rid, s_idx, pre, l, s_bytes[:4].hex()))
            else:
                str_byte_len = s_bytes[1]
                if str_byte_len + 2 != l:
                    length_mismatches.append((rid, s_idx, str_byte_len, l))
                    
        offset += rlen
        
    print(f"Non-01 prefixes in PRISTINE BACKUP: {len(non_01_prefixes)}")
    if non_01_prefixes:
        print("  Sample non-01:", non_01_prefixes[:10])
    print(f"Length mismatches (when prefix is 0x01): {len(length_mismatches)}")

if __name__ == "__main__":
    main()
