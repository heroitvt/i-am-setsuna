from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def main():
    cpk_path = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    with open(cpk_path, "rb") as f:
        f.seek(9603072)
        raw = f.read(372704)
        
    c = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    dec = c.decryptor().update(raw)
    
    # Check first record in CPK
    magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[:16])
    print(f"Record 0 in CPK: rid={rid}, l1={l1}, l2={l2}, l3={l3}")
    
    # Check text of s2
    cur = 16 + 1 + dec[16] + 1 + dec[16+1+dec[16]]
    s1 = dec[cur:cur+l1]; cur += l1
    s2 = dec[cur:cur+l2]; cur += l2
    print("s2 raw in CPK:", s2.hex())
    print("s2 text in CPK:", repr(s2.decode('utf-16le', errors='ignore')))
    
    # Check record 1
    cur_off = rlen
    magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[cur_off:cur_off+16])
    print(f"Record 1 in CPK: rid={rid}, l1={l1}, l2={l2}, l3={l3}")
    cur = cur_off + 16 + 1 + dec[cur_off+16] + 1 + dec[cur_off+16+1+dec[cur_off+16]]
    s1 = dec[cur:cur+l1]; cur += l1
    s2 = dec[cur:cur+l2]; cur += l2
    print("s2 text in CPK (record 1):", repr(s2.decode('utf-16le', errors='ignore')))

if __name__ == "__main__":
    main()
