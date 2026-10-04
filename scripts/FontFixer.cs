using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using UnityEngine;
using UnityEngine.UI;

namespace SetsunaFontFix
{
    public class FontFixer : MonoBehaviour
    {
        private static Font customFont = null;
        private static bool initialized = false;

        private static byte[] vnChapter1Dec = null;
        private static byte[] vnNormalConvDec = null;
        private static byte[] vnChapter1Enc = null;
        private static byte[] vnNormalConvEnc = null;
        private static byte[] vnSystemMsgEnc = null;

        private static Dictionary<string, byte[]> encFiles = new Dictionary<string, byte[]>(StringComparer.OrdinalIgnoreCase);
        private static bool binariesLoaded = false;
        private static bool skillDataReloaded = false;

        private static FieldInfo mainPathField = null;
        private static FieldInfo convField = null;
        private static FieldInfo lastChapterField = null;
        private static Type uiMsgWinType = null;

        private static Dictionary<string, string> tutorialMap = new Dictionary<string, string>()
        {
            {"SYS142", "Thương Hội Ma Đạo"},
            {"SYS143", "Đầu Bếp & Nấu Ăn"},
            {"SYS144", "Rèn Cường Hóa Vũ Khí"},
            {"SYS145", "Biến Chuyển Flux"},
            {"SYS146", "Biến Chuyển Hỗ Trợ"},
            {"SYS147", "Chạm Trán Quái Vật"},
            {"SYS148", "Chiến Đấu Thời Gian Thực (ATB)"},
            {"SYS149", "Pháp Thạch Spritnite"},
            {"SYS150", "Chế Độ Xung Lực (Momentum)"},
            {"SYS151", "Hiệu Ứng Xung Lực & Dị Thường"},
            {"SYS152", "Điểm Lưu Game"},
            {"SYS173", "Thành viên của Thương Hội Ma Đạo có mặt tại các thị trấn và làng mạc trên khắp đại lục.\r\n\r\nHọ sẽ thu mua những nguyên liệu mà quái vật đánh rơi. Ngoài việc nhận được tiền vàng, bạn còn có thể đổi lấy các viên pháp thạch Spritnite tùy thuộc vào những loại nguyên liệu bạn đã từng bán. Quái vật sẽ rơi ra các vật phẩm khác nhau tùy thuộc vào cách bạn tiêu diệt chúng (chẳng hạn như dùng đòn tấn công thuộc tính nhất định, dùng liên chiêu combo, dùng đòn đánh Xung Lực, tiêu diệt khi chúng đang dính trạng thái bất lợi, tiêu diệt với lượng sát thương vượt trội Over Kill, hoặc tiêu diệt với lượng sát thương vừa vặn Exact Kill).\r\n\r\nCác viên pháp thạch Spritnite bạn có thể nhận được hiển thị tại mục 'Nhận Spritnite'. Càng tiến sâu vào hành trình, càng có thêm nhiều pháp thạch mới, vì vậy hãy thường xuyên quay lại kiểm tra nhé!"},
            {"SYS174", "Đầu bếp có mặt tại các thị trấn và làng mạc trên khắp đại lục.\r\n\r\nBằng cách trò chuyện với họ, bạn có thể mua các món ăn bồi bổ. Thức ăn chỉ có thể dùng từ menu và sẽ phát huy tác dụng tăng chỉ số trong trận chiến tiếp theo. Sau trận chiến đó, hiệu quả sẽ kết thúc.\r\n\r\nBạn có thể mở rộng danh sách món ăn bằng cách thu thập đủ các nguyên liệu cần thiết để nhận công thức nấu nướng. Nguyên liệu có thể nhặt được tại các điểm phát sáng lấp lánh trên bản đồ thế giới và trong các khu vực. Khi có đủ nguyên liệu, trò chuyện với các NPC nhất định sẽ giúp bạn nhận được công thức món ăn mới."},
            {"SYS175", "Trên suốt chuyến hành trình, đôi khi bạn sẽ tìm thấy những loại kim loại đặc biệt.\r\n\r\nBằng cách kết hợp những kim loại này với vũ khí của bạn, bạn có thể gia tăng các chỉ số tấn công và phòng thủ của chúng. Bạn có thể thực hiện việc này ngay từ menu Vũ Khí.\r\n\r\nCàng tiến xa trong game, bạn cũng sẽ có thể mua thêm những kim loại quý này tại các thương gia và tiệm vũ khí."},
            {"SYS176", "Nếu một nhân vật trang bị bùa hộ mệnh Talisman có dòng thưởng Flux, hiệu ứng Biến Chuyển Flux đôi khi sẽ ngẫu nhiên xuất hiện khi nhân vật đó sử dụng kỹ năng hoặc liên chiêu ở chế độ Xung Lực (Momentum). Điều này cho phép bạn cường hóa pháp thạch Spritnite tương ứng bằng cách khắc thêm các thuộc tính 'Flux' vào viên đá.\r\n\r\nCó rất nhiều loại thưởng Flux khác nhau: tăng uy lực kỹ năng, giảm lượng MP tiêu hao, nạp sẵn thanh ATB sau khi hành động, và nhiều hiệu ứng khác. Loại thưởng nhận được sẽ phụ thuộc vào bùa hộ mệnh mà bạn đang trang bị.\r\n\r\nKhi Biến Chuyển Flux xuất hiện trong trận đấu, các thuộc tính nhận được sẽ hiển thị trên màn hình sau khi trận chiến kết thúc. Bạn có thể chọn có khắc các thuộc tính này vào pháp thạch Spritnite hay không để tùy biến sức mạnh theo ý thích."},
            {"SYS177", "Bên cạnh Pháp Thạch Mệnh Lệnh (Command Spritnite), Biến Chuyển Flux đôi khi cũng xuất hiện trên Pháp Thạch Hỗ Trợ (Support Spritnite).\r\n\r\nNếu một nhân vật trang bị bùa hộ mệnh có dòng thưởng 'Thưởng Hỗ Trợ' (Support Bonus), đồng thời trang bị nhiều hơn một Pháp Thạch Hỗ Trợ, hiện tượng Biến Chuyển Flux đôi khi sẽ ngẫu nhiên xuất hiện trên một trong các viên pháp thạch khi kích hoạt chế độ Xung Lực.\r\n\r\nKhi điều này xảy ra, hiệu ứng của một viên Pháp Thạch Hỗ Trợ sẽ được khắc ghép sang viên đá kia. Tuy nhiên, hiệu ứng ghép thêm này sẽ chỉ mang 1/10 sức mạnh gốc của nó."},
            {"SYS178", "Khi bạn di chuyển lại gần quái vật trong một khoảng cách nhất định, trận chiến sẽ bắt đầu.\r\n\r\nNếu bạn tiếp cận quái vật từ phía trước, chúng sẽ vào thế phòng thủ sẵn sàng. Tuy nhiên, nếu bạn lén tiếp cận chúng từ phía sau lưng, chúng sẽ bị bất ngờ sơ hở. Khi đó, bạn sẽ bắt đầu trận chiến với thanh ATB và thanh SP được nạp đầy 100%, cho phép tung ra đòn tấn công phủ đầu chớp nhoáng.\r\n\r\nCả hai thanh ATB và SP đều đóng vai trò sống còn trong chiến đấu, và sẽ được giải thích chi tiết ở các phần tiếp theo."},
            {"SYS179", "Khi trận chiến bắt đầu, thanh đo ATB (Active Time Battle) của các nhân vật hiển thị ở góc dưới màn hình sẽ bắt đầu nạp dần. Khi thanh ATB của một nhân vật đầy, bảng lệnh chiến đấu của nhân vật đó sẽ xuất hiện. Hãy chọn một mệnh lệnh (Tấn công, Kỹ năng, Vật phẩm) và mục tiêu, nhân vật sẽ thực hiện hành động đó ngay lập tức.\r\n\r\nKhi có nhiều hơn một nhân vật đầy thanh ATB, bạn có thể nhấn phím điều hướng trái/phải hoặc gạt cần analog trái sang hai bên để chuyển đổi giữa các nhân vật.\r\n\r\nDù không hiển thị trên màn hình, quái vật cũng sở hữu thanh đo ATB riêng và sẽ ra đòn ngay khi thanh của chúng đầy."},
            {"SYS180", "Spritnite là những viên đá chứa đầy ma lực huyền bí. Trang bị chúng cho phép các nhân vật sở hữu vô vàn sức mạnh đặc biệt.\r\n\r\nCó hai loại pháp thạch: Pháp Thạch Mệnh Lệnh cho phép nhân vật sử dụng các kỹ năng khác nhau trong trận chiến và từ menu Kỹ Năng; trong khi Pháp Thạch Hỗ Trợ mang lại các hiệu ứng bổ trợ tự động kích hoạt trong suốt trận chiến.\r\n\r\nPháp thạch có thể được trang bị từ menu chính. Thao tác này được thực hiện bằng cách khảm chúng vào các 'ô chứa' (slots) trên bùa hộ mệnh Talisman. Ban đầu nhân vật chỉ có 1 ô chứa, nhưng sẽ mở thêm nhiều ô hơn khi thăng cấp và khi trang bị các loại bùa hộ mệnh cao cấp khác nhau. Có ba loại ô chứa: ô dành riêng cho Pháp Thạch Mệnh Lệnh, ô dành riêng cho Pháp Thạch Hỗ Trợ, và ô đa năng có thể khảm bất kỳ loại pháp thạch nào."},
            {"SYS181", "Khi thanh ATB của nhân vật đã đầy nhưng bạn chưa chọn mệnh lệnh, thanh đo SP (Special Power) hình tròn ở bên phải sẽ bắt đầu được tích lũy. Thanh này cũng sẽ được nạp khi nhân vật thực hiện hành động hoặc phải chịu sát thương. Khi đầy, thanh sẽ nhấp nháy phát sáng và một điểm SP màu vàng sẽ xuất hiện ở trên đỉnh. Sau đó thanh đo sẽ được thiết lập lại và bắt đầu tích lũy tiếp từ dưới lên. Số điểm SP tối đa có thể tích lũy là 3 điểm.\r\n\r\nKhi nhân vật có ít nhất 1 điểm SP, bạn có thể kích hoạt 'Chế độ Xung Lực' (Momentum mode) để bổ sung thêm nhiều hiệu ứng uy lực cho các đòn đánh và kỹ năng. Ngay khoảnh khắc nhân vật chuẩn bị ra đòn, một vệt sáng sẽ bừng lên trên đầu họ; nhấn phím <ICON_SQUARE> <BUTTON> (phím H trên bàn phím) đúng vào thời khắc đó sẽ kích hoạt Chế độ Xung Lực."},
            {"SYS182", "Kích hoạt Chế độ Xung Lực sẽ bổ sung thêm nhiều hiệu ứng uy lực đặc biệt cho các kỹ năng và liên chiêu combo của bạn.\r\n\r\nKích hoạt khi tấn công sẽ gây thêm sát thương phụ, chắc chắn gây đòn chí mạng, hoặc áp đặt trạng thái bất lợi lên kẻ địch. Kích hoạt khi dùng kỹ năng trị thương hoặc hỗ trợ sẽ hồi thêm HP/MP, mở rộng phạm vi tác dụng, hoặc kéo dài thời gian duy trì của bùa lợi.\r\n\r\nTrong trận chiến, các phần thưởng đặc biệt ảnh hưởng lên toàn đội đôi khi cũng ngẫu nhiên xuất hiện. Hiện tượng này được gọi là 'Điểm Dị Thường' (Singularity). Có rất nhiều loại dị thường khác nhau và xuất hiện ngẫu nhiên. Càng sử dụng chế độ Xung Lực nhiều lần, tỉ lệ kích hoạt Điểm Dị Thường càng cao. Trong các trận đánh boss kéo dài, hãy tận dụng chế độ Xung Lực càng nhiều càng tốt!"},
            {"SYS183", "Điểm Lưu Game (Save Points) là những quầng sáng ma thuật xuất hiện trên các bản đồ khu vực, cho phép bạn ghi lại tiến trình chơi game hiện tại. Nếu bước vào trong quầng sáng này và nhấn phím <ICON_CIRCLE> <BUTTON>, bạn sẽ được hỏi có muốn lưu game hay không. Ngoài ra, bạn cũng có thể mở menu chính khi đang đứng trong quầng sáng và chọn mục Lưu Game.\r\n\r\nĐiểm Lưu Game chỉ xuất hiện ở một số vị trí nhất định trong các khu vực. Tuy nhiên, khi ở trên Bản Đồ Thế Giới (World Map), bạn sẽ có thể lưu tiến trình chơi bất cứ lúc nào trực tiếp từ menu chính.\r\n\r\nXin lưu ý rằng trò chơi này không tự động lưu game (No Auto-Save). Hãy luôn chủ động lưu game thường xuyên để đảm bảo hành trình của bạn luôn an toàn và thuận lợi."}
        };

