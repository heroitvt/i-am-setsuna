$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.UiMessageWindow')

foreach ($m in $t.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly')) {
    if ($m.Name -like '*mainPath*' -or $m.Name -like '*conversation*' -or $m.Name -like '*subEvent*') {
        Write-Host "Method: $($m.Name)"
    }
}
