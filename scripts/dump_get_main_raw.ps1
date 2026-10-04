$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.UiMessageWindow')
$m = $t.GetMethod('get_mainPathTextData', [System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static')
$body = $m.GetMethodBody()
$il = $body.GetILAsByteArray()
Write-Host "get_mainPathTextData IL length: $($il.Length)"
for ($i=0; $i -lt $il.Length; $i++) {
    Write-Host ("{0:X4}: {1:X2}" -f $i, $il[$i])
}
