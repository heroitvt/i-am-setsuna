import os

fontfixer_path = r"D:\i-am-setsuna\scripts\FontFixer.cs"
with open(fontfixer_path, "r", encoding="utf-8") as f:
    code = f.read()

# Replace fields with expanded Gamepad and Keyboard fields
old_fields = """        private static float fontScale = -1f;
        private static bool userAdjustedScale = false;
        private static Dictionary<int, int> originalFontSizes = new Dictionary<int, int>();

        private static MethodInfo mAddMoney = null;
        private static MethodInfo mSetMoney = null;
        private static MethodInfo mGetMoney = null;
        private static bool moneyMethodsResolved = false;

        private static string notificationText = "";
        private static float notificationTimer = 0f;"""

new_fields = """        private static float fontScale = -1f;
        private static bool userAdjustedScale = false;
        private static Dictionary<int, int> originalFontSizes = new Dictionary<int, int>();

        private static MethodInfo mAddMoney = null;
        private static MethodInfo mSetMoney = null;
        private static MethodInfo mGetMoney = null;
        private static bool moneyMethodsResolved = false;

        private static PropertyInfo pIsL1 = null;
        private static PropertyInfo pIsR1 = null;
        private static PropertyInfo pIsL3 = null;
        private static PropertyInfo pIsR3 = null;
        private static PropertyInfo pIsDpadUp = null;
        private static PropertyInfo pIsDpadDown = null;
        private static PropertyInfo pIsDpadLeft = null;
        private static PropertyInfo pIsDpadRight = null;
        private static PropertyInfo pIsSelect = null;
        private static PropertyInfo pIsTriangle = null;
        private static bool inputMethodsResolved = false;

        private static bool prevPadUp = false;
        private static bool prevPadDown = false;
        private static bool prevPadLeft = false;
        private static bool prevPadRight = false;
        private static bool prevPadL3R3 = false;
        private static bool prevPadSelect = false;

        private static string notificationText = "";
        private static float notificationTimer = 0f;"""

code = code.replace(old_fields, new_fields)

# Update Start greeting to mention Gamepad
old_greeting = 'ShowNotification("VIỆT HÓA SETSUNA | [F1] Phím Tắt & Cheat | [F8] +500k G | [F9] Max G");'
new_greeting = 'ShowNotification("VIỆT HÓA SETSUNA | [F1] hoặc [L3+R3] Bật Hướng Dẫn | Gamepad: Giữ [L1+R1] + D-Pad");'
code = code.replace(old_greeting, new_greeting)

