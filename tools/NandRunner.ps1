param (
    [Parameter(Mandatory = $true)]
    [string]$simulatorCommand,

    [Parameter(Mandatory = $true, ValueFromRemainingArguments = $true)]
    [string[]]$testPatterns
)

# Save current code page
$currentCodePage = (chcp) -replace '[^\d]', ''
$null = chcp 65001

try {
    if (-not (Get-Command $simulatorCommand -ErrorAction SilentlyContinue)) {
        Write-Error "Simulator command not found in PATH: $simulatorCommand"
        exit 1
    }

    # Expand wildcard patterns into test files
    $testFiles = @()
    foreach ($pattern in $testPatterns) {
        $resolved = Get-ChildItem -Path $pattern -File -ErrorAction SilentlyContinue
        if ($resolved) {
            $testFiles += $resolved.FullName
        } else {
            Write-Warning "No test files matched pattern: $pattern"
        }
    }

    if ($testFiles.Count -eq 0) {
        Write-Warning "No test files found. Exiting."
        exit 0
    }

    foreach ($testFile in $testFiles) {
        Write-Host "`n--- Running test: $testFile ---"
        $output = & $simulatorCommand $testFile 2>&1 | Where-Object { $_ -notmatch "Active code page: 65001" }
        Write-Output $output
    }
}
finally {
    # Restore original code page
    $null = chcp $currentCodePage
}
