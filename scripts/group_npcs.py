import json

def main():
    with open(r"d:\Viet Hoa Game\temp_scripts\normal_conv_all.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Group by NPC prefix:
    # In Setsuna:
    # NPC_21xxx = Port of Nive (ma_0001)
    # NPC_22xxx = Village of Nive (ma_0002)
    # NPC_10010 = Raishin (Village of Nive)
    # Let's see what other NPC prefixes exist
    by_prefix = {}
    for r in data:
        npc = r['npc']
        pref = npc[:6] if len(npc) >= 6 else npc
        if pref not in by_prefix:
            by_prefix[pref] = []
        by_prefix[pref].append(r)
        
    print("NPC Groups:")
    for pref, rlist in sorted(by_prefix.items()):
        print(f"Prefix {pref:<10}: {len(rlist)} records, RIDs {rlist[0]['rid']}..{rlist[-1]['rid']}")

if __name__ == "__main__":
    main()
