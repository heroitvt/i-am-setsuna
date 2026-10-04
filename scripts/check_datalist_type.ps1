$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")

$t = $asm.GetType('Setsuna.ParameterManager')
$f = $t.GetField('dataList', [System.Reflection.BindingFlags]'Public,NonPublic,Instance')
Write-Host "dataList FieldType: $($f.FieldType.FullName)"
foreach ($arg in $f.FieldType.GetGenericArguments()) {
    Write-Host "  GenericArg: $($arg.FullName)"
}
