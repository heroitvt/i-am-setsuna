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
    for r in range(16):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if r == 15:
            print(f"Record 15: offset={offset}, magic={magic}, rid={rid}, l1={l1}, l2={l2}, l3={l3}, rlen={rlen}, npcid={npcid}")
            rdata = dec[offset:offset+rlen]
            for i in range(0, len(rdata), 16):
                chunk = rdata[i:i+16]
                hex_str = " ".join(f"{b:02x}" for b in chunk)
                ascii_str = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
                print(f"{i:04x}: {hex_str:<48} | {ascii_str}")
        offset += rlen

if __name__ == "__main__":
    main()
