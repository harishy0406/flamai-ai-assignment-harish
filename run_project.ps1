param(
    [switch]$SkipInstall,
    [switch]$Offline,
    [string]$Python = ""
)

$ErrorActionPreference = "Stop"

function Invoke-Step {
    param(
        [string]$Name,
        [scriptblock]$Command
    )

    Write-Host ""
    Write-Host "==> $Name" -ForegroundColor Cyan
    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "$Name failed with exit code $LASTEXITCODE"
    }
}

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot

if ([string]::IsNullOrWhiteSpace($Python)) {
    $VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    $Python = if (Test-Path $VenvPython) { $VenvPython } else { "python" }
}
$AnalysisMode = if ($Offline) { "reference" } else { "real" }
$CorpusArgs = if ($Offline) { @() } else { @("--source", "flores", "--sample-size", "250") }

Write-Host "Running FLAM AI audit project from $RepoRoot" -ForegroundColor Green
Write-Host "Python: $Python" -ForegroundColor DarkGray
Write-Host "Analysis mode: $AnalysisMode" -ForegroundColor DarkGray

if (-not $SkipInstall) {
    Invoke-Step "Upgrade pip" {
        & $Python -m pip install --upgrade pip
    }

    Invoke-Step "Install dependencies" {
        & $Python -m pip install -r requirements.txt
    }
}

Invoke-Step "Build corpus" {
    & $Python partA/corpus/build_corpus.py @CorpusArgs
}

Invoke-Step "Check starter-kit inputs" {
    & $Python partA/audit/experiments/exp_missing_inputs.py --mode inputs
}

Invoke-Step "Check audit inputs" {
    & $Python partA/audit/experiments/exp_missing_inputs.py --mode audit
}

Invoke-Step "Run whitespace audit experiment" {
    & $Python partA/audit/experiments/exp_whitespace_word_count.py
}

Invoke-Step "Run lowercasing audit experiment" {
    & $Python partA/audit/experiments/exp_lowercasing.py
}

Invoke-Step "Run NFC red-herring experiment" {
    & $Python partA/audit/experiments/exp_nfc_red_herring.py
}

Invoke-Step "Run corrected fertility analysis" {
    & $Python partA/analysis/corrected_fertility.py --mode $AnalysisMode
}

Invoke-Step "Check serving inputs" {
    & $Python partB/b3_goodput.py --check-only
}

Invoke-Step "Compute serving goodput" {
    & $Python partB/b3_goodput.py --batch-size 24 --prompt-len 3584
}

Invoke-Step "Generate throughput anomaly plot and Desmos equation" {
    & $Python partB/plot_anomaly.py
}

Invoke-Step "Validate Part C decision memo" {
    & $Python -c "from pathlib import Path; p=Path('partC/memo.md'); text=p.read_text(encoding='utf-8'); assert text.strip(), 'Part C memo is empty'; print(f'Part C memo: {p} ({len(text.split())} words)')"
}

Invoke-Step "Run ruff" {
    & $Python -m ruff check project_inputs.py partA partB partC
}

Invoke-Step "Compile Python files" {
    & $Python -m compileall project_inputs.py partA partB partC
}

Write-Host ""
Write-Host "Project run completed successfully." -ForegroundColor Green
Write-Host "Key outputs:"
Write-Host "- partA/corpus/processed/manifest.json"
Write-Host "- partA/analysis/results.csv"
Write-Host "- partA/analysis/a3_results.json"
Write-Host "- partB/plots/b2_long_context_anomaly.png"
Write-Host "- partB/plots/throughput_curve.tex"
Write-Host "- partC/memo.md"
