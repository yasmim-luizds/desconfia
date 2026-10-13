param([switch]$Demo)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$bundled = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies'
$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCommand) { $pythonExe = $pythonCommand.Source }
elseif (Test-Path "$bundled\python\python.exe") { $pythonExe = "$bundled\python\python.exe" }
else { throw 'Instale Python 3.12 ou superior e tente novamente.' }
if (!(Test-Path '.venv\Scripts\python.exe')) {
    & $pythonExe -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Não foi possível criar o ambiente Python.' }
}
$pythonExe = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
& $pythonExe -m pip install -r backend/requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar as dependências Python.' }
$pnpmCommand = Get-Command pnpm -ErrorAction SilentlyContinue
if ($pnpmCommand) { $pnpmExe = $pnpmCommand.Source }
elseif (Test-Path "$bundled\bin\fallback\pnpm.cmd") {
    $pnpmExe = "$bundled\bin\fallback\pnpm.cmd"
    $env:PATH = "$bundled\node\bin;" + $env:PATH
} else { throw 'Instale Node.js 22 e execute: npm install -g pnpm@11.25.0' }
& $pnpmExe --dir frontend install --frozen-lockfile
if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar o front-end.' }
& $pnpmExe --dir frontend build
if ($LASTEXITCODE -ne 0) { throw 'Falha ao preparar o front-end.' }
if ($Demo) { $env:AI_MODE = 'demo' } else { $env:AI_MODE = 'groq' }
Set-Location -LiteralPath (Join-Path $PSScriptRoot 'backend')
Write-Host 'Desconfia: abra http://127.0.0.1:8000. Ctrl+C encerra o servidor.'
& $pythonExe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
