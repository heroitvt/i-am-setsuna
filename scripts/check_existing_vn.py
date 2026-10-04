import json

def is_vietnamese(text):
    vn_chars = "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
    return any(c in vn_chars for c in text.lower())

def main():
    with open(r"d:\Viet Hoa Game\temp_scripts\normal_conv_all.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    nive_records = [r for r in data if 5265 <= r['rid'] <= 5387]
    lines = []
    for r in nive_records:
        if is_vietnamese(r['en']):
            lines.append(f"RID {r['rid']} (NPC {r['npc']}):")
            lines.append(f"  VN: {repr(r['en'])}")
            lines.append(f"  JP: {repr(r['jp'])}")
            
    with open(r"d:\Viet Hoa Game\temp_scripts\existing_vn_out.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Saved to existing_vn_out.txt")

if __name__ == "__main__":
    main()
