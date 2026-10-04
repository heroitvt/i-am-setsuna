$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.ParameterManager')

$m = ($t.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly') | Where-Object { $_.Name -eq 'GetParameter' })[0]
$body = $m.GetMethodBody()
$il = $body.GetILAsByteArray()

for ($i=0; $i -lt $il.Length; $i++) {
    $b = $il[$i]
    if ($b -eq 0x72) {
        $st = [System.BitConverter]::ToInt32($il, $i+1)
        try {
            $str = $asm.ManifestModule.ResolveString($st)
            Write-Host "[$i] ldstr: '$str'"
        } catch {}
    } elseif ($b -eq 0x28 -or $b -eq 0x6f) {
        $mt = [System.BitConverter]::ToInt32($il, $i+1)
        try {
            $mem = $asm.ManifestModule.ResolveMember($mt)
            Write-Host "[$i] call: $($mem.DeclaringType.Name)::$($mem.Name)"
        } catch {}
    }
}
Write-Host "GetParameter IL Bytes: $($il.Length)"
Write-Host ([System.BitConverter]::ToString($il))
