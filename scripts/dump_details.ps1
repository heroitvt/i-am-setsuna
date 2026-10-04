$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.UI.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\SetsunaFontFix.dll")
$t = $asm.GetType('SetsunaFontFix.FontFixer')

foreach ($m in $t.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly')) {
    Write-Host "=== Method: $($m.Name) ==="
    $body = $m.GetMethodBody()
    if ($body) {
        $il = $body.GetILAsByteArray()
        for ($i=0; $i -lt $il.Length; $i++) {
            $b = $il[$i]
            if ($b -eq 0x72) { # ldstr
                $token = [System.BitConverter]::ToInt32($il, $i+1)
                $str = $asm.ManifestModule.ResolveString($token)
                Write-Host "  ldstr: '$str'"
            } elseif ($b -eq 0x28 -or $b -eq 0x6f) { # call or callvirt
                $token = [System.BitConverter]::ToInt32($il, $i+1)
                try {
                    $member = $asm.ManifestModule.ResolveMember($token)
                    Write-Host "  call: $($member.DeclaringType.Name)::$($member.Name)"
                } catch {}
            }
        }
    }
}
