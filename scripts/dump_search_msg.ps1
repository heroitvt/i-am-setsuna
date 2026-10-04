$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.UiMessageWindow')

foreach ($mName in @('SearchTalkData', 'SearchMessage')) {
    $m = $t.GetMethod($mName, [System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly')
    Write-Host "=== Method: $mName ==="
    $body = $m.GetMethodBody()
    if ($body) {
        $il = $body.GetILAsByteArray()
        Write-Host "IL Bytes: $($il.Length)"
        for ($i=0; $i -lt $il.Length - 4; $i++) {
            if ($il[$i] -eq 0x7B -or $il[$i] -eq 0x7E) {
                $tok = [System.BitConverter]::ToInt32($il, $i+1)
                try {
                    $f = $asm.ManifestModule.ResolveField($tok)
                    Write-Host "  field: $($f.DeclaringType.Name)::$($f.Name)"
                } catch {}
            } elseif ($il[$i] -eq 0x28 -or $il[$i] -eq 0x6f) {
                $tok = [System.BitConverter]::ToInt32($il, $i+1)
                try {
                    $mem = $asm.ManifestModule.ResolveMember($tok)
                    Write-Host "  call: $($mem.DeclaringType.Name)::$($mem.Name)"
                } catch {}
            }
        }
    }
}
