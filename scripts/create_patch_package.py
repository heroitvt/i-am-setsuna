import os
import zipfile
import shutil

def main():
    game_dir = r"D:\Viet Hoa Game\I am Setsuna"
    patch_folder = r"D:\Viet Hoa Game\Setsuna_VietHoa_Patch"
    zip_output = r"D:\Viet Hoa Game\Setsuna_VietHoa_Patch.zip"

    if os.path.exists(patch_folder):
        shutil.rmtree(patch_folder)

    # 1. Managed files
    managed_dst = os.path.join(patch_folder, "SETSUNA_Data", "Managed")
    os.makedirs(managed_dst, exist_ok=True)
    shutil.copy2(os.path.join(game_dir, "SETSUNA_Data", "Managed", "Assembly-CSharp.dll"), managed_dst)
    shutil.copy2(os.path.join(game_dir, "SETSUNA_Data", "Managed", "SetsunaFontFix.dll"), managed_dst)

    # 2. Parameter files to include
    param_dst = os.path.join(patch_folder, "SETSUNA_Data", "StreamingAssets", "data", "parameter")
    os.makedirs(param_dst, exist_ok=True)

    param_files = [
        "ScenarioMessageData_Chapter_1",
        "ScenarioMessageData_Chapter_1.dec",
        "ScenarioMessageData_NormalConversation",
        "ScenarioMessageData_NormalConversation.dec",
        "SystemMessage",
        "SystemMessage.dec",
        "PlayerSkillDataMessage",
        "PlayerSkillDataMessage.dec",
        "SetsunaSkillDataMessage",
        "SetsunaSkillDataMessage.dec",
        "TsukushiSkillDataMessage",
        "TsukushiSkillDataMessage.dec",
        "YomiSkillDataMessage",
        "YomiSkillDataMessage.dec",
        "KishilSkillDataMessage",
        "KishilSkillDataMessage.dec",
        "SionSkillDataMessage",
        "SionSkillDataMessage.dec",
        "GrimreaperSkillDataMessage",
        "GrimreaperSkillDataMessage.dec",
        "TwoPlayerCoopSkillDataMessage",
        "TwoPlayerCoopSkillDataMessage.dec",
        "ThreePlayerCoopSkillDataMessage",
        "ThreePlayerCoopSkillDataMessage.dec",
        "EnemySkillDataMessage",
        "EnemySkillDataMessage.dec",
        "EnemyBossSkillDataMessage",
        "EnemyCoopSkillDataMessage",
        "EnemyCoopSkillDataMessage.dec",
        "ItemSkillDataMessage",
        "ItemSkillDataMessage.dec",
        "MateriaMessage",
        "MateriaMessage.dec"
    ]

    for pf in param_files:
        src = os.path.join(game_dir, "SETSUNA_Data", "StreamingAssets", "data", "parameter", pf)
        if os.path.exists(src):
            shutil.copy2(src, param_dst)

    # 3. CPK file
    cpk_dst = os.path.join(patch_folder, "SETSUNA_Data", "StreamingAssets", "x86_64")
    os.makedirs(cpk_dst, exist_ok=True)
    shutil.copy2(os.path.join(game_dir, "SETSUNA_Data", "StreamingAssets", "x86_64", "parameter.cpk"), cpk_dst)

    # 4. Create Readme
    readme_path = os.path.join(patch_folder, "Huong_Dan_Cai_Dat.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("=== HƯỚNG DẪN CÀI ĐẶT PATCH VIỆT HÓA I AM SETSUNA ===\n\n"
                "1. Copy toàn bộ thư mục 'SETSUNA_Data' trong gói này.\n"
                "2. Dán đè (Paste & Replace) vào thư mục cài đặt game I am Setsuna trên máy của bạn.\n"
                "3. Khởi động game bằng SETSUNA.exe và trải nghiệm!\n")

    # 5. Zip it
    with zipfile.ZipFile(zip_output, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(patch_folder):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, patch_folder)
                zipf.write(abs_path, rel_path)

    zip_size_mb = os.path.getsize(zip_output) / (1024 * 1024)
    print(f"Created patch folder: {patch_folder}")
    print(f"Created standalone patch zip: {zip_output} ({zip_size_mb:.2f} MB)")

if __name__ == "__main__":
    main()
