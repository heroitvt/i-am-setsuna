@echo off
set CSC=C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe
set MANAGED=d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed
set SRC=d:\Viet Hoa Game\temp_scripts\FontFixer.cs
set OUT=d:\Viet Hoa Game\temp_scripts\SetsunaFontFix.dll

"%CSC%" /noconfig /target:library /nostdlib+ /reference:"%MANAGED%\mscorlib.dll" /reference:"%MANAGED%\System.dll" /reference:"%MANAGED%\UnityEngine.dll" /reference:"%MANAGED%\UnityEngine.UI.dll" /out:"%OUT%" "%SRC%"
if %errorlevel% equ 0 (
    echo Compilation succeeded!
) else (
    echo Compilation failed!
)