# Replace HandleKeyInputs and add input helper methods
old_handle = """        private void HandleKeyInputs()
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

new_handle = """        private static void ResolveInputMethods()
        {
            if (inputMethodsResolved) return;
            inputMethodsResolved = true;
            try
            {
                Type inType = Type.GetType("Setsuna.InputManager, Assembly-CSharp");
                if (inType != null)
                {
                    pIsL1 = inType.GetProperty("IsL1", BindingFlags.Public | BindingFlags.Static);
                    pIsR1 = inType.GetProperty("IsR1", BindingFlags.Public | BindingFlags.Static);
                    pIsL3 = inType.GetProperty("IsL3", BindingFlags.Public | BindingFlags.Static);
                    pIsR3 = inType.GetProperty("IsR3", BindingFlags.Public | BindingFlags.Static);
                    pIsDpadUp = inType.GetProperty("IsDpadUp", BindingFlags.Public | BindingFlags.Static);
                    pIsDpadDown = inType.GetProperty("IsDpadDown", BindingFlags.Public | BindingFlags.Static);
                    pIsDpadLeft = inType.GetProperty("IsDpadLeft", BindingFlags.Public | BindingFlags.Static);
                    pIsDpadRight = inType.GetProperty("IsDpadRight", BindingFlags.Public | BindingFlags.Static);
                    pIsSelect = inType.GetProperty("IsSelect", BindingFlags.Public | BindingFlags.Static);
                    pIsTriangle = inType.GetProperty("IsTriangle", BindingFlags.Public | BindingFlags.Static);
                }
            }
            catch (Exception ex)
            {
                Debug.LogError("[SetsunaFontFix] Failed to resolve InputManager properties: " + ex.Message);
            }
        }

        private static bool GetPadProp(PropertyInfo p)
        {
            if (p != null)
            {
                try
                {
                    return (bool)p.GetValue(null, null);
                }
                catch { }
            }
            return false;
        }

        private void HandleKeyInputs()
        {
            ResolveInputMethods();

            // 1. Gamepad Input Detection (Setsuna.InputManager + Native Unity KeyCode Fallback)
            bool isL1 = GetPadProp(pIsL1) || Input.GetKey(KeyCode.JoystickButton4);
            bool isR1 = GetPadProp(pIsR1) || Input.GetKey(KeyCode.JoystickButton5);
            bool isL3 = GetPadProp(pIsL3) || Input.GetKey(KeyCode.JoystickButton8);
            bool isR3 = GetPadProp(pIsR3) || Input.GetKey(KeyCode.JoystickButton9);
            bool isDpadUp = GetPadProp(pIsDpadUp);
            bool isDpadDown = GetPadProp(pIsDpadDown);
            bool isDpadLeft = GetPadProp(pIsDpadLeft);
            bool isDpadRight = GetPadProp(pIsDpadRight);
            bool isSelect = GetPadProp(pIsSelect) || Input.GetKey(KeyCode.JoystickButton6);

            // Debouncing trigger edges (1 click per press)
            bool pressUp = isDpadUp && !prevPadUp;
            bool pressDown = isDpadDown && !prevPadDown;
            bool pressLeft = isDpadLeft && !prevPadLeft;
            bool pressRight = isDpadRight && !prevPadRight;
            bool pressSelect = isSelect && !prevPadSelect;
            bool pressL3R3 = (isL3 && isR3) && !prevPadL3R3;

            prevPadUp = isDpadUp;
            prevPadDown = isDpadDown;
            prevPadLeft = isDpadLeft;
            prevPadRight = isDpadRight;
            prevPadSelect = isSelect;
            prevPadL3R3 = (isL3 && isR3);

            bool holdL1R1 = isL1 && isR1;

            // ========================================================
            // A. GAMEPAD COMBO CONTROLS (GIỮ L1 + R1 / LB + RB)
            // ========================================================
            if (holdL1R1)
            {
                // [L1 + R1] + D-Pad Lên: Tăng cỡ chữ
                if (pressUp)
                {
                    userAdjustedScale = true;
                    fontScale = Mathf.Min(2.00f, fontScale + 0.05f);
                    ApplyFontAndLayoutToVietnameseText(true);
                    ShowNotification(string.Format("GAMEPAD [L1+R1+LÊN]: CỠ CHỮ {0}%", Mathf.RoundToInt(fontScale * 100f)));
                }
                // [L1 + R1] + D-Pad Xuống: Giảm cỡ chữ
                else if (pressDown)
                {
                    userAdjustedScale = true;
                    fontScale = Mathf.Max(0.80f, fontScale - 0.05f);
                    ApplyFontAndLayoutToVietnameseText(true);
                    ShowNotification(string.Format("GAMEPAD [L1+R1+XUỐNG]: CỠ CHỮ {0}%", Mathf.RoundToInt(fontScale * 100f)));
                }
                // [L1 + R1] + D-Pad Trái: Cheat +500.000 Vàng
                else if (pressLeft)
                {
                    AddMoneyCheat(500000);
                }
                // [L1 + R1] + D-Pad Phải: Cheat Max 99.999.999 Vàng
                else if (pressRight)
                {
                    SetMaxMoneyCheat();
                }
                // [L1 + R1] + Select: Bật hướng dẫn
                else if (pressSelect)
                {
                    ShowNotification("[L1+R1]+D-Pad Lên/Xuống: Cỡ chữ | +Trái: +500k G | +Phải: Max G | L3+R3: +500k G");
                }
            }

            // Gamepad Shortcut: Nhấn đồng thời 2 cần Analog (L3 + R3) -> Cộng 500k Vàng & Bật Hướng dẫn
            if (pressL3R3)
            {
                AddMoneyCheat(500000);
            }

            // ========================================================
            // B. KEYBOARD HOTKEYS (BÀN PHÍM PC)
            // ========================================================
            // F1: Hướng dẫn
            if (Input.GetKeyDown(KeyCode.F1))
            {
                ShowNotification("[F6/F7]: Cỡ chữ | [F8]: +500k G | [F9]: Max G | Gamepad: [L1+R1]+D-Pad");
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

code = code.replace(old_handle, new_handle)

with open(fontfixer_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated FontFixer.cs with Gamepad support!")
