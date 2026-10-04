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
    while offset + 16 <= len(dec):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if rid in (2458, 2610):
            cur = offset + 16
            cur += 1 + dec[cur]
            cur += 1 + dec[cur]
            cur += l1
            s2 = dec[cur:cur+l2]
            print(f"RID {rid}: l2={l2}, raw prefix={s2[:6].hex()}")
            for start in (1, 2, 3):
                try:
                    txt = s2[start:].decode('utf-16le')
                    safe = txt.encode('ascii', 'backslashreplace').decode('ascii')
                    print(f"  start={start}, len={len(txt)}: {repr(safe[:40])}")
                except Exception as e:
                    print(f"  start={start} failed: {e}")
        offset += rlen

if __name__ == "__main__":
    main()
