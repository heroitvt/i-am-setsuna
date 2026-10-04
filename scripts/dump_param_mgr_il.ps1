$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.ParameterManager')

foreach ($mName in @('LoadChapterText', 'PackDataLoad', 'DecryptParameter')) {
    $methods = $t.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly') | Where-Object { $_.Name -eq $mName }
    foreach ($m in $methods) {
        Write-Host "=== Method: $($m.Name) ($($m.GetParameters().Length) params) ==="
        $body = $m.GetMethodBody()
        if ($body) {
            $il = $body.GetILAsByteArray()
            for ($i=0; $i -lt $il.Length; $i++) {
                $b = $il[$i]
                if ($b -eq 0x72) {
                    $token = [System.BitConverter]::ToInt32($il, $i+1)
                    try {
                        $str = $asm.ManifestModule.ResolveString($token)
                        Write-Host "  ldstr: '$str'"
                    } catch {}
                } elseif ($b -eq 0x28 -or $b -eq 0x6f) {
                    $token = [System.BitConverter]::ToInt32($il, $i+1)
                    try {
                        $member = $asm.ManifestModule.ResolveMember($token)
                        Write-Host "  call: $($member.DeclaringType.Name)::$($member.Name)"
                    } catch {}
                }
            }
        }
    }
}
