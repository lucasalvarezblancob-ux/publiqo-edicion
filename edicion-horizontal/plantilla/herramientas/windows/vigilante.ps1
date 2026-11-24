# Vigilante del analisis de referencias (Windows). Lo lanza cada 5 min la tarea programada "EdicionHorizontal-Vigilante"
# (instalar_vigilante.ps1). Solo toca NUESTROS procesos: los python/node/bash de la carpeta de edicion y lo que lancen
# (ffmpeg, ffprobe, yt-dlp). Cualquier otro proceso: solo se apunta en el log, nunca se cierra.
#   1) Apunta la RAM libre.
#   2) Recorta la memoria de trabajo (EmptyWorkingSet) de nuestros procesos: libera RAM sin cerrar nada.
#   3) Si la cola lleva > $MinColgado min sin latido (refs\dinamicos\_analisis\latido.json) o la RAM libre baja de
#      $RamMin %, mata el proceso de NUESTROS mas pesado y deja relanzar.flag: la siguiente "cola_refs.py avanzar" repite ese paso.
#   4) Procesos "No responde" que no son nuestros: solo aviso en el log.
param(
  [Parameter(Mandatory = $true)][string]$Carpeta,     # carpeta de edicion (la que tiene personal\LEEME.md)
  [int]$RamMin = 15, [int]$MinColgado = 10
)
$ErrorActionPreference = "SilentlyContinue"
$An = Join-Path $Carpeta "refs\dinamicos\_analisis"; New-Item -ItemType Directory -Force -Path $An | Out-Null
$Log = Join-Path $An "vigilante.log"
function Apunta($m) { "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $m" | Add-Content -Path $Log -Encoding utf8 }

Add-Type -Namespace Vig -Name Mem -MemberDefinition '[DllImport("psapi.dll")] public static extern bool EmptyWorkingSet(IntPtr h);'
$os = Get-CimInstance Win32_OperatingSystem
$libre = [math]::Round($os.FreePhysicalMemory * 100 / $os.TotalVisibleMemorySize, 1)

# "Nuestros" = los python/node/bash cuya linea de comandos o ejecutable esta en ESTA carpeta de edicion (en sus tres
# formas: C:\..., C:/... y /c/... de Git Bash) y todos sus descendientes (ffmpeg, ffprobe, yt-dlp que lanzan).
# Un ffmpeg o un python de otra carpeta o del sistema NO cuenta.
$carpetaN = (Resolve-Path $Carpeta).Path.ToLower().TrimEnd('\')
$formas = @($carpetaN, $carpetaN.Replace('\', '/'), ('/' + $carpetaN.Substring(0, 1) + $carpetaN.Substring(2).Replace('\', '/')))
$todos = Get-CimInstance Win32_Process
$raices = $todos | Where-Object {
  $n = $_.Name.ToLower(); $cl = "$($_.CommandLine)".ToLower(); $ex = "$($_.ExecutablePath)".ToLower()
  ($n -in @("python.exe", "pythonw.exe", "node.exe", "bash.exe", "sh.exe")) -and (@($formas | Where-Object { $cl.Contains($_) -or $ex.Contains($_) }).Count -gt 0)
}
$ids = New-Object System.Collections.Generic.HashSet[int]
foreach ($r in $raices) { [void]$ids.Add([int]$r.ProcessId) }
do {
  $antes = $ids.Count
  foreach ($p in $todos) { if ($ids.Contains([int]$p.ParentProcessId)) { [void]$ids.Add([int]$p.ProcessId) } }
} while ($ids.Count -gt $antes)
$nuestros = $todos | Where-Object { $ids.Contains([int]$_.ProcessId) }
$recortados = 0
foreach ($p in $nuestros) {
  $h = (Get-Process -Id $p.ProcessId).Handle
  if ($h) { if ([Vig.Mem]::EmptyWorkingSet($h)) { $recortados++ } }
}
$os2 = Get-CimInstance Win32_OperatingSystem
$libre2 = [math]::Round($os2.FreePhysicalMemory * 100 / $os2.TotalVisibleMemorySize, 1)

# latido de la cola
$colgado = $false; $paso = ""
$lat = Join-Path $An "latido.json"
if (Test-Path $lat) {
  $j = Get-Content $lat -Raw | ConvertFrom-Json
  $paso = "$($j.paso) $($j.video)"
  if ($j.pid -and $j.paso -ne "parado") {
    $edad = ((Get-Date) - [datetime]$j.hora).TotalMinutes
    $vivo = Get-Process -Id $j.pid
    if (-not $vivo) { Apunta "La cola (pid $($j.pid), $paso) ya no existe: hay que relanzar cola_refs.py avanzar"; New-Item -Force -Path (Join-Path $An "relanzar.flag") | Out-Null }
    elseif ($edad -gt $MinColgado) { $colgado = $true; Apunta "Cola sin latido desde hace $([math]::Round($edad)) min ($paso)" }
  }
}

if (($colgado -or $libre2 -lt $RamMin) -and $nuestros) {
  # el mas pesado de los nuestros que no sea la propia cola (la cola es la que relanza)
  $vic = $nuestros | Where-Object { "$($_.CommandLine)" -notmatch "cola_refs.py" } | Sort-Object WorkingSetSize -Descending | Select-Object -First 1
  if ($vic) {
    Stop-Process -Id $vic.ProcessId -Force
    New-Item -Force -Path (Join-Path $An "relanzar.flag") | Out-Null
    Apunta "MATADO $($vic.Name) pid $($vic.ProcessId) ($([math]::Round($vic.WorkingSetSize/1MB)) MB) - motivo: $(if ($colgado) {'colgado'} else {"RAM libre $libre2 %"}). Se repetira el paso."
  }
}

# procesos de otros que no responden: solo aviso
$noResp = Get-Process | Where-Object { $_.MainWindowHandle -ne 0 -and -not $_.Responding }
foreach ($p in $noResp) {
  if ($nuestros.ProcessId -notcontains $p.Id) { Apunta "AVISO: '$($p.ProcessName)' (pid $($p.Id)) no responde. No lo toco." }
}
Apunta "RAM libre $libre % -> $libre2 % (recortados $recortados de $(@($nuestros).Count) nuestros)$(if ($paso) {" - cola: $paso"})"
# el log no crece sin fin: se queda con las ultimas 2000 lineas
$l = Get-Content $Log; if ($l.Count -gt 2000) { $l | Select-Object -Last 2000 | Set-Content $Log -Encoding utf8 }
