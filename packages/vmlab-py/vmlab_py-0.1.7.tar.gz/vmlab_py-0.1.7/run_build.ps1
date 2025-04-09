# Build the Rust package using maturin
Write-Host "Building package with maturin..." -ForegroundColor Green
maturin build --release

# Get the latest wheel file
$wheelPath = Get-ChildItem -Path "C:\Users\gemin\rust_targets\wheels\vmlab_py-*.whl" | 
            Sort-Object LastWriteTime -Descending | 
            Select-Object -First 1

if ($wheelPath) {
    Write-Host "Installing wheel: $($wheelPath.Name)" -ForegroundColor Green
    pip install $wheelPath --force-reinstall

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Installation completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "Installation failed!" -ForegroundColor Red
    }
} else {
    Write-Host "No wheel file found!" -ForegroundColor Red
}

