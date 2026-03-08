# Setup PriceTracker to run at Windows startup via Task Scheduler
# Run this script once as Administrator: powershell -ExecutionPolicy Bypass -File .\setup_startup.ps1

$taskName = "PriceTracker"
$projectDir = "c:\ceva"
$pythonExe = "$projectDir\.venv\Scripts\pythonw.exe"
$scriptPath = "$projectDir\main.py"

# Verify paths exist
if (-not (Test-Path $pythonExe)) {
    Write-Host "ERROR: Python executable not found at $pythonExe" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $scriptPath)) {
    Write-Host "ERROR: main.py not found at $scriptPath" -ForegroundColor Red
    exit 1
}

# Remove existing task if it exists
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false # this removes it
    Write-Host "Removed existing task '$taskName'" -ForegroundColor Yellow
}

# Create the scheduled task
$action = New-ScheduledTaskAction `
    -Execute $pythonExe `
    -Argument $scriptPath `
    -WorkingDirectory $projectDir

$trigger = New-ScheduledTaskTrigger -AtLogon

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Runs PriceTracker script at user logon"

Write-Host "`nTask '$taskName' created successfully!" -ForegroundColor Green
Write-Host "The script will run automatically every time you log in." -ForegroundColor Cyan
Write-Host "`nTo remove it later, run:" -ForegroundColor Gray
Write-Host "  Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false" -ForegroundColor Gray
