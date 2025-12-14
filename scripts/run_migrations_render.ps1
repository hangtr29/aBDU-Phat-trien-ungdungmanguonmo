# Script để chạy migrations trên Render Database từ máy local
# Yêu cầu: External Database URL từ Render Dashboard

param(
    [Parameter(Mandatory=$true)]
    [string]$DatabaseUrl
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CHẠY MIGRATIONS TRÊN RENDER DATABASE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra psql
$psqlPath = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
if (-not (Test-Path $psqlPath)) {
    $psqlPath = "C:\Program Files\PostgreSQL\17\bin\psql.exe"
    if (-not (Test-Path $psqlPath)) {
        Write-Host "ERROR: Khong tim thay psql.exe" -ForegroundColor Red
        Write-Host "   Vui long cai dat PostgreSQL hoac su dung Render Shell" -ForegroundColor Yellow
        exit 1
    }
}

# Chuyển đổi URL nếu cần (postgresql+psycopg:// -> postgresql://)
if ($DatabaseUrl -match "postgresql\+psycopg://") {
    $DatabaseUrl = $DatabaseUrl -replace "postgresql\+psycopg://", "postgresql://"
}

Write-Host "Dang ket noi voi database..." -ForegroundColor Yellow
Write-Host "   URL: $($DatabaseUrl -replace ':[^:@]+@', ':****@')" -ForegroundColor Gray
Write-Host ""

# Test connection
Write-Host "Kiem tra ket noi..." -ForegroundColor Yellow
try {
    $testResult = & $psqlPath $DatabaseUrl -c "SELECT version();" 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) {
        throw "Connection failed"
    }
} catch {
    Write-Host "ERROR: Khong the ket noi voi database!" -ForegroundColor Red
    Write-Host $testResult -ForegroundColor Red
    Write-Host ""
    Write-Host "Goi y:" -ForegroundColor Yellow
    Write-Host "   1. Kiem tra External Database URL trong Render Dashboard" -ForegroundColor White
    Write-Host "   2. Dam bao External Access da duoc bat" -ForegroundColor White
    Write-Host "   3. Hoac su dung Render Shell (khuyen nghi)" -ForegroundColor White
    exit 1
}

Write-Host "Ket noi thanh cong!" -ForegroundColor Green
Write-Host ""

# Danh sách migrations
$migrations = @(
    "database/schema_pg.sql",
    "database/create_enrollment_table.sql",
    "database/create_notifications_table.sql",
    "database/create_payment_table.sql",
    "database/add_lesson_resources.sql",
    "database/add_diem_toi_da_to_bai_tap.sql",
    "database/create_deposit_transactions.sql",
    "database/add_deposit_fields.sql",
    "database/add_user_balance.sql"
)

# Tính project root: từ scripts/ lên 1 cấp
$projectRoot = Split-Path -Parent $PSScriptRoot
$successCount = 0
$failedCount = 0

Write-Host "Bat dau chay migrations..." -ForegroundColor Cyan
Write-Host ""

foreach ($migration in $migrations) {
    $fullPath = Join-Path $projectRoot $migration
    
    if (-not (Test-Path $fullPath)) {
        Write-Host "SKIP: $migration (file not found)" -ForegroundColor Yellow
        continue
    }
    
    Write-Host "Running: $migration..." -ForegroundColor Yellow
    
    # Chạy migration
    try {
        $result = & $psqlPath $DatabaseUrl -f $fullPath 2>&1 | Out-String
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   Completed: $migration" -ForegroundColor Green
            $successCount++
        } else {
            # Kiểm tra xem có phải lỗi "already exists" không
            $errorText = $result
            if ($errorText -match "already exists" -or $errorText -match "duplicate") {
                Write-Host "   Skipped (already exists): $migration" -ForegroundColor Yellow
                $successCount++
            } else {
                Write-Host "   ERROR in $migration" -ForegroundColor Red
                Write-Host $result -ForegroundColor Red
                $failedCount++
            }
        }
    } catch {
        Write-Host "   ERROR in $migration" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        $failedCount++
    }
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Migration Summary:" -ForegroundColor Cyan
Write-Host "   Success: $successCount" -ForegroundColor Green
Write-Host "   Failed: $failedCount" -ForegroundColor $(if ($failedCount -gt 0) { "Red" } else { "Green" })
Write-Host "========================================" -ForegroundColor Cyan

if ($failedCount -gt 0) {
    Write-Host ""
    Write-Host "Mot so migrations that bai. Vui long kiem tra loi o tren." -ForegroundColor Yellow
    exit 1
} else {
    Write-Host ""
    Write-Host "Tat ca migrations da hoan thanh thanh cong!" -ForegroundColor Green
    exit 0
}

