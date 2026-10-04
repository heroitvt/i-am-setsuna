$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")

$found = 0
foreach ($t in $asm.GetTypes()) {
    foreach ($m in $t.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static')) {
        $body = $m.GetMethodBody()
        if ($body) {
            $il = $body.GetILAsByteArray()
            for ($i=0; $i -lt $il.Length - 4; $i++) {
                if ($il[$i] -eq 0x28 -or $il[$i] -eq 0x6f) {
                    $tok = [System.BitConverter]::ToInt32($il, $i+1)
                    try {
                        $mem = $asm.ManifestModule.ResolveMember($tok)
                        if ($mem.DeclaringType.FullName -like '*FontFix*') {
                            Write-Host "FOUND CALL: $($t.FullName)::$($m.Name) -> $($mem.DeclaringType.FullName)::$($mem.Name)"
                            $found++
                        }
                    } catch {}
                }
            }
        }
    }
}

if ($found -eq 0) {
    Write-Host "NO CALLS TO FontFix FOUND ANYWHERE IN Assembly-CSharp.dll!"
}
