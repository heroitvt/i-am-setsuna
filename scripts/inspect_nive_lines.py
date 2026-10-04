import json

def main():
    with open(r"d:\Viet Hoa Game\temp_scripts\nive_to_translate.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    lines = []
    lines.append(f"Total lines to translate: {len(data)}")
    for i, r in enumerate(data):
        lines.append(f"\n[{i+1}] RID {r['rid']} (NPC {r['npc']}):")
        lines.append(f"  EN: {repr(r['en'])}")
        lines.append(f"  JP: {repr(r['jp'])}")
        
    with open(r"d:\Viet Hoa Game\temp_scripts\nive_lines_out.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Saved to nive_lines_out.txt")

if __name__ == "__main__":
    main()
