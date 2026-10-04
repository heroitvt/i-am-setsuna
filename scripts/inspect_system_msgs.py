from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct
import os

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def decrypt_file(p):
    with open(p, "rb") as f:
        d = f.read()
    c = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    dec = c.decryptor().update(d)
    return dec

def inspect_param_file(name):
    p = os.path.join(r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter", name)
    if not os.path.exists(p):
        print(f"{name} not found!")
        return
    dec = decrypt_file(p)
    print(f"\n=== {name} (size: {len(dec)}) ===")
    
    # Check if format is same records
    offset = 0
    records = []
    while offset + 16 <= len(dec):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if magic != -1:
            break
        cur = offset + 16
        # some files don't have npc/quest, or do they?
        # let's check
        records.append((rid, l1, l2, l3, rlen, offset))
        offset += rlen
        
    print(f"Total parsed records in {name}: {len(records)}")
    for r in records[:5]:
        rid, l1, l2, l3, rlen, roff = r
        cur = roff + 16
        # let's find strings in record
        raw_rec = dec[roff:roff+rlen]
        # find ascii/utf-16 text
        s2_sample = ""
        try:
            # try finding utf-16
            import re
            u16 = re.findall(b"(?:[\x20-\x7e]\x00){3,}", raw_rec)
            texts = [b.decode('utf-16le') for b in u16]
            s2_sample = " | ".join(texts[:3])
        except:
            pass
        print(f"  RID {rid}: {s2_sample[:80]}")

def main():
    for f in ["TitleMessage", "SystemMessage", "BattleMessage", "CampMessage"]:
        inspect_param_file(f)

if __name__ == "__main__":
    main()
