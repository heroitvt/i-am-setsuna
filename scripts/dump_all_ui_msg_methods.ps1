$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.UiMessageWindow')
$methods = $t.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static')
foreach ($m in $methods) {
    $params = ($m.GetParameters() | ForEach-Object { "$($_.ParameterType.Name) $($_.Name)" }) -join ', '
    Write-Host "$($m.ReturnType.Name) $($m.Name)($params)"
}
