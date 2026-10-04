$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")

foreach ($t in $asm.GetTypes()) {
    foreach ($m in $t.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly')) {
        $body = $m.GetMethodBody()
        if ($body) {
            $il = $body.GetILAsByteArray()
            for ($i=0; $i -lt $il.Length; $i++) {
                $b = $il[$i]
                if ($b -eq 0x28 -or $b -eq 0x6f) {
                    $mt = [System.BitConverter]::ToInt32($il, $i+1)
                    try {
                        $mem = $asm.ManifestModule.ResolveMember($mt)
                        if ($mem.Name -eq 'SearchData' -and $mem.DeclaringType.Name -eq 'ParameterManager') {
                            Write-Host "SearchData called from $($t.FullName)::$($m.Name)"
                        }
                    } catch {}
                }
            }
        }
    }
}
