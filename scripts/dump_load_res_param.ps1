$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.ResourceManager')
$m = ($t.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly') | Where-Object { $_.Name -eq 'LoadResourceParameter' })[0]

$body = $m.GetMethodBody()
$il = $body.GetILAsByteArray()
Write-Host "IL Bytes ($($il.Length)): $([System.BitConverter]::ToString($il))"
