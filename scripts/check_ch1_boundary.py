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
    
    # Check records 305 to 312
    offset = 0
    records = []
    while offset + 16 <= len(dec):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if magic != -1:
            break
        records.append((rid, l1, l2, l3, rlen, npcid, offset))
        offset += rlen
        
    print(f"Total parsed records: {len(records)}")
    for r in records[306:312]:
        rid, l1, l2, l3, rlen, npcid, roff = r
        cur = roff + 16
        n_len = dec[cur]; cur += 1
        npc = dec[cur:cur+n_len].decode('utf-16le', errors='ignore'); cur += n_len
        q_len = dec[cur]; cur += 1
        quest = dec[cur:cur+q_len].decode('utf-16le', errors='ignore'); cur += q_len
        
        s1 = dec[cur:cur+l1]; cur += l1
        s2 = dec[cur:cur+l2]; cur += l2
        s3 = dec[cur:cur+l3]; cur += l3
        
        print(f"RID {rid}: rlen={rlen}, l1={l1}, l2={l2}, l3={l3}")
        print(f"  s1: {s1[:6].hex()} | {repr(s1.decode('utf-16le', errors='ignore')[:30])}")
        print(f"  s2: {s2[:6].hex()} | {repr(s2.decode('utf-16le', errors='ignore')[:30])}")

if __name__ == "__main__":
    main()
