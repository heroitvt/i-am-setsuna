$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.ResourceManager')
if (!$t) {
    $t = $asm.GetTypes() | Where-Object { $_.Name -eq 'ResourceManager' }
}
Write-Host "Found ResourceManager: $($t.FullName)"
foreach ($m in $t.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly')) {
    if ($m.Name -like '*Load*' -or $m.Name -like '*Parameter*') {
        Write-Host "  Method: $($m.Name) ($($m.GetParameters().Length) params)"
    }
}
