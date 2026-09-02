[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$integrationRoot = Join-Path $repoRoot 'integrations'
$jsonExamples = Get-ChildItem -LiteralPath $integrationRoot -Recurse -File -Filter '*.json.example'

if ($jsonExamples.Count -eq 0) {
    throw 'No JSON MCP examples were found.'
}

foreach ($file in $jsonExamples) {
    $parsed = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($null -eq $parsed.mcpServers) {
        throw "$($file.FullName): missing mcpServers."
    }
}

$configExamples = Get-ChildItem -LiteralPath $integrationRoot -Recurse -File |
    Where-Object { $_.Name -like '*.json.example' -or $_.Name -like '*.toml.example' }

$forbiddenPatterns = @(
    '(?i)(?<![A-Za-z0-9])[A-Z]:[\\/]',
    '(?<![A-Za-z0-9:/\\])[\\/]{2}(?![.?\\/])',
    '(?i)api[_-]?key\s*[:=]',
    '(?i)bearer\s+[A-Za-z0-9._-]{12,}'
)

foreach ($file in $configExamples) {
    $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    foreach ($pattern in $forbiddenPatterns) {
        if ($content -match $pattern) {
            throw "$($file.FullName): contains a disallowed value or absolute path."
        }
    }
}

$tomlExamples = Get-ChildItem -LiteralPath $integrationRoot -Recurse -File -Filter '*.toml.example'
$commandPattern = '(?m)^[ \t]*command[ \t]*=[ \t]*"[^"]+"[ \t]*\r?$'
$crlfCommandProbe = "[mcp_servers.example]`r`ncommand = `"example`"`r`n"
if ($crlfCommandProbe -notmatch $commandPattern) {
    throw 'Internal command-entry validation does not accept CRLF input.'
}

foreach ($file in $tomlExamples) {
    $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    if ($content -notmatch '(?m)^\[mcp_servers\.') {
        throw "$($file.FullName): missing MCP server table."
    }
    if ($content -notmatch $commandPattern) {
        throw "$($file.FullName): missing command entry."
    }
}

Write-Host "Examples validated: JSON $($jsonExamples.Count), TOML $($tomlExamples.Count)"
