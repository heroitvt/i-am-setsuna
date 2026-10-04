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
    records = []
    while offset + 16 <= len(dec):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if magic != -1:
            break
        records.append((rid, l1, l2, l3, rlen, npcid, offset))
        offset += rlen
        
    print(f"Parsed {len(records)} records.")
    print(f"Final offset: {offset} / total file len: {len(dec)} (padding: {len(dec) - offset} bytes)")
    print(f"Last record ID: {records[-1][0]}")

if __name__ == "__main__":
    main()
