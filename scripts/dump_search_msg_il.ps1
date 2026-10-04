$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.UiMessageWindow')

function DumpMethod($name) {
    Write-Host "=== $name ==="
    $m = $t.GetMethod($name, [System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static')
    if (-not $m) { Write-Host "Not found"; return }
    $body = $m.GetMethodBody()
    if (-not $body) { Write-Host "No body"; return }
    $il = $body.GetILAsByteArray()
    for ($i=0; $i -lt $il.Length; $i++) {
        $b = $il[$i]
        if ($b -eq 0x7B -or $b -eq 0x7E -or $b -eq 0x80) {
            $tok = [System.BitConverter]::ToInt32($il, $i+1)
            try {
                $f = $asm.ManifestModule.ResolveField($tok)
                Write-Host "  offset ${i}: ldfld $($f.DeclaringType.Name)::$($f.Name)"
            } catch {}
        } elseif ($b -eq 0x28 -or $b -eq 0x6f) {
            $tok = [System.BitConverter]::ToInt32($il, $i+1)
            try {
                $mem = $asm.ManifestModule.ResolveMember($tok)
                Write-Host "  offset ${i}: call $($mem.DeclaringType.Name)::$($mem.Name)"
            } catch {}
        } elseif ($b -eq 0x72) {
            $tok = [System.BitConverter]::ToInt32($il, $i+1)
            try {
                $str = $asm.ManifestModule.ResolveString($tok)
                Write-Host "  offset ${i}: ldstr '$str'"
            } catch {}
        }
    }
}

DumpMethod("get_mainPathTextData")
DumpMethod("SearchMessage")
DumpMethod("GetMessage")
