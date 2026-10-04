$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")

$t = $asm.GetType('Setsuna.ResourceManager+Resource')
foreach ($f in $t.GetFields([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static')) {
    Write-Host "Field: $($f.Name) Type: $($f.FieldType.FullName)"
}
