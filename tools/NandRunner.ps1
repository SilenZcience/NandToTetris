param (
    [Parameter(Mandatory=$true)]
    [string]$simulatorCommand,

    [Parameter(Mandatory=$true, ValueFromRemainingArguments=$true)]
    [string[]]$testFiles
)

# Save the current code page
$currentCodePage = (chcp) -replace '[^\d]', ''

# Silently switch to UTF-8 (code page 65001)
$null = chcp 65001

try {
    if (-not (Get-Command $simulatorCommand -ErrorAction SilentlyContinue)) {
        Write-Error "Simulator command not found in PATH: $simulatorCommand"
        exit 1
    }

    foreach ($testFile in $testFiles) {
        if (-not (Test-Path $testFile)) {
            Write-Warning "Test file not found: $testFile — Skipping..."
            continue
        }

        Write-Host "`n--- Running test: $testFile ---"
        $output = & $simulatorCommand $testFile 2>&1 | Where-Object { $_ -notmatch "Active code page: 65001" }
        Write-Output $output
    }
}
finally {
    # Restore the original code page
    $null = chcp $currentCodePage
}
