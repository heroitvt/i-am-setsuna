import json

def main():
    with open(r"d:\Viet Hoa Game\temp_scripts\normal_conv_all.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    nive_all = [r for r in data if 5265 <= r['rid'] <= 5387]
    print(f"Total Nive records: {len(nive_all)}")
    
    with open(r"d:\Viet Hoa Game\temp_scripts\nive_full_123.json", "w", encoding="utf-8") as f:
        json.dump(nive_all, f, ensure_ascii=False, indent=2)
    print("Exported to nive_full_123.json")

if __name__ == "__main__":
    main()
