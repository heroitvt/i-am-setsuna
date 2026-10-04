$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.UiMessageWindow')

$allTypes = @($t) + $t.GetNestedTypes([System.Reflection.BindingFlags]'Public,NonPublic')
foreach ($typ in $allTypes) {
    foreach ($m in $typ.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly')) {
        $body = $m.GetMethodBody()
        if ($body) {
            $il = $body.GetILAsByteArray()
            for ($i=0; $i -lt $il.Length - 4; $i++) {
                if ($il[$i] -eq 0x7D) {
                    $tok = [System.BitConverter]::ToInt32($il, $i+1)
                    try {
                        $f = $asm.ManifestModule.ResolveField($tok)
                        if ($f.Name -like '*TextData*') {
                            Write-Host "Assigned in: $($typ.Name)::$($m.Name) -> $($f.Name)"
                        }
                    } catch {}
                }
            }
        }
    }
}
