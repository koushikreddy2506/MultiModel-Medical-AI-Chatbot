@echo off
setlocal
rem One-file launcher. PowerShell code begins after the marker below.
set "MEDICAL_BAT_FILE=%~f0"
powershell -NoProfile -Command "$raw = Get-Content -LiteralPath $env:MEDICAL_BAT_FILE -Raw; $marker = [regex]::Match($raw, '(?m)^# POWERSHELL_START\r?$'); if (-not $marker.Success) { throw 'Launcher is incomplete.' }; & ([scriptblock]::Create($raw.Substring($marker.Index + $marker.Length)))"
exit /b %ERRORLEVEL%
# POWERSHELL_START
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$project = Split-Path -Parent $env:MEDICAL_BAT_FILE
Set-Location -LiteralPath $project
$venvPython = Join-Path $project '.venv\Scripts\python.exe'
$outputDir = Join-Path $project 'outputs'
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
$appOut = Join-Path $outputDir 'app.stdout.log'
$appErr = Join-Path $outputDir 'app.stderr.log'
$tunnelOut = Join-Path $outputDir 'tunnel.stdout.log'
$tunnelErr = Join-Path $outputDir 'tunnel.stderr.log'
$appProcess = $null
$tunnelProcess = $null
$exitCode = 0

try {
    if (-not (Test-Path -LiteralPath $venvPython)) {
        $candidates = @(
            @{ Command = 'py'; Prefix = @('-3.12') },
            @{ Command = 'py'; Prefix = @('-3.11') },
            @{ Command = 'py'; Prefix = @('-3.10') },
            @{ Command = 'python'; Prefix = @() }
        )
        $created = $false
        foreach ($candidate in $candidates) {
            $command = Get-Command $candidate.Command -ErrorAction SilentlyContinue
            if (-not $command) { continue }
            $prefix = $candidate.Prefix
            & $command.Source @prefix -c 'import sys; raise SystemExit(not ((3, 10) <= sys.version_info[:2] <= (3, 12)))' 2>$null
            if ($LASTEXITCODE -ne 0) { continue }
            Write-Host 'Creating Python virtual environment...'
            & $command.Source @prefix -m venv (Join-Path $project '.venv')
            if ($LASTEXITCODE -eq 0 -and (Test-Path -LiteralPath $venvPython)) {
                $created = $true
                break
            }
        }
        if (-not $created) {
            throw 'Python 3.10-3.12 was not found. Install Python 3.12, then run this file again.'
        }
    }

    Write-Host 'Installing or checking CPU app dependencies...'
    & $venvPython -m pip install --disable-pip-version-check -q -r (Join-Path $project 'requirements-cpu.txt')
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }

    $cloudflaredCommand = Get-Command cloudflared -ErrorAction SilentlyContinue
    $cloudflared = if ($cloudflaredCommand) { $cloudflaredCommand.Source } else { $null }
    if (-not $cloudflared) {
        $installed = 'C:\Program Files (x86)\cloudflared\cloudflared.exe'
        if (Test-Path -LiteralPath $installed) { $cloudflared = $installed }
    }
    if (-not $cloudflared) {
        $toolDir = Join-Path $project '.tools'
        New-Item -ItemType Directory -Path $toolDir -Force | Out-Null
        $cloudflared = Join-Path $toolDir 'cloudflared.exe'
        if (-not (Test-Path -LiteralPath $cloudflared)) {
            Write-Host 'Downloading Cloudflare Tunnel from its official GitHub release...'
            $download = 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe'
            Invoke-WebRequest -Uri $download -OutFile $cloudflared -UseBasicParsing
        }
    }
    & $cloudflared --version | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Cloudflare Tunnel could not start.' }

    $listener = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, 0)
    $listener.Start()
    $port = ([Net.IPEndPoint]$listener.LocalEndpoint).Port
    $listener.Stop()
    $localUrl = "http://127.0.0.1:$port"

    $env:HF_HOME = Join-Path $project '.hf-cache'
    $env:HF_HUB_DISABLE_SYMLINKS_WARNING = '1'
    $env:PYTHONUNBUFFERED = '1'
    Write-Host 'Starting the CPU vision app. First run may download model weights...'
    $appProcess = Start-Process -FilePath $venvPython -ArgumentList @('-u', 'app.py', '--cpu', '--port', "$port") -WorkingDirectory $project -WindowStyle Hidden -PassThru -RedirectStandardOutput $appOut -RedirectStandardError $appErr
    $deadline = (Get-Date).AddMinutes(8)
    $ready = $false
    while ((Get-Date) -lt $deadline) {
        if ($appProcess.HasExited) { throw "App stopped during startup. See $appErr" }
        try {
            $response = Invoke-WebRequest -Uri $localUrl -TimeoutSec 3 -UseBasicParsing
            if ($response.StatusCode -eq 200) { $ready = $true; break }
        } catch { }
        Start-Sleep -Seconds 2
    }
    if (-not $ready) { throw "App did not start within 8 minutes. See $appErr" }

    Write-Host "App ready at $localUrl. Creating the public link..."
    $tunnelProcess = Start-Process -FilePath $cloudflared -ArgumentList @('tunnel', '--url', $localUrl, '--no-autoupdate') -WorkingDirectory $project -WindowStyle Hidden -PassThru -RedirectStandardOutput $tunnelOut -RedirectStandardError $tunnelErr
    $deadline = (Get-Date).AddMinutes(2)
    $publicUrl = $null
    while ((Get-Date) -lt $deadline) {
        if ($tunnelProcess.HasExited) { throw "Tunnel stopped during startup. See $tunnelErr" }
        if (Test-Path -LiteralPath $tunnelErr) {
            $log = Get-Content -LiteralPath $tunnelErr -Raw -ErrorAction SilentlyContinue
            if ($log -match 'https://[a-z0-9-]+\.trycloudflare\.com') {
                $publicUrl = $Matches[0]
                break
            }
        }
        Start-Sleep -Seconds 2
    }
    if (-not $publicUrl) { throw "No public URL appeared within 2 minutes. See $tunnelErr" }

    $reachable = $false
    for ($attempt = 0; $attempt -lt 15; $attempt++) {
        try {
            $response = Invoke-WebRequest -Uri $publicUrl -TimeoutSec 10 -UseBasicParsing
            if ($response.StatusCode -eq 200) { $reachable = $true; break }
        } catch { }
        Start-Sleep -Seconds 2
    }
    if (-not $reachable) { throw "Public URL was created but could not be reached: $publicUrl" }

    Write-Host ''
    Write-Host 'WORKING PUBLIC LINK:' -ForegroundColor Green
    Write-Host $publicUrl -ForegroundColor Cyan
    Write-Host ''
    Write-Host 'Keep this window open. The link stops when you press Enter or close the computer.'
    Write-Host 'This is a temporary public link; do not upload private medical records.'
    Read-Host 'Press Enter to stop the app and tunnel' | Out-Null
} catch {
    Write-Host "Launch failed: $($_.Exception.Message)" -ForegroundColor Red
    if (Test-Path -LiteralPath $appErr) {
        Get-Content -LiteralPath $appErr -Tail 8 -ErrorAction SilentlyContinue
    }
    if (Test-Path -LiteralPath $tunnelErr) {
        Get-Content -LiteralPath $tunnelErr -Tail 8 -ErrorAction SilentlyContinue
    }
    $exitCode = 1
} finally {
    if ($tunnelProcess -and -not $tunnelProcess.HasExited) {
        Stop-Process -Id $tunnelProcess.Id -Force -ErrorAction SilentlyContinue
    }
    if ($appProcess -and -not $appProcess.HasExited) {
        Stop-Process -Id $appProcess.Id -Force -ErrorAction SilentlyContinue
    }
}
exit $exitCode
