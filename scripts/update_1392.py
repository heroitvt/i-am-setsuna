import openpyxl
import json
import re

def main():
    txt = "Cô ấy đã hứng trọn luồng sức mạnh pháp thạch ở cự ly gần...\nNó đang làm tổn hại đến cơ thể cô ấy..."
    excel_path = r"d:\Viet Hoa Game\I_am_Setsuna-parameter-Steam.xlsx"
    wb = openpyxl.load_workbook(excel_path)
    ws = wb["ScenarioMessageData_Chapter_1"]
    ws.cell(1395, 3).value = txt
    wb.save(excel_path)
    
    json_path = r"d:\Viet Hoa Game\translation_export\ScenarioMessageData_Chapter_1.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        if '"Id":1392' in item.get("id", ""):
            item["vietnamese"] = txt
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Updated RID 1392 successfully!")

if __name__ == "__main__":
    main()
