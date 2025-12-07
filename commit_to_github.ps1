# Script để commit thư mục Webhoctructuyen lên GitHub
# Repository: https://github.com/hangtr29/Web-vnl.git

# Chuyển vào thư mục Webhoctructuyen
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "Current directory: $(Get-Location)" -ForegroundColor Green

# Kiểm tra xem đã có git repository chưa
if (-not (Test-Path .git)) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
}

# Kiểm tra remote origin
$remoteUrl = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Adding remote origin..." -ForegroundColor Yellow
    git remote add origin https://github.com/hangtr29/Web-vnl.git
} else {
    Write-Host "Remote origin already exists: $remoteUrl" -ForegroundColor Cyan
    # Cập nhật URL nếu cần
    git remote set-url origin https://github.com/hangtr29/Web-vnl.git
}

# Thêm tất cả file vào staging
Write-Host "Adding files to staging..." -ForegroundColor Yellow
git add .

# Commit
Write-Host "Committing changes..." -ForegroundColor Yellow
$commitMessage = "Add Webhoctructuyen project"
git commit -m $commitMessage

# Kiểm tra branch hiện tại
$currentBranch = git branch --show-current
if (-not $currentBranch) {
    Write-Host "Creating main branch..." -ForegroundColor Yellow
    git branch -M main
    $currentBranch = "main"
}

# Push lên GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "Branch: $currentBranch" -ForegroundColor Cyan
git push -u origin $currentBranch

Write-Host "`nDone! Check your repository at: https://github.com/hangtr29/Web-vnl" -ForegroundColor Green

