from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def decrypt_file(p):
    with open(p, "rb") as f:
        d = f.read()
    c = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    dec = c.decryptor().update(d)
    return dec

def main():
    p = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter\ScenarioMessageData_NormalConversation"
    dec = decrypt_file(p)
    
    offset = 0
    lines = []
    for r in range(30):
        if offset + 16 > len(dec):
            break
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        cur = offset + 16
        n_len = dec[cur]; cur += 1
        npc = dec[cur:cur+n_len].decode('utf-16le', errors='ignore'); cur += n_len
        q_len = dec[cur]; cur += 1
        quest = dec[cur:cur+q_len].decode('utf-16le', errors='ignore'); cur += q_len
        
        s1 = dec[cur:cur+l1]; cur += l1
        s2 = dec[cur:cur+l2]; cur += l2
        s3 = dec[cur:cur+l3]; cur += l3
        
        if len(s2) > 0:
            num_pages = s2[0]
            txt = ""
            c_p = 1
            for _ in range(num_pages):
                plen = s2[c_p]; c_p += 1
                txt += s2[c_p:c_p+plen].decode('utf-16le', errors='ignore') + " "
                c_p += plen
        else:
            txt = ""
            
        lines.append(f"RID {rid} (NPC {npc}): {txt.strip()}")
        offset += rlen
        
    with open(r"d:\Viet Hoa Game\temp_scripts\normal_conv_out.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Done!")

if __name__ == "__main__":
    main()
