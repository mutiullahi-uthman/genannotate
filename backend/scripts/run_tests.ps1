$ErrorActionPreference = "Stop"

$backendDirectory = Split-Path -Parent $PSScriptRoot
Push-Location $backendDirectory
try {
    docker compose -f docker-compose.yml run --build --rm --no-deps api `
        python -m unittest discover -s tests -v
    $testExitCode = $LASTEXITCODE
}
finally {
    Pop-Location
}

exit $testExitCode