        public static Font GetCustomFont()
        {
            if ((object)customFont == null)
            {
                string[] fontNames = new string[]
                {
                    "Georgia",
                    "Palatino Linotype",
                    "Book Antiqua",
                    "Times New Roman",
                    "Segoe UI",
                    "Arial"
                };
                customFont = Font.CreateDynamicFontFromOSFont(fontNames, 20);
                if ((object)customFont != null)
                {
                    UnityEngine.Object.DontDestroyOnLoad(customFont);
                }
            }
            return customFont;
        }

        public static void Initialize()
        {
            if (!initialized)
            {
                initialized = true;
                LoadBinaries();
                GameObject go = new GameObject("SetsunaFontFixerObj");
                UnityEngine.Object.DontDestroyOnLoad(go);
                go.AddComponent<FontFixer>();
                Debug.Log("[SetsunaFontFix] Initialized Complete Vietnamese Dialogue, Skills & Font Injector.");
            }
        }

        private static void LoadBinaries()
        {
            if (binariesLoaded) return;
            try
            {
                string dir = Path.Combine(Application.streamingAssetsPath, "data/parameter");

                string pCh1Dec = Path.Combine(dir, "ScenarioMessageData_Chapter_1.dec");
                if (File.Exists(pCh1Dec)) vnChapter1Dec = File.ReadAllBytes(pCh1Dec);

                string pNormDec = Path.Combine(dir, "ScenarioMessageData_NormalConversation.dec");
                if (File.Exists(pNormDec)) vnNormalConvDec = File.ReadAllBytes(pNormDec);

                string pCh1Enc = Path.Combine(dir, "ScenarioMessageData_Chapter_1");
                if (File.Exists(pCh1Enc)) vnChapter1Enc = File.ReadAllBytes(pCh1Enc);

                string pNormEnc = Path.Combine(dir, "ScenarioMessageData_NormalConversation");
                if (File.Exists(pNormEnc)) vnNormalConvEnc = File.ReadAllBytes(pNormEnc);

                string pSysEnc = Path.Combine(dir, "SystemMessage");
                if (File.Exists(pSysEnc)) vnSystemMsgEnc = File.ReadAllBytes(pSysEnc);

                string[] skillFileList = new string[]
                {
                    "PlayerSkillDataMessage", "SetsunaSkillDataMessage", "TsukushiSkillDataMessage",
                    "YomiSkillDataMessage", "KishilSkillDataMessage", "SionSkillDataMessage",
                    "GrimreaperSkillDataMessage", "TwoPlayerCoopSkillDataMessage", "ThreePlayerCoopSkillDataMessage",
                    "EnemySkillDataMessage", "EnemyBossSkillDataMessage", "EnemyCoopSkillDataMessage",
                    "ItemSkillDataMessage", "MateriaMessage", "SystemMessage"
                };

                for (int i = 0; i < skillFileList.Length; i++)
                {
                    string fName = skillFileList[i];
                    string p = Path.Combine(dir, fName);
                    if (File.Exists(p))
                    {
                        encFiles[fName] = File.ReadAllBytes(p);
                    }
                }

                binariesLoaded = true;
                Debug.Log("[SetsunaFontFix] Binaries loaded: encFiles=" + encFiles.Count);
            }
            catch (Exception ex)
            {
                Debug.LogError("[SetsunaFontFix] Error loading binaries: " + ex.Message);
            }
        }

