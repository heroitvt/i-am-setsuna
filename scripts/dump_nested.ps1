$managed = 'd:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed'
[System.Reflection.Assembly]::LoadFrom("$managed\UnityEngine.dll") | Out-Null
$asm = [System.Reflection.Assembly]::LoadFrom("$managed\Assembly-CSharp.dll")
$t = $asm.GetType('Setsuna.ParameterManager')

foreach ($nested in $t.GetNestedTypes([System.Reflection.BindingFlags]'Public,NonPublic')) {
    Write-Host "Nested: $($nested.Name)"
    foreach ($m in $nested.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly')) {
        if ($m.Name -eq 'MoveNext') {
            Write-Host "  MoveNext in $($nested.Name):"
            $body = $m.GetMethodBody()
            if ($body) {
                $il = $body.GetILAsByteArray()
                for ($i=0; $i -lt $il.Length; $i++) {
                    $b = $il[$i]
                    if ($b -eq 0x72) {
                        $token = [System.BitConverter]::ToInt32($il, $i+1)
                        try {
                            $str = $asm.ManifestModule.ResolveString($token)
                            Write-Host "    ldstr: '$str'"
                        } catch {}
                    } elseif ($b -eq 0x28 -or $b -eq 0x6f) {
                        $token = [System.BitConverter]::ToInt32($il, $i+1)
                        try {
                            $member = $asm.ManifestModule.ResolveMember($token)
                            if ($member.Name -like '*Load*' -or $member.Name -like '*File*' -or $member.Name -like '*Cpk*' -or $member.Name -like '*Chapter*') {
                                Write-Host "    call: $($member.DeclaringType.Name)::$($member.Name)"
                            }
                        } catch {}
                    }
                }
            }
        }
    }
}
