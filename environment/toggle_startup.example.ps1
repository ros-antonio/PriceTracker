# Enable or Disable the PriceTracker scheduled task
# Usage:
#   .\toggle_startup.ps1 enable
#   .\toggle_startup.ps1 disable
#   .\toggle_startup.ps1          (toggles current state)

param(
    [ValidateSet("enable", "disable")]
    [string]$Action
)

# Self-elevate to Administrator if not already
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    $args = "-ExecutionPolicy Bypass -File `"$PSCommandPath`""
    if ($Action) { $args += " -Action $Action" }
    Start-Process powershell -Verb RunAs -ArgumentList $args
    exit
}

$taskName = "PriceTracker"

# Check if task exists
$task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if (-not $task) {
    Write-Host "ERROR: Task '$taskName' not found. Run setup_startup.ps1 first." -ForegroundColor Red
    exit 1
}

# If no action specified, toggle
if (-not $Action) {
    if ($task.State -eq "Disabled") {
        $Action = "enable"
    } else {
        $Action = "disable"
    }
}

if ($Action -eq "enable") {
    Enable-ScheduledTask -TaskName $taskName | Out-Null
    Write-Host "Task '$taskName' ENABLED. It will run at next logon." -ForegroundColor Green
} else {
    Disable-ScheduledTask -TaskName $taskName | Out-Null
    Write-Host "Task '$taskName' DISABLED. It will NOT run at logon." -ForegroundColor Yellow
}
