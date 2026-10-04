$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")

$token = 0x060017F9
$member = $asm.ManifestModule.ResolveMember($token)
Write-Host "Resolved: $($member.DeclaringType.FullName)::$($member.Name)"

$iterType = $member.DeclaringType
$moveNext = $iterType.GetMethod('MoveNext', [System.Reflection.BindingFlags]'Public,NonPublic,Instance,DeclaredOnly')
$body = $moveNext.GetMethodBody()
$il = $body.GetILAsByteArray()
for ($i=0; $i -lt $il.Length; $i++) {
    $b = $il[$i]
    if ($b -eq 0x72) {
        $st = [System.BitConverter]::ToInt32($il, $i+1)
        try {
            $str = $asm.ManifestModule.ResolveString($st)
            Write-Host "  ldstr: '$str'"
        } catch {}
    } elseif ($b -eq 0x28 -or $b -eq 0x6f) {
        $mt = [System.BitConverter]::ToInt32($il, $i+1)
        try {
            $m = $asm.ManifestModule.ResolveMember($mt)
            Write-Host "  call: $($m.DeclaringType.Name)::$($m.Name)"
        } catch {}
    }
}
