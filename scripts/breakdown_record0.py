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
    
    r0 = dec[:160]
    magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", r0[:16])
    lines = []
    lines.append(f"magic: {hex(magic)}, rid: {rid}, l1: {l1}, l2: {l2}, l3: {l3}, rlen: {rlen}, npcid: {npcid}")
    
    cur = 16
    npc_len = r0[cur]; cur += 1
    npc = r0[cur:cur+npc_len].decode('utf-16le', errors='ignore'); cur += npc_len
    lines.append(f"npc_len: {npc_len}, npc: {repr(npc)}")
    
    quest_len = r0[cur]; cur += 1
    quest = r0[cur:cur+quest_len].decode('utf-16le', errors='ignore'); cur += quest_len
    lines.append(f"quest_len: {quest_len}, quest: {repr(quest)}")
    
    # String 1
    s1_pre = r0[cur]; cur += 1
    s1_bytes = r0[cur:cur+l1]
    s1 = s1_bytes.decode('utf-16le', errors='ignore')
    cur += l1
    lines.append(f"s1_pre: {s1_pre}, s1 len: {len(s1_bytes)} ({l1}), s1: {repr(s1)}")
    
    # String 2
    s2_pre = r0[cur]; cur += 1
    s2_bytes = r0[cur:cur+l2]
    s2 = s2_bytes.decode('utf-16le', errors='ignore')
    cur += l2
    lines.append(f"s2_pre: {s2_pre}, s2 len: {len(s2_bytes)} ({l2}), s2: {repr(s2)}")
    
    # String 3
    s3_pre = r0[cur]; cur += 1
    s3_bytes = r0[cur:cur+l3]
    s3 = s3_bytes.decode('utf-16le', errors='ignore')
    cur += l3
    lines.append(f"s3_pre: {s3_pre}, s3 len: {len(s3_bytes)} ({l3}), s3: {repr(s3)}")
    
    lines.append(f"Consumed {cur} bytes out of rlen={rlen}. Remaining: {rlen - cur} bytes: {r0[cur:]}")
    
    with open(r"d:\Viet Hoa Game\temp_scripts\record0_output.txt", "w", encoding="utf-8") as out:
        out.write("\n".join(lines))
    print("Done! Check record0_output.txt")

if __name__ == "__main__":
    main()
