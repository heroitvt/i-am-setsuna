$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.UI.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\SetsunaFontFix.dll")
$t = $asm.GetType('SetsunaFontFix.FontFixer')

foreach ($m in $t.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly')) {
    Write-Host "=== Method: $($m.Name) ==="
    $body = $m.GetMethodBody()
    if ($body) {
        $il = $body.GetILAsByteArray()
        Write-Host "Bytes: $([System.BitConverter]::ToString($il))"
    }
}
