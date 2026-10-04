# i-am-setsuna

Dự án Việt Hóa game **I am Setsuna** (PC / Steam).

## 1. Cấu trúc thư mục
- `I_am_Setsuna-parameter-Steam.xlsx`: Master Excel chứa toàn bộ text gốc và bản dịch tiếng Việt của toàn bộ game.
- `AGENTS.md`: Tài liệu kỹ thuật chi tiết về cấu trúc mã hóa AES, địa chỉ offset nhị phân và quy chuẩn khung thoại.
- `scripts/`: Toàn bộ các công cụ Python & C# phục vụ:
  - Trích xuất và giải mã dữ liệu (`.dec`, AES-128-CBC).
  - Quét kiểm tra lỗi hiển thị vượt khung thoại in-game.
  - In-place patch nhị phân vào `parameter.cpk` giữ nguyên $13.291.792$ bytes.
  - Hook font Unicode và nạp dữ liệu runtime qua `SetsunaFontFix.dll`.
- `patch_files/`: Toàn bộ các file patch đầu ra đã được đóng gói sẵn sàng đưa vào game.

## 2. Thông số kỹ thuật
- **AES Key:** `8xTD|EgD|b?07QDj` (16 bytes)
- **AES IV:** `/]s@*CxLzM!9Qd%(` (16 bytes)
- **Font Hook:** `SETSUNA_Data/Managed/SetsunaFontFix.dll`
- **Engine:** Unity x86_64
