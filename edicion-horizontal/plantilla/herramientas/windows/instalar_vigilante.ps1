# Instala (o quita) la tarea programada que lanza vigilante.ps1 cada 5 minutos, sin ventana, con tu usuario.
#   powershell -ExecutionPolicy Bypass -File herramientas\windows\instalar_vigilante.ps1 -Carpeta "C:\Users\...\Horizontal"
#   ... -Quitar        (la borra)
param([Parameter(Mandatory = $true)][string]$Carpeta, [switch]$Quitar, [int]$RamMin = 15, [int]$MinColgado = 10)
$Nombre = "EdicionHorizontal-Vigilante"
if ($Quitar) { schtasks /Delete /TN $Nombre /F; exit }
$Script = Join-Path $PSScriptRoot "vigilante.ps1"
$Accion = "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$Script`" -Carpeta `"$Carpeta`" -RamMin $RamMin -MinColgado $MinColgado"
schtasks /Create /TN $Nombre /TR $Accion /SC MINUTE /MO 5 /F | Out-Null
schtasks /Run /TN $Nombre | Out-Null
Start-Sleep -Seconds 8
schtasks /Query /TN $Nombre /FO LIST | Select-String "TaskName|Next Run|Próxima|Status|Estado"
$log = Join-Path $Carpeta "refs\dinamicos\_analisis\vigilante.log"
if (Test-Path $log) { "Última línea del log:"; Get-Content $log -Tail 1 } else { "Aún no hay log en $log (mira en 1 min)" }
