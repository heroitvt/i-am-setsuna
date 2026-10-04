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
    
    lines = []
    lines.append(f"Chapter 2 decrypted len: {len(dec)}")
    for r in range(5):
        magic, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[:16])
        lines.append(f"\n--- Chapter 2 Record {r}: rid={rid}, l1={l1}, l2={l2}, l3={l3}, rlen={rlen}, npcid={npcid} ---")
        cur = 16
        npc_len = dec[cur]; cur += 1
        npc = dec[cur:cur+npc_len]; cur += npc_len
        q_len = dec[cur]; cur += 1
        quest = dec[cur:cur+q_len]; cur += q_len
        
        s1 = dec[cur:cur+l1]; cur += l1
        s2 = dec[cur:cur+l2]; cur += l2
        s3 = dec[cur:cur+l3]; cur += l3
        
        lines.append(f"npc ({npc_len}): {npc.decode('utf-16le', errors='ignore')}")
        lines.append(f"quest ({q_len}): {quest.decode('utf-16le', errors='ignore')}")
        lines.append(f"s1 ({l1}): hex={s1[:10].hex()} | text={repr(s1.decode('utf-16le', errors='ignore'))}")
        lines.append(f"s2 ({l2}): hex={s2[:10].hex()} | text={repr(s2.decode('utf-16le', errors='ignore'))}")
        lines.append(f"s3 ({l3}): hex={s3[:10].hex()} | text={repr(s3.decode('utf-16le', errors='ignore'))}")
        lines.append(f"rlen={rlen}, consumed={cur}, diff={rlen-cur}")
        dec = dec[rlen:]
        
    with open(r"d:\Viet Hoa Game\temp_scripts\ch2_output.txt", "w", encoding="utf-8") as out:
        out.write("\n".join(lines))
    print("Saved to ch2_output.txt")

if __name__ == "__main__":
    main()
