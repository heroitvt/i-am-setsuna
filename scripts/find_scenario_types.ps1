$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")

foreach ($t in $asm.GetTypes()) {
    if ($t.Name -like '*Scenario*' -or $t.Name -like '*EventManager*' -or $t.Name -like '*MessageManager*') {
        Write-Host "Type: $($t.FullName)"
    }
}
