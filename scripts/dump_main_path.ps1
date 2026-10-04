$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.UiMessageWindow')

$p = $t.GetProperty('mainPathTextData')
Write-Host "mainPathTextData PropertyType: $($p.PropertyType.FullName)"
$m = $p.GetGetMethod([System.Reflection.BindingFlags]'Public,NonPublic,Instance')
$body = $m.GetMethodBody()
$il = $body.GetILAsByteArray()

for ($i=0; $i -lt $il.Length - 4; $i++) {
    $b = $il[$i]
    if ($b -eq 0x7B -or $b -eq 0x7E) {
        $tok = [System.BitConverter]::ToInt32($il, $i+1)
        try {
            $f = $asm.ManifestModule.ResolveField($tok)
            Write-Host "  field: $($f.DeclaringType.Name)::$($f.Name) Type: $($f.FieldType.Name)"
        } catch {}
    } elseif ($b -eq 0x28 -or $b -eq 0x6f) {
        $tok = [System.BitConverter]::ToInt32($il, $i+1)
        try {
            $mem = $asm.ManifestModule.ResolveMember($tok)
            Write-Host "  call: $($mem.DeclaringType.Name)::$($mem.Name)"
        } catch {}
    }
}
