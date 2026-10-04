$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")

$t = $asm.GetType('Setsuna.ParameterManager')
foreach ($f in $t.GetFields([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static')) {
    if ($f.Name -like '*Message*' -or $f.Name -like '*Story*' -or $f.Name -like '*Chapter*' -or $f.Name -like '*Scenario*') {
        Write-Host "Field: $($f.Name) Type: $($f.FieldType.FullName)"
    }
}
