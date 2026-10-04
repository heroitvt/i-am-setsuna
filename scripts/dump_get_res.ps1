$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.ResourceManager')

$methods = $t.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly') | Where-Object { $_.Name -eq 'GetResource' }
foreach ($m in $methods) {
    Write-Host "GetResource params: $($m.GetParameters().Length)"
    $body = $m.GetMethodBody()
    if ($body) {
        $il = $body.GetILAsByteArray()
        for ($i=0; $i -lt $il.Length; $i++) {
            $b = $il[$i]
            if ($b -eq 0x28 -or $b -eq 0x6f) {
                $mt = [System.BitConverter]::ToInt32($il, $i+1)
                try {
                    $mem = $asm.ManifestModule.ResolveMember($mt)
                    Write-Host "  call: $($mem.DeclaringType.Name)::$($mem.Name)"
                } catch {}
            }
        }
    }
}
