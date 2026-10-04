$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.ParameterManager')
$m = $t.GetMethod('GetParameter', [System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static', $null, @([string], [byte[]].MakeByRefType()), $null)
if (-not $m) {
    Write-Host "Overload not found, listing all GetParameter:"
    $t.GetMethods() | Where-Object { $_.Name -eq 'GetParameter' } | ForEach-Object { Write-Host $_ }
    exit
}
$body = $m.GetMethodBody()
$il = $body.GetILAsByteArray()
Write-Host "GetParameter IL length: $($il.Length)"
for ($i=0; $i -lt $il.Length; $i++) {
    $b = $il[$i]
    if ($b -eq 0x7B -or $b -eq 0x7E -or $b -eq 0x80) {
        $tok = [System.BitConverter]::ToInt32($il, $i+1)
        try {
            $f = $asm.ManifestModule.ResolveField($tok)
            Write-Host "  offset ${i}: ldfld $($f.DeclaringType.Name)::$($f.Name)"
        } catch {}
    } elseif ($b -eq 0x28 -or $b -eq 0x6f) {
        $tok = [System.BitConverter]::ToInt32($il, $i+1)
        try {
            $mem = $asm.ManifestModule.ResolveMember($tok)
            Write-Host "  offset ${i}: call $($mem.DeclaringType.Name)::$($mem.Name)"
        } catch {}
    }
}