        private void Awake()
        {
            UnityEngine.Object.DontDestroyOnLoad(this.gameObject);
        }

        private void Start()
        {
            InjectAll();
            ApplyFontToVietnameseText();
        }

        private void Update()
        {
            InjectAll();
            ApplyFontToVietnameseText();
        }

        private static void InjectAll()
        {
            if (!binariesLoaded) LoadBinaries();

            // 1. Direct Injection into UiMessageWindow
            try
            {
                if ((object)uiMsgWinType == null)
                {
                    uiMsgWinType = Type.GetType("Setsuna.UiMessageWindow, Assembly-CSharp");
                    if ((object)uiMsgWinType != null)
                    {
                        mainPathField = uiMsgWinType.GetField("_mainPathTextData", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                        convField = uiMsgWinType.GetField("conversationTextData", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                        lastChapterField = uiMsgWinType.GetField("lastchapterName", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                    }
                }

                if ((object)uiMsgWinType != null && (object)mainPathField != null && (object)convField != null)
                {
                    UnityEngine.Object[] windows = UnityEngine.Object.FindObjectsOfType(uiMsgWinType);
                    if (windows != null)
                    {
                        for (int i = 0; i < windows.Length; i++)
                        {
                            object win = windows[i];
                            if (win != null)
                            {
                                string curLastChapter = (lastChapterField != null) ? (lastChapterField.GetValue(win) as string) : null;
                                
                                if (vnChapter1Dec != null)
                                {
                                    if (string.IsNullOrEmpty(curLastChapter) || curLastChapter.IndexOf("Chapter_1", StringComparison.OrdinalIgnoreCase) >= 0)
                                    {
                                        byte[] curMain = mainPathField.GetValue(win) as byte[];
                                        if (curMain == null || curMain != vnChapter1Dec)
                                        {
                                            mainPathField.SetValue(win, vnChapter1Dec);
                                            if (lastChapterField != null)
                                            {
                                                lastChapterField.SetValue(win, "ScenarioMessageData_Chapter_1");
                                            }
                                        }
                                    }
                                }

                                if (vnNormalConvDec != null)
                                {
                                    byte[] curConv = convField.GetValue(win) as byte[];
                                    if (curConv == null || curConv != vnNormalConvDec)
                                    {
                                        convField.SetValue(win, vnNormalConvDec);
                                    }
                                }
                            }
                        }
                    }
                }
            }
            catch
            {
            }

            // 2. Direct Injection into ParameterManager.dataList
            try
            {
                Type pmType = Type.GetType("Setsuna.ParameterManager, Assembly-CSharp");
                if ((object)pmType != null)
                {
                    PropertyInfo instProp = pmType.GetProperty("Instance", BindingFlags.Public | BindingFlags.Static);
                    if ((object)instProp != null)
                    {
                        object pmInst = instProp.GetValue(null, null);
                        if (pmInst != null)
                        {
                            FieldInfo dataListField = pmType.GetField("dataList", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                            if ((object)dataListField != null)
                            {
                                IDictionary dict = dataListField.GetValue(pmInst) as IDictionary;
                                if (dict != null)
                                {
                                    foreach (KeyValuePair<string, byte[]> kvp in encFiles)
                                    {
                                        dict[kvp.Key] = kvp.Value;
                                        dict["Parameters/x86_64/Init/" + kvp.Key] = kvp.Value;
                                    }
                                }
                            }

                            // Inject directly into uiMessageParameter
                            FieldInfo uiMsgField = pmType.GetField("uiMessageParameter", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                            if ((object)uiMsgField != null)
                            {
                                Dictionary<string, string> uiMsgDict = uiMsgField.GetValue(pmInst) as Dictionary<string, string>;
                                if (uiMsgDict != null)
                                {
                                    foreach (KeyValuePair<string, string> kvp in tutorialMap)
                                    {
                                        uiMsgDict[kvp.Key] = kvp.Value;
                                    }
                                }
                            }

                            // Trigger MakeSkillData and MakeUiMessageData once to apply
                            if (!skillDataReloaded)
                            {
                                skillDataReloaded = true;
                                MethodInfo mMakeSkill = pmType.GetMethod("MakeSkillData", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                                if ((object)mMakeSkill != null)
                                {
                                    mMakeSkill.Invoke(pmInst, null);
                                    Debug.Log("[SetsunaFontFix] Re-executed MakeSkillData with Vietnamese skills!");
                                }
                            }
                        }
                    }
                }
            }
            catch
            {
            }

            // 3. Direct Injection into ResourceManager.resourceDictionary
            try
            {
                Type rmType = Type.GetType("Setsuna.ResourceManager, Assembly-CSharp");
                if ((object)rmType != null)
                {
                    PropertyInfo instProp = rmType.GetProperty("Instance", BindingFlags.Public | BindingFlags.Static);
                    if ((object)instProp != null)
                    {
                        object rmInst = instProp.GetValue(null, null);
                        if (rmInst != null)
                        {
                            FieldInfo resDictField = rmType.GetField("resourceDictionary", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                            if ((object)resDictField != null)
                            {
                                IDictionary resDict = resDictField.GetValue(rmInst) as IDictionary;
                                if (resDict != null)
                                {
                                    ArrayList keys = new ArrayList(resDict.Keys);
                                    for (int k = 0; k < keys.Count; k++)
                                    {
                                        string key = keys[k] as string;
                                        if (!string.IsNullOrEmpty(key))
                                        {
                                            foreach (KeyValuePair<string, byte[]> kvp in encFiles)
                                            {
                                                if (key.IndexOf(kvp.Key, StringComparison.OrdinalIgnoreCase) >= 0)
                                                {
                                                    object resObj = resDict[key];
                                                    if (resObj != null)
                                                    {
                                                        FieldInfo bytesF = resObj.GetType().GetField("bytes", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                                                        if ((object)bytesF != null)
                                                        {
                                                            bytesF.SetValue(resObj, kvp.Value);
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            catch
            {
            }
        }

        public static bool IsVietnamese(string str)
        {
            if (string.IsNullOrEmpty(str)) return false;
            for (int i = 0; i < str.Length; i++)
            {
                if ((int)str[i] > 127) return true;
            }
            return false;
        }

        public static void ApplyFontToVietnameseText()
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
                }
            }
        }
    }
}
