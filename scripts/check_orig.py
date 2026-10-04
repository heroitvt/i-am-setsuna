def main():
    p = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter_backup_before_MASTER_FINAL\ScenarioMessageData_Chapter_1.bak_original"
    with open(p, "rb") as f:
        d = f.read(64)
    print("bak_original first 64 bytes:", d)

if __name__ == "__main__":
    main()
