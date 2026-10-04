$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")

$t = $asm.GetType('Setsuna.ParameterManager')
$methods = $t.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,DeclaredOnly') | Where-Object { $_.Name -eq 'GetCurrentStoryMessage' }

foreach ($m in $methods) {
    Write-Host "GetCurrentStoryMessage ($($m.GetParameters().Length) params):"
    $body = $m.GetMethodBody()
    if ($body) {
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
                    $mem = $asm.ManifestModule.ResolveMember($mt)
                    Write-Host "  call: $($mem.DeclaringType.Name)::$($mem.Name)"
                } catch {}
            }
        }
    }
}
