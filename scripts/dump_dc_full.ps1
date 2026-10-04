$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")

$t = $asm.GetType('Setsuna.ResourceManager+<LoadResourceParameter>c__IteratorDC')
$m = $t.GetMethod('MoveNext', [System.Reflection.BindingFlags]'Public,NonPublic,Instance,DeclaredOnly')
$body = $m.GetMethodBody()
$il = $body.GetILAsByteArray()

Write-Host "Total bytes: $($il.Length)"
Write-Host ([System.BitConverter]::ToString($il))
