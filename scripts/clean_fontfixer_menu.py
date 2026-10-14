import os

fontfixer_path = r"D:\i-am-setsuna\scripts\FontFixer.cs"
with open(fontfixer_path, "r", encoding="utf-8") as f:
    code = f.read()

fields_start = code.find("        private static float fontScale = -1f;")
assert fields_start != -1

new_fields = """        private static float fontScale = -1f;
        private static bool userAdjustedScale = false;
        private static Dictionary<int, int> originalFontSizes = new Dictionary<int, int>();

        private static MethodInfo mAddMoney = null;
        private static MethodInfo mSetMoney = null;
        private static MethodInfo mGetMoney = null;
        private static bool moneyMethodsResolved = false;

        // Clean Safe Menu & Input state
        private static bool menuOpen = false;
        private static float holdTimer = 0f;
        private static string notificationText = "";
        private static float notificationTimer = 0f;

        // D-Pad debounce while menu is open
        private static bool prevMenuUp = false;
        private static bool prevMenuDown = false;
        private static bool prevMenuLeft = false;
        private static bool prevMenuRight = false;
"""

apply_start = code.find("        public static void ApplyFontAndLayoutToVietnameseText(")
assert apply_start != -1

code_top = code[:fields_start] + new_fields + code[fields_start:apply_start]

# Clean up redundant old fields in code_top
code_top = code_top.replace(
    'ShowNotification("VIỆT HÓA SETSUNA | [F1] hoặc [L3+R3] Bật Hướng Dẫn | Gamepad: Giữ [L1+R1] + D-Pad");',
    'ShowNotification("VIỆT HÓA SETSUNA | Chạm [⚙ Menu] hoặc Giữ [L1+R1+Select] 1.5s để chỉnh Cỡ Chữ & Cheat");'
)

# Remove the old fields block from code_top
old_block_end = code_top.find("        private static string notificationText = \"\";\n        private static float notificationTimer = 0f;\n", fields_start + len(new_fields))
if old_block_end != -1:
    old_block_end += len("        private static string notificationText = \"\";\n        private static float notificationTimer = 0f;\n")
    code_top = code_top[:fields_start + len(new_fields)] + code_top[old_block_end:]

