$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.UiMessageWindow')

$m = $t.GetMethod('get_mainPathTextData', [System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly')
$body = $m.GetMethodBody()
$il = $body.GetILAsByteArray()

Write-Host "Bytes: $([System.BitConverter]::ToString($il))"
for ($i=0; $i -lt $il.Length - 4; $i++) {
    if ($il[$i] -eq 0x72) {
        $st = [System.BitConverter]::ToInt32($il, $i+1)
        try {
            $str = $asm.ManifestModule.ResolveString($st)
            Write-Host "  ldstr: '$str'"
        } catch {}
    } elseif ($il[$i] -eq 0x28 -or $il[$i] -eq 0x6f) {
        $mt = [System.BitConverter]::ToInt32($il, $i+1)
        try {
            $mem = $asm.ManifestModule.ResolveMember($mt)
            Write-Host "  call: $($mem.DeclaringType.Name)::$($mem.Name)"
        } catch {}
    }
}
