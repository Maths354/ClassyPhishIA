# Variables
$VENV_DIR = "venv"
$PYTHON = "$VENV_DIR\Scripts\python.exe"
$PIP = "$VENV_DIR\Scripts\pip.exe"
$GUNICORN = "$VENV_DIR\Scripts\gunicorn.exe"
$TESTS_DIR = "tests"
$REQUIREMENTS_FILE = "requirements.txt"

# Helper function to check if a command exists
function Command-Exists {
    param (
        [string]$command
    )
    $ErrorActionPreference = "Stop"
    try {
        $null = Get-Command $command -ErrorAction Stop
        return $true
    } catch {
        return $false
    } finally {
        $ErrorActionPreference = "Continue"
    }
}

# Target: venv
function venv {
    if (-Not (Test-Path $VENV_DIR)) {
        python -m venv $VENV_DIR
    }
}

# Target: install
function install {
    venv
    & $PIP install -r $REQUIREMENTS_FILE
}

# Target: add_datas
function add_datas {
    & $PYTHON "inject_db/inject_officialsite_datas.py"
}

# Target: run
function run {
    & $GUNICORN -w 4 -b localhost:8000 wsgi:app
}

# Target: dev
function dev {
    & $PYTHON "wsgi.py"
}

# Target: all
function all {
    install
    run
}

# Main script execution
param (
    [string]$target = "all"
)

switch ($target) {
    "all" { all }
    "venv" { venv }
    "install" { install }
    "add_datas" { add_datas }
    "run" { run }
    "dev" { dev }
    default { Write-Error "Unknown target: $target" }
}
