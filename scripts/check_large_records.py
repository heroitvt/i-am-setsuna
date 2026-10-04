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
    large_records = []
    while offset + 16 <= len(dec):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if l1 > 250 or l2 > 250 or l3 > 250:
            large_records.append((rid, l1, l2, l3, rlen, offset))
        offset += rlen
        
    print(f"Total large records: {len(large_records)}")
    for r in large_records[:5]:
        rid, l1, l2, l3, rlen, roff = r
        print(f"Record {rid}: l1={l1}, l2={l2}, l3={l3}")
        cur = roff + 16
        cur += 1 + dec[cur] # npc
        cur += 1 + dec[cur] # quest
        s1_raw = dec[cur:cur+l1]; cur += l1
        s2_raw = dec[cur:cur+l2]; cur += l2
        print(f"  s1 prefix bytes: {s1_raw[:4].hex()}")
        print(f"  s2 prefix bytes: {s2_raw[:4].hex()}")

if __name__ == "__main__":
    main()
