$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.ParameterManager')

$m = ($t.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly') | Where-Object { $_.Name -eq 'GetCurrentStoryMessage' -and $_.GetParameters().Length -eq 2 })[0]
$body = $m.GetMethodBody()
$il = $body.GetILAsByteArray()

for ($i=0; $i -lt $il.Length - 4; $i++) {
    $b = $il[$i]
    if ($b -eq 0x7B -or $b -eq 0x7E) { # ldfld or ldsfld
        $tok = [System.BitConverter]::ToInt32($il, $i+1)
        try {
            $f = $asm.ManifestModule.ResolveField($tok)
            Write-Host "[$i] field: $($f.DeclaringType.Name)::$($f.Name) Type: $($f.FieldType.Name)"
        } catch {}
    }
}
