$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")

foreach ($t in $asm.GetTypes()) {
    foreach ($m in $t.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly')) {
        $body = $m.GetMethodBody()
        if ($body) {
            $il = $body.GetILAsByteArray()
            for ($i=0; $i -lt $il.Length; $i++) {
                if ($il[$i] -eq 0x72) {
                    $token = [System.BitConverter]::ToInt32($il, $i+1)
                    try {
                        $str = $asm.ManifestModule.ResolveString($token)
                        if ($str -like '*NormalConversation*' -or $str -like '*ScenarioMessageData*') {
                            Write-Host "Type: $($t.FullName) Method: $($m.Name) -> '$str'"
                        }
                    } catch {}
                }
            }
        }
    }
}
