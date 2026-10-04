[System.AppDomain]::CurrentDomain.add_AssemblyResolve({
    param($sender, $args)
    $name = $args.Name.Split(',')[0]
    $dir = "d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed"
    $path = Join-Path $dir "$name.dll"
    if (Test-Path $path) {
        return [System.Reflection.Assembly]::LoadFrom($path)
    }
    return $null
})

$asmPath = "d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll"
$asm = [System.Reflection.Assembly]::LoadFrom($asmPath)
$types = $asm.GetTypes()
foreach ($t in $types) {
    if ($t.Name -like "*ScenarioMessage*" -or $t.Name -like "*Parameter*") {
        Write-Host "$($t.FullName) : $($t.BaseType.Name)"
    }
}