final_methods = """        public static void ApplyFontAndLayoutToVietnameseText(bool forceRefresh = false)
        {
            Font font = GetCustomFont();
            if ((object)font == null) return;

            // Auto-determine base font scale for resolution if not adjusted by player
            if (!userAdjustedScale)
            {
                if (Screen.height >= 1400) fontScale = 1.35f;
                else if (Screen.height >= 1000) fontScale = 1.25f; // +25% cho 1080p to rõ nét
                else fontScale = 1.15f;
            }

            Text[] texts = UnityEngine.Object.FindObjectsOfType<Text>();
            if (texts == null) return;

            for (int i = 0; i < texts.Length; i++)
            {
                Text t = texts[i];
                if ((object)t == null) continue;

                string txt = t.text;
                bool isVn = IsVietnamese(txt) || (object)t.font == (object)font;
                if (!isVn) continue;

                if ((object)t.font != (object)font)
                {
                    t.font = font;
                }

                // Dynamic Multi-Resolution Adaptation:
                t.horizontalOverflow = HorizontalWrapMode.Wrap;
                t.verticalOverflow = VerticalWrapMode.Overflow;

                if (t.lineSpacing > 0.92f || t.lineSpacing < 0.88f)
                {
                    t.lineSpacing = 0.90f;
                }

                // Scaling Font Size
                int id = t.GetInstanceID();
                int baseSize;
                if (!originalFontSizes.TryGetValue(id, out baseSize) || forceRefresh)
                {
                    if (!originalFontSizes.TryGetValue(id, out baseSize))
                    {
                        baseSize = t.fontSize;
                        if (baseSize <= 0) baseSize = 20;
                        originalFontSizes[id] = baseSize;
                    }
                }

                int targetSize = Mathf.RoundToInt(baseSize * fontScale);
                if (t.fontSize != targetSize)
                {
                    t.fontSize = targetSize;
                }
            }
        }

        // ==========================================
        // CHEAT & HOTKEY HANDLERS
        // ==========================================

        private static void ResolveMoneyMethods()
        {
            if (moneyMethodsResolved) return;
            moneyMethodsResolved = true;
            try
            {
                Type commonType = Type.GetType("Setsuna.Common, Assembly-CSharp");
                if (commonType != null)
                {
                    mAddMoney = commonType.GetMethod("AddMoney", BindingFlags.Public | BindingFlags.Static);
                    mSetMoney = commonType.GetMethod("SetMoney", BindingFlags.Public | BindingFlags.Static);
                    mGetMoney = commonType.GetMethod("GetMoney", BindingFlags.Public | BindingFlags.Static);
                }
            }
            catch (Exception ex)
            {
                Debug.LogError("[SetsunaFontFix] Failed to resolve money methods: " + ex.Message);
            }
        }

        public static uint GetCurrentMoney()
        {
            ResolveMoneyMethods();
            if (mGetMoney != null)
            {
                try
                {
                    return (uint)mGetMoney.Invoke(null, null);
                }
                catch { }
            }
            return 0;
        }

        public static void AddMoneyCheat(uint amount)
        {
            ResolveMoneyMethods();
            if (mAddMoney != null)
            {
                try
                {
                    mAddMoney.Invoke(null, new object[] { amount });
                    uint current = GetCurrentMoney();
                    ShowNotification(string.Format("CHEAT TIỀN: +{0:N0} VÀNG! HIỆN CÓ: {1:N0} G", amount, current));
                    Debug.Log(string.Format("[SetsunaFontFix] Cheat: Added {0} gold. Current: {1}", amount, current));
                }
                catch (Exception ex)
                {
                    ShowNotification("VUI LÒNG TẢI FILE SAVE TRƯỚC KHI DÙNG CHEAT!");
                    Debug.LogWarning("[SetsunaFontFix] AddMoney error: " + ex.Message);
                }
            }
            else
            {
                ShowNotification("KHÔNG TÌM THẤY HÀM XỬ LÝ TIỀN CỦA GAME!");
            }
        }

        public static void SetMaxMoneyCheat()
        {
            ResolveMoneyMethods();
            if (mSetMoney != null)
            {
                try
                {
                    mSetMoney.Invoke(null, new object[] { (uint)99999999 });
                    ShowNotification("CHEAT TIỀN: ĐÃ TỐI ĐA 99.999.999 VÀNG!");
                    Debug.Log("[SetsunaFontFix] Cheat: Set money to MAX 99999999.");
                }
                catch (Exception ex)
                {
                    ShowNotification("VUI LÒNG TẢI FILE SAVE TRƯỚC KHI DÙNG CHEAT!");
                    Debug.LogWarning("[SetsunaFontFix] SetMaxMoney error: " + ex.Message);
                }
            }
            else
            {
                ShowNotification("KHÔNG TÌM THẤY HÀM XỬ LÝ TIỀN CỦA GAME!");
            }
        }

        public static void ShowNotification(string text)
        {
            notificationText = text;
            notificationTimer = 3.5f;
        }

        private static bool SafeGetButton(string name)
        {
            try { return Input.GetButton(name); } catch { return false; }
        }

        private static bool SafeGetButtonDown(string name)
        {
            try { return Input.GetButtonDown(name); } catch { return false; }
        }

        private static float SafeGetAxis(string name)
        {
            try { return Input.GetAxisRaw(name); } catch { return 0f; }
        }

        private void HandleKeyInputs()
        {
            // ========================================================
            // 1. GAMEPAD ACTIVATION (HOLD L1+R1+SELECT FOR 1.5 SECONDS)
            // ========================================================
            // ZERO GHOST PRESSES: Completely avoids raw JoystickButton!
            // Only checks the game's native Input axes and requires 1.5s intentional hold.
            bool holdCombo = (SafeGetButton("LeftShoulder") && SafeGetButton("RightShoulder") && SafeGetButton("Select"))
                          || (SafeGetButton("LeftShoulder2") && SafeGetButton("RightShoulder2") && SafeGetButton("Select"));

            if (holdCombo)
            {
                holdTimer += Time.deltaTime;
                if (holdTimer >= 1.5f)
                {
                    holdTimer = 0f;
                    menuOpen = !menuOpen;
                    ShowNotification(menuOpen ? "ĐÃ MỞ BẢNG ĐIỀU KHIỂN & CHEAT" : "ĐÃ ĐÓNG BẢNG ĐIỀU KHIỂN");
                }
            }
            else
            {
                holdTimer = 0f;
            }

            // ========================================================
            // 2. KEYBOARD SHORTCUTS (PC)
            // ========================================================
            if (Input.GetKeyDown(KeyCode.F1))
            {
                menuOpen = !menuOpen;
            }

            if (Input.GetKeyDown(KeyCode.F6))
            {
                userAdjustedScale = true;
                fontScale = Mathf.Max(0.80f, fontScale - 0.05f);
                ApplyFontAndLayoutToVietnameseText(true);
                ShowNotification(string.Format("CỠ CHỮ: {0}% (MẶC ĐỊNH: 125%)", Mathf.RoundToInt(fontScale * 100f)));
            }

            if (Input.GetKeyDown(KeyCode.F7))
            {
                userAdjustedScale = true;
                fontScale = Mathf.Min(2.00f, fontScale + 0.05f);
                ApplyFontAndLayoutToVietnameseText(true);
                ShowNotification(string.Format("CỠ CHỮ: {0}% (MẶC ĐỊNH: 125%)", Mathf.RoundToInt(fontScale * 100f)));
            }

            if (Input.GetKeyDown(KeyCode.F8))
            {
                AddMoneyCheat(500000);
            }

            if (Input.GetKeyDown(KeyCode.F9))
            {
                SetMaxMoneyCheat();
            }

            // ========================================================
            // 3. GAMEPAD CONTROLS ONLY WHILE MENU IS OPEN
            // ========================================================
            if (menuOpen)
            {
                float padY = SafeGetAxis("PadVertical");
                float padX = SafeGetAxis("PadHorizontal");

                bool curUp = padY > 0.5f;
                bool curDown = padY < -0.5f;
                bool curLeft = padX < -0.5f;
                bool curRight = padX > 0.5f;

                if (curUp && !prevMenuUp)
                {
                    userAdjustedScale = true;
                    fontScale = Mathf.Min(2.00f, fontScale + 0.05f);
                    ApplyFontAndLayoutToVietnameseText(true);
                }
                else if (curDown && !prevMenuDown)
                {
                    userAdjustedScale = true;
                    fontScale = Mathf.Max(0.80f, fontScale - 0.05f);
                    ApplyFontAndLayoutToVietnameseText(true);
                }
                else if (curLeft && !prevMenuLeft)
                {
                    AddMoneyCheat(500000);
                }
                else if (curRight && !prevMenuRight)
                {
                    SetMaxMoneyCheat();
                }

                prevMenuUp = curUp;
                prevMenuDown = curDown;
                prevMenuLeft = curLeft;
                prevMenuRight = curRight;

                // Close menu with Circle / B / Start / Escape
                if (SafeGetButtonDown("Circle") || SafeGetButtonDown("Start") || Input.GetKeyDown(KeyCode.Escape))
                {
                    menuOpen = false;
                }
            }
        }

        private void OnGUI()
        {
            int screenW = Screen.width;
            int screenH = Screen.height;

            // 1. Toast Notification Bar
            if (notificationTimer > 0f)
            {
                notificationTimer -= Time.deltaTime;
                int boxW = Mathf.Min(780, screenW - 40);
                int boxH = 46;
                int boxX = (screenW - boxW) / 2;
                int boxY = 20;

                GUI.color = new Color(0f, 0f, 0f, 0.85f);
                GUI.Box(new Rect(boxX - 2, boxY - 2, boxW + 4, boxH + 4), "");
                GUI.color = new Color(0.10f, 0.35f, 0.70f, 0.95f);
                GUI.Box(new Rect(boxX, boxY, boxW, boxH), "");

                GUIStyle style = new GUIStyle();
                style.alignment = TextAnchor.MiddleCenter;
                style.fontSize = Mathf.Clamp(Mathf.RoundToInt(screenH * 0.022f), 14, 22);
                style.fontStyle = FontStyle.Bold;
                style.normal.textColor = Color.yellow;

                GUI.color = Color.white;
                GUI.Label(new Rect(boxX, boxY, boxW, boxH), notificationText, style);
            }

            // 2. ROG Ally Touch / Quick Button at Top-Right Corner
            int btnW = 150;
            int btnH = 36;
            int btnX = screenW - btnW - 16;
            int btnY = 16;

            GUI.color = new Color(0.12f, 0.40f, 0.85f, 0.85f);
            if (GUI.Button(new Rect(btnX, btnY, btnW, btnH), menuOpen ? "✕ Đóng Menu" : "⚙ Menu Tiện Ích"))
            {
                menuOpen = !menuOpen;
            }

            // 3. Full Config & Cheat Modal Panel (Touch Friendly & Gamepad Navigable)
            if (menuOpen)
            {
                int panelW = Mathf.Min(560, screenW - 40);
                int panelH = 340;
                int panelX = (screenW - panelW) / 2;
                int panelY = (screenH - panelH) / 2;

                // Dim Background
                GUI.color = new Color(0f, 0f, 0f, 0.65f);
                GUI.DrawTexture(new Rect(0, 0, screenW, screenH), Texture2D.whiteTexture);

                // Modal Box
                GUI.color = new Color(0.08f, 0.12f, 0.18f, 0.98f);
                GUI.Box(new Rect(panelX, panelY, panelW, panelH), "");
                GUI.color = new Color(0.18f, 0.50f, 0.92f, 1f);
                GUI.Box(new Rect(panelX + 2, panelY + 2, panelW - 4, 40), "");

                // Header Title
                GUIStyle titleStyle = new GUIStyle();
                titleStyle.alignment = TextAnchor.MiddleCenter;
                titleStyle.fontSize = 17;
                titleStyle.fontStyle = FontStyle.Bold;
                titleStyle.normal.textColor = Color.white;
                GUI.color = Color.white;
                GUI.Label(new Rect(panelX, panelY + 4, panelW, 36), "CẤU HÌNH VIỆT HÓA & CHEAT SETSUNA", titleStyle);

                // Subtitle Info
                uint curGold = GetCurrentMoney();
                int curScalePercent = Mathf.RoundToInt((fontScale < 0 ? 1.25f : fontScale) * 100f);
                GUIStyle infoStyle = new GUIStyle();
                infoStyle.alignment = TextAnchor.MiddleCenter;
                infoStyle.fontSize = 14;
                infoStyle.fontStyle = FontStyle.Bold;
                infoStyle.normal.textColor = new Color(0.95f, 0.85f, 0.30f);
                GUI.Label(new Rect(panelX, panelY + 50, panelW, 26), 
                    string.Format("Cỡ chữ: {0}% | Tiền vàng: {1:N0} G", curScalePercent, curGold), infoStyle);

                // Section 1: Font Size Controls
                int row1Y = panelY + 85;
                GUI.Label(new Rect(panelX + 20, row1Y, panelW - 40, 22), "1. CỠ CHỮ HỘI THOẠI (1080p / 2K / 4K):");

                int bW = (panelW - 60) / 3;
                if (GUI.Button(new Rect(panelX + 20, row1Y + 24, bW, 44), "[-] Giảm 5%\\n(D-Pad Xuống / F6)"))
                {
                    userAdjustedScale = true;
                    fontScale = Mathf.Max(0.80f, fontScale - 0.05f);
                    ApplyFontAndLayoutToVietnameseText(true);
                }
                if (GUI.Button(new Rect(panelX + 20 + bW + 10, row1Y + 24, bW, 44), "[+] Tăng 5%\\n(D-Pad Lên / F7)"))
                {
                    userAdjustedScale = true;
                    fontScale = Mathf.Min(2.00f, fontScale + 0.05f);
                    ApplyFontAndLayoutToVietnameseText(true);
                }
                if (GUI.Button(new Rect(panelX + 20 + (bW + 10) * 2, row1Y + 24, bW, 44), "Mặc Định\\n(125%)"))
                {
                    userAdjustedScale = true;
                    fontScale = 1.25f;
                    ApplyFontAndLayoutToVietnameseText(true);
                }

                // Section 2: Gold Cheat Controls
                int row2Y = row1Y + 80;
                GUI.Label(new Rect(panelX + 20, row2Y, panelW - 40, 22), "2. CHEAT TIỀN VÀNG (GOLD):");

                int bW2 = (panelW - 50) / 2;
                if (GUI.Button(new Rect(panelX + 20, row2Y + 24, bW2, 44), "+500.000 Vàng\\n(D-Pad Trái / F8)"))
                {
                    AddMoneyCheat(500000);
                }
                if (GUI.Button(new Rect(panelX + 20 + bW2 + 10, row2Y + 24, bW2, 44), "Tối Đa 99.999.999 Vàng\\n(D-Pad Phải / F9)"))
                {
                    SetMaxMoneyCheat();
                }

                // Section 3: Close Button & Shortcut Tips
                int row3Y = row2Y + 80;
                GUIStyle tipStyle = new GUIStyle();
                tipStyle.alignment = TextAnchor.MiddleCenter;
                tipStyle.fontSize = 11;
                tipStyle.normal.textColor = Color.gray;
                GUI.Label(new Rect(panelX, row3Y, panelW, 20), "Mở lại menu: Chạm [⚙] hoặc Giữ [L1+R1+Select] 1.5s / Bấm F1", tipStyle);

                if (GUI.Button(new Rect(panelX + 30, row3Y + 22, panelW - 60, 36), "ĐÓNG BẢNG ĐIỀU KHIỂN (B / Circle / Esc)"))
                {
                    menuOpen = false;
                }
            }
        }
    }
}
"""

full_code = code_top + final_methods

with open(fontfixer_path, "w", encoding="utf-8") as f:
    f.write(full_code)

print("Updated FontFixer.cs cleanly!")
