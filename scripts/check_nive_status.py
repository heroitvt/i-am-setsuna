import json

def is_vietnamese(text):
    # check for common vietnamese diacritics
    vn_chars = "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
    return any(c in vn_chars for c in text.lower())

def main():
    with open(r"d:\Viet Hoa Game\temp_scripts\normal_conv_all.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    nive_records = [r for r in data if 5265 <= r['rid'] <= 5387]
    print(f"Total Nive Island records: {len(nive_records)}")
    
    vn_count = 0
    en_count = 0
    en_list = []
    for r in nive_records:
        txt = r['en']
        if is_vietnamese(txt):
            vn_count += 1
        else:
            en_count += 1
            en_list.append(r)
            
    print(f"Already Vietnamese: {vn_count}")
    print(f"Still English: {en_count}")
    
    # Save English lines to translate
    with open(r"d:\Viet Hoa Game\temp_scripts\nive_to_translate.json", "w", encoding="utf-8") as f:
        json.dump(en_list, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(en_list)} records to translate into nive_to_translate.json")

if __name__ == "__main__":
    main()
