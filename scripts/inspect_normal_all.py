from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct

KEY = b"8xTD|EgD|b?07QDj"
IV = b"/]s@*CxLzM!9Qd%("

def main():
    p = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter\ScenarioMessageData_NormalConversation"
    with open(p, "rb") as f:
        d = f.read()
    c = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    dec = c.decryptor().update(d)
    
    offset = 0
    records = []
    while offset + 16 <= len(dec):
        mtype, rid, l1, l2, l3, rlen, npcid = struct.unpack("<ihhhhHh", dec[offset:offset+16])
        if rlen == 0 or rlen > 5000:
            break
        cur = offset + 16
        n_len = dec[cur]; cur += 1
        npc = dec[cur:cur+n_len].decode('utf-16le', errors='ignore'); cur += n_len
        q_len = dec[cur]; cur += 1
        quest = dec[cur:cur+q_len].decode('utf-16le', errors='ignore'); cur += q_len
        
        s1 = dec[cur:cur+l1]; cur += l1
        s2 = dec[cur:cur+l2]; cur += l2
        s3 = dec[cur:cur+l3]; cur += l3
        
        # parse s2
        pages = []
        if len(s2) > 0:
            num_p = s2[0]
            c_p = 1
            for _ in range(num_p):
                plen = s2[c_p]; c_p += 1
                pages.append(s2[c_p:c_p+plen].decode('utf-16le', errors='ignore'))
                c_p += plen
        txt = "\n|\n".join(pages)
        records.append({
            'rid': rid,
            'npc': npc,
            'quest': quest,
            's2': txt,
            'l1': l1,
            'l2': l2,
            'l3': l3,
            'rlen': rlen
        })
        offset += rlen
        
    print(f"Total records in NormalConversation: {len(records)}")
    print(f"RID range: {records[0]['rid']} to {records[-1]['rid']}")
    
    # Save a summary of NPCs and their RID ranges
    npc_groups = {}
    for r in records:
        npc = r['npc']
        if npc not in npc_groups:
            npc_groups[npc] = []
        npc_groups[npc].append(r)
        
    print(f"Total unique NPCs: {len(npc_groups)}")
    for npc, rlist in list(npc_groups.items())[:25]:
        sample = rlist[0]['s2'].replace('\n', ' ')[:50]
        print(f"NPC {npc:<15} ({len(rlist)} lines, RIDs {rlist[0]['rid']}..{rlist[-1]['rid']}): {sample}")

if __name__ == "__main__":
    main()
