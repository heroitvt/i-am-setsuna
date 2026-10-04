$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")

foreach ($t in $asm.GetTypes()) {
    if ($t.Name -like '*Balloon*' -or $t.Name -like '*MessageWindow*') {
        Write-Host "Type: $($t.FullName)"
        foreach ($m in $t.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly')) {
            if ($m.Name -like '*Set*' -or $m.Name -like '*Show*' -or $m.Name -like '*Open*' -or $m.Name -like '*Text*') {
                Write-Host "  Method: $($m.Name)"
            }
        }
    }
}
