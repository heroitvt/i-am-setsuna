import json

with open("D:/Viet Hoa Game/temp_scripts/patch_system_tutorials.py", "r", encoding="utf-8") as f:
    code = f.read()

# Let us load TUTORIAL_TRANSLATIONS from patch_system_tutorials.py
from patch_system_tutorials import TUTORIAL_TRANSLATIONS

print(f"Loaded {len(TUTORIAL_TRANSLATIONS)} tutorial translations.")

# Generate C# code snippet
csharp_dict_lines = []
for k, v in TUTORIAL_TRANSLATIONS.items():
    escaped_v = v.replace("\\", "\\\\").replace("\"", "\\\"").replace("\r", "").replace("\n", "\\n")
    csharp_dict_lines.append(f'            uiMsgDict["{k}"] = "{escaped_v}";')

dict_csharp_code = "\n".join(csharp_dict_lines)
print("Sample C# line:\n", csharp_dict_lines[0])

# Read FontFixer.cs template
with open("D:/Viet Hoa Game/temp_scripts/FontFixer.cs", "r", encoding="utf-8") as f:
    ff_src = f.read()

# Add uiMessageParameter injection into FontFixer.cs
injection_code = f"""
            // 4. Direct Injection into ParameterManager.uiMessageParameter (Tutorials & UI System)
            try
            {{
                Type pmType = Type.GetType("Setsuna.ParameterManager, Assembly-CSharp");
                if ((object)pmType != null)
                {{
                    PropertyInfo instProp = pmType.GetProperty("Instance", BindingFlags.Public | BindingFlags.Static);
                    if ((object)instProp != null)
                    {{
                        object pmInst = instProp.GetValue(null, null);
                        if (pmInst != null)
                        {{
                            FieldInfo uiMsgField = pmType.GetField("uiMessageParameter", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                            if ((object)uiMsgField != null)
                            {{
                                Dictionary<string, string> uiMsgDict = uiMsgField.GetValue(pmInst) as Dictionary<string, string>;
                                if (uiMsgDict != null)
                                {{
{dict_csharp_code}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
            catch
            {{
            }}
"""

# Let's inspect where to insert in FontFixer.cs
idx = ff_src.find("public static bool IsVietnamese")
assert idx != -1, "Could not find insertion point"

new_ff_src = ff_src[:idx] + injection_code + "\n        " + ff_src[idx:]

with open("D:/Viet Hoa Game/temp_scripts/FontFixer.cs", "w", encoding="utf-8") as f:
    f.write(new_ff_src)

print("Updated FontFixer.cs with tutorial injection successfully!")
