$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.UiMessageWindow')

foreach ($p in $t.GetProperties([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static')) {
    Write-Host "Property: $($p.Name) Type: $($p.PropertyType.FullName)"
}
foreach ($f in $t.GetFields([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static')) {
    if ($f.Name -like '*Text*' -or $f.Name -like '*Msg*' -or $f.Name -like '*Data*') {
        Write-Host "Field: $($f.Name) Type: $($f.FieldType.FullName)"
    }
}
