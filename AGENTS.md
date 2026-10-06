# QUY TẮC PHÁT TRIỂN & VIỆT HÓA DỰ ÁN I AM SETSUNA (PROJECT RULES)

Tài liệu này là quy chuẩn kỹ thuật bắt buộc cho bất kỳ Agent / Lập trình viên nào làm việc trên dự án Việt Hóa *I am Setsuna*. Mọi tác vụ phải tuân thủ nghiêm ngặt để đảm bảo **làm 1 lần là thành công**, không gây lỗi màn hình đen và không làm hỏng game.

---

## 1. QUY TẮC QUẢN LÝ THƯ MỤC VÀ KHÔNG GIAN LÀM VIỆC
- **Không xả rác ra thư mục gốc:** Tuyệt đối KHÔNG tạo các file code Python, PowerShell, JSON tạm, dump text... tại thư mục gốc `d:\Viet Hoa Game\`.
- **Thư mục file tạm:** Tất cả 100% script can thiệp, tool trích xuất, file dump, file test bắt buộc phải nằm gọn trong:
  `d:\Viet Hoa Game\temp_scripts\`
- Luôn dọn dẹp các tiến trình nền bị treo (nếu có) trước khi hoàn tất công việc.

---

## 2. KIẾN TRÚC NẠP DỮ LIỆU CỦA GAME & NGUYÊN TẮC BẤT DI BẤT DỊCH
1. **Cơ chế nạp file thoại (DUAL-SOURCE ENGINE):**
   - Engine Unity của game đọc và nạp dữ liệu hội thoại từ **2 NGUỒN ĐỒNG THỜI**:
     1. **File rời bên ngoài:** `SETSUNA_Data\StreamingAssets\data\parameter\` (chứa các file mã hóa AES và `.dec` plaintext như `ScenarioMessageData_Chapter_1`, `ScenarioMessageData_NormalConversation`...).
     2. **Kho lưu trữ tổng của game:** `SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk` (Kích thước gốc an toàn bắt buộc: **13.291.792 bytes**).
   - **LƯU Ý CỰC KỲ QUAN TRỌNG:** Một số sự kiện cốt truyện và NPC cố định (như Raishin, Kind Woman, trưởng làng...) được Unity **ƯU TIÊN NẠP TRỰC TIẾP TỪ KHO `parameter.cpk`**. Nếu chỉ sửa file rời mà không patch vào `parameter.cpk`, game sẽ vẫn hiện text tiếng Anh gốc!
   - **BẮT BUỘC:** Mỗi khi cập nhật/sửa lỗi dịch thuật, phải đồng bộ in-place vào cả 2 nguồn: file rời và file `parameter.cpk`!
2. **NGHIÊM CẤM TÁI TẠO (REBUILD/REPACK) FILE CPK TỪ ĐẦU:**
   - Việc dùng script custom để đóng gói lại toàn bộ file CPK sẽ làm sai lệch cấu trúc bảng mục lục (TOC), sai lệch căn lề (Alignment) và chữ ký bảo mật ETOC của CRIWare.
   - **Hậu quả:** Game bị deadlock ngay tại logo khởi động $\rightarrow$ **MÀN HÌNH ĐEN**.
3. **PHƯƠNG PHÁP GHI ĐÈ TẠI CHỖ (IN-PLACE PATCHING - BẮT BUỘC DÙNG):**
   - Không rebuild CPK, mà chỉ ghi đè block dữ liệu trực tiếp vào đúng offset bên trong `parameter.cpk`:
     - `ScenarioMessageData_Chapter_1`: Offset **`9605120`**, kích thước đúng **`372.704 bytes`**.
   - **Quy trình chuẩn khi sửa text trong Chapter 1:**
     1. Mở `parameter.cpk` ở chế độ đọc/ghi nhị phân (`r+b`).
     2. Đọc đúng 372.704 bytes tại offset `9605120`.
     3. Giải mã AES-128-CBC (`Key = b"8xTD|EgD|b?07QDj"`, `IV = b"/]s@*CxLzM!9Qd%("`).
     4. Chỉnh sửa record mục tiêu (tính toán lại độ dài chuỗi UTF-16LE, nếu text ngắn hơn có thể đệm khoảng trắng cuối câu hoặc tính lại padding cuối file sao cho tổng kích thước giải mã đúng bằng 372.704 bytes).
     5. Mã hóa lại chuẩn AES-128-CBC.
     6. Ghi đè đúng 372.704 bytes vào offset `9605120`.
     7. Đảm bảo kích thước toàn file `parameter.cpk` sau khi sửa **vẫn đúng 13.291.792 bytes**.

---

## 3. QUY CHUẨN ĐỊNH DẠNG VĂN BẢN & GIAO DIỆN KHUNG THOẠI (UI)
1. **Giới hạn số dòng khung thoại (Tránh lỗi tràn viền cụt chữ):**
   - Khung thoại của game chỉ hiển thị đẹp và trọn vẹn trong **tối đa 2 dòng thoại**.
   - Nếu text dài thành 3 dòng, dòng thứ 3 sẽ bị đẩy xuống sát mép dưới và bị khung thoại che khuất (lỗi mất chữ như chữ *"sinh"*).
   - **Quy chuẩn ngắt dòng (`\n`):**
     - Dòng 1: $\le 28 - 30$ ký tự.
     - Dòng 2: $\le 28 - 30$ ký tự.
     - Chủ động chèn dấu ngắt dòng `\n` hợp lý, không để Unity tự động ngắt dòng tự do.
2. **Giới hạn byte an toàn của Engine:**
   - Mỗi trang thoại tiếng Việt sau khi encode UTF-16LE không được vượt quá **234 bytes** (ngưỡng an toàn tối đa của biến 1-byte trong engine game là 255 bytes).
3. **Bảo tồn nguyên vẹn thẻ đặc biệt:**
   - Các thẻ hệ thống như `<NAME=NPC_...>`, `<NAME=CP_...>`, thẻ phân trang `|` phải được giữ chính xác 100%, không được làm sai lệch cú pháp.
4. **Quy chuẩn đối với Menu Hệ thống & Tên riêng (SYSTEM & NAMING RULES):**
   - **Menu giao diện hệ thống KHÔNG CẦN DỊCH:** Các tùy chọn cài đặt (Settings), thông báo hệ thống kỹ thuật, cửa sổ phím bấm/điều khiển (`SetsunaSystemDataMessage`, phím bấm keyboard/gamepad...) giữ nguyên gốc tiếng Anh.
   - **"Tên riêng" vật phẩm, trang bị, nguyên liệu KHÔNG DỊCH:** Toàn bộ danh từ riêng, tên vũ khí, tên phụ kiện, tên nguyên liệu quái vật rơi, tên món ăn (`WeaponItemMessage`, `MaterialItemMessage`, `CookingItemMessage`...) giữ nguyên tiếng Anh gốc.
   - **Tên toàn bộ Quái vật, Boss & NPC KHÔNG CẦN DỊCH:** Toàn bộ tên quái vật, Boss (`EnemySetParameterMessage`, `BraveStoryMonsterMessage`) và tên/danh xưng NPC (`NPCSetParameterMessage`) giữ nguyên gốc tiếng Anh để người chơi dễ tra cứu wiki/hướng dẫn.
   - **Phần BẮT BUỘC DỊCH:** Cốt truyện chính (Chapters 1–4), Hội thoại tự do của NPC (Normal Conversation), Nhiệm vụ phụ (SubQuest), Mô tả công dụng trang bị/vật phẩm/kỹ năng, Hướng dẫn sử dụng, Công thức nấu ăn/chế tạo và Toàn bộ Thư viện truyền thuyết (Brave Story Lore).

---

## 4. HỆ THỐNG INJECTOR & ĐỒNG BỘ NGUỒN DỮ LIỆU
1. **Font & Bộ giải mã mở rộng:**
   - `SetsunaFontFix.dll` (nằm trong `SETSUNA_Data\Managed\`) được hook vào `Setsuna.GameManager.Awake` để nạp font động tiếng Việt (Georgia / Times New Roman).
2. **Nguyên tắc đồng bộ 3 lớp (Đảm bảo tính nhất quán):**
   Mỗi khi thay đổi bất kỳ câu thoại nào, phải đồng bộ đầy đủ cả 3 nơi:
   1. **File Master Excel:** `I_am_Setsuna-parameter-Steam.xlsx` (để lưu trữ và theo dõi tiến độ dịch).
   2. **File Loose:** `SETSUNA_Data\StreamingAssets\data\parameter\` (cả file `.dec` plaintext và file mã hóa AES).
   3. **Kho lưu trữ CPK:** `SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk` (In-place patch).

---

## 5. QUY TRÌNH KIỂM THỬ TRƯỚC KHI BÀN GIAO (CHECKLIST)
Trước khi thông báo hoàn tất cho người dùng, BẮT BUỘC phải chạy kiểm tra:
- [ ] File `parameter.cpk` có đúng kích thước $13.291.792$ bytes không?
- [ ] Chạy script `temp_scripts/test_launch.py` kiểm tra `SETSUNA.exe` có khởi động bình thường sau 3 giây không (không bị màn hình đen)?
- [ ] Đọc ngược dữ liệu từ CPK / file nhị phân để in ra text thực tế đã ghi, đảm bảo khớp 100% với yêu cầu của người dùng.

---

## 6. TIẾN ĐỘ DỰ ÁN & BÀN GIAO (CẬP NHẬT 04/10/2026)

### Tổng quan tiến độ: 10.579 / 10.831 dòng (97.67% - Hoàn tất 100% các phân mục theo quy chuẩn)
*(Còn lại 252 dòng thuộc Menu giao diện hệ thống & tùy chọn cài đặt giữ nguyên tiếng Anh theo đúng Rule của Anh).*

### Các phân mục ĐÃ HOÀN THÀNH 100%:
1. **Cốt truyện chính (Chapters 1, 2, 3, 4) & Toàn bộ Hội thoại NPC:**
   - `ScenarioMessageData_Chapter_1`: 1.403 dòng (100%).
   - `ScenarioMessageData_Chapter_2`: 1.713 dòng (100%).
   - `ScenarioMessageData_Chapter_3`: 1.344 dòng (100%).
   - `ScenarioMessageData_Chapter_4`: 805 dòng (100%).
   - `ScenarioMessageData_NormalConv`: 684 dòng (100%).
   - `SubQuestMessageData`: 21 dòng (100%).
2. **Hướng dẫn cách chơi & Hệ thống (`SystemMessage`):**
   - 11 bảng hướng dẫn cốt lõi (Xung Lực Momentum, Chiến Đấu ATB, Spritnite, Biến Chuyển Flux...).
3. **Kỹ năng & Nhân vật (Skills) & Pháp thạch (Materia):**
   - Kỹ năng 7 nhân vật chính, 133 Combos phối hợp, kỹ năng Boss & quái vật.
   - 218 loại Pháp thạch (`MateriaMessage`).
4. **Vật phẩm, Trang bị & Nguyên liệu (Nhóm 3):**
   - Giữ nguyên tên riêng tiếng Anh theo Rule.
   - Dịch 100% mô tả công dụng, công thức nấu ăn & hiệu ứng thuộc tính (`WeaponItemMessage`, `MaterialItemMessage`, `CookingItemMessage`, `EventItemMessage`, `SublimationDataMessage`).
5. **Thư viện / Lore (Brave Story) (1.389 dòng - 100%):**
   - Hoàn tất toàn bộ 12 Sheet truyền thuyết.
6. **Bộ cài & Cập nhật OTA:**
   - Hoàn thiện ứng dụng độc lập `Setsuna_VietHoa_Patcher.exe` kết nối GitHub OTA.

