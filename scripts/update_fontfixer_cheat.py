import os

fontfixer_path = r"D:\i-am-setsuna\scripts\FontFixer.cs"
with open(fontfixer_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update GetCustomFont base point size to 28
code = code.replace(
    "customFont = Font.CreateDynamicFontFromOSFont(fontNames, 20);",
    "customFont = Font.CreateDynamicFontFromOSFont(fontNames, 28);"
)

# 2. Add fields
fields_to_add = """
        private static float fontScale = -1f;
        private static bool userAdjustedScale = false;
        private static Dictionary<int, int> originalFontSizes = new Dictionary<int, int>();

        private static MethodInfo mAddMoney = null;
        private static MethodInfo mSetMoney = null;
        private static MethodInfo mGetMoney = null;
        private static bool moneyMethodsResolved = false;

        private static string notificationText = "";
        private static float notificationTimer = 0f;
"""

code = code.replace(
    "        private static Type uiMsgWinType = null;\n",
    "        private static Type uiMsgWinType = null;\n" + fields_to_add
)

# 3. Update Start and Update
old_start_update = """        private void Start()
        {
            InjectAll();
            ApplyFontAndLayoutToVietnameseText();
        }

        private void Update()
        {
            InjectAll();
            ApplyFontAndLayoutToVietnameseText();
        }"""

new_start_update = """        private void Start()
        {
            InjectAll();
            ApplyFontAndLayoutToVietnameseText();
            ShowNotification("VIỆT HÓA SETSUNA | [F1] Phím Tắt & Cheat | [F8] +500k G | [F9] Max G");
        }

        private void Update()
        {
            InjectAll();
            ApplyFontAndLayoutToVietnameseText();
            HandleKeyInputs();
        }"""

code = code.replace(old_start_update, new_start_update)

# 4. Replace ApplyFontAndLayoutToVietnameseText and add cheat methods
old_apply = """        public static void ApplyFontAndLayoutToVietnameseText()
        {
            Font font = GetCustomFont();
            if ((object)font == null) return;

            Text[] texts = UnityEngine.Object.FindObjectsOfType<Text>();
            if (texts == null) return;

            for (int i = 0; i < texts.Length; i++)
            {
                Text t = texts[i];
                if ((object)t != null && !string.IsNullOrEmpty(t.text) && IsVietnamese(t.text))
                {
                    if ((object)t.font != (object)font)
                    {
                        t.font = font;
                    }

                    // Dynamic Multi-Resolution Adaptation:
                    // 1. Enable Horizontal & Vertical Overflow so text is never truncated by bounding boxes
                    t.horizontalOverflow = HorizontalWrapMode.Wrap;
                    t.verticalOverflow = VerticalWrapMode.Overflow;

                    // 2. Compact line spacing (0.9f) to fit 2-3 lines comfortably in dialogue frames across 720p/1080p/2K/4K
                    if (t.lineSpacing > 0.92f || t.lineSpacing < 0.88f)
                    {
                        t.lineSpacing = 0.90f;
                    }
                }
            }
        }"""

new_apply_and_cheats = """        public static void ApplyFontAndLayoutToVietnameseText(bool forceRefresh = false)
        {
            Font font = GetCustomFont();
            if ((object)font == null) return;

            // Auto-determine base font scale for resolution if not adjusted by player
            if (fontScale < 0f)
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
                // 1. Enable Horizontal & Vertical Overflow so text is never truncated by bounding boxes
                t.horizontalOverflow = HorizontalWrapMode.Wrap;
                t.verticalOverflow = VerticalWrapMode.Overflow;

                // 2. Compact line spacing (0.90f) to fit 2-3 lines comfortably in dialogue frames across 720p/1080p/2K/4K
                if (t.lineSpacing > 0.92f || t.lineSpacing < 0.88f)
                {
                    t.lineSpacing = 0.90f;
                }

                // 3. Scaling Font Size for clear readability at 1080p / higher resolutions
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
                    ShowNotification("VUI LÒNG VÀO TRÒ CHƠI / TẢI SAVE TRƯỚC KHI BẤM CHEAT!");
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
                    ShowNotification("VUI LÒNG VÀO TRÒ CHƠI / TẢI SAVE TRƯỚC KHI BẤM CHEAT!");
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

        private void OnGUI()
        {
            if (notificationTimer > 0f)
            {
                notificationTimer -= Time.deltaTime;
                int screenW = Screen.width;
                int screenH = Screen.height;

                int boxW = Mathf.Min(740, screenW - 40);
                int boxH = 48;
                int boxX = (screenW - boxW) / 2;
                int boxY = 24;

                GUI.color = new Color(0f, 0f, 0f, 0.85f);
                GUI.Box(new Rect(boxX - 2, boxY - 2, boxW + 4, boxH + 4), "");
                GUI.color = new Color(0.12f, 0.38f, 0.72f, 0.95f);
                GUI.Box(new Rect(boxX, boxY, boxW, boxH), "");

                GUIStyle style = new GUIStyle();
                style.alignment = TextAnchor.MiddleCenter;
                style.fontSize = Mathf.Clamp(Mathf.RoundToInt(screenH * 0.022f), 15, 24);
                style.fontStyle = FontStyle.Bold;
                style.normal.textColor = Color.yellow;

                GUI.color = Color.white;
                GUI.Label(new Rect(boxX, boxY, boxW, boxH), notificationText, style);
            }
        }

        private void HandleKeyInputs()
        {
            // F1: Hướng dẫn
            if (Input.GetKeyDown(KeyCode.F1))
            {
                ShowNotification("[F6/F7]: Chỉnh cỡ chữ | [F8]: +500.000 G | [F9]: Max 99.999.999 G");
            }

            // F6: Giảm cỡ chữ
            if (Input.GetKeyDown(KeyCode.F6))
            {
                userAdjustedScale = true;
                fontScale = Mathf.Max(0.80f, fontScale - 0.05f);
                ApplyFontAndLayoutToVietnameseText(true);
                ShowNotification(string.Format("CỠ CHỮ VIỆT HÓA: {0}% (MẶC ĐỊNH: 125%)", Mathf.RoundToInt(fontScale * 100f)));
            }

            // F7: Tăng cỡ chữ
            if (Input.GetKeyDown(KeyCode.F7))
            {
                userAdjustedScale = true;
                fontScale = Mathf.Min(2.00f, fontScale + 0.05f);
                ApplyFontAndLayoutToVietnameseText(true);
                ShowNotification(string.Format("CỠ CHỮ VIỆT HÓA: {0}% (MẶC ĐỊNH: 125%)", Mathf.RoundToInt(fontScale * 100f)));
            }

            // F8: Cheat +500,000 Vàng
            if (Input.GetKeyDown(KeyCode.F8))
            {
                AddMoneyCheat(500000);
            }

            // F9: Cheat Max Vàng
            if (Input.GetKeyDown(KeyCode.F9))
            {
                SetMaxMoneyCheat();
            }
        }"""

code = code.replace(old_apply, new_apply_and_cheats)

with open(fontfixer_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated FontFixer.cs successfully!")
