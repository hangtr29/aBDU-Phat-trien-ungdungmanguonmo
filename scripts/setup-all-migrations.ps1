# Script chay TAT CA migrations (bat buoc)
# Chay: .\scripts\setup-all-migrations.ps1

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SETUP DATABASE MIGRATIONS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Tim duong dan PostgreSQL
$psqlPath = $null
$possiblePaths = @(
    "C:\Program Files\PostgreSQL\18\bin\psql.exe",
    "C:\Program Files\PostgreSQL\17\bin\psql.exe",
    "C:\Program Files\PostgreSQL\16\bin\psql.exe",
    "C:\Program Files\PostgreSQL\15\bin\psql.exe",
    "C:\Program Files\PostgreSQL\14\bin\psql.exe",
    "C:\Program Files\PostgreSQL\13\bin\psql.exe"
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $psqlPath = $path
        break
    }
}

# Neu khong tim thay, thu tim trong PATH
if (-not $psqlPath) {
    $psqlInPath = Get-Command psql.exe -ErrorAction SilentlyContinue
    if ($psqlInPath) {
        $psqlPath = $psqlInPath.Source
    }
}

# Neu van khong tim thay, bao loi
if (-not $psqlPath) {
    Write-Host "LOI: Khong tim thay psql.exe!" -ForegroundColor Red
    Write-Host "Vui long:" -ForegroundColor Yellow
    Write-Host "  1. Them PostgreSQL bin vao PATH, hoac" -ForegroundColor Yellow
    Write-Host "  2. Sua duong dan trong script nay" -ForegroundColor Yellow
    exit 1
}

Write-Host "OK: Tim thay psql tai: $psqlPath" -ForegroundColor Green

$dbName = "elearning"
# Thử dùng postgres user trước, nếu không được thì dùng elearn
$dbUser = "postgres"
$projectRoot = Split-Path -Parent $PSScriptRoot

# Danh sach cac file migration BAT BUOC (theo thu tu)
$migrations = @(
    @{ File = "schema_pg.sql"; Name = "Schema co ban (bang users, khoa_hoc, ...)" },
    @{ File = "create_enrollment_table.sql"; Name = "Bang dang ky khoa hoc" },
    @{ File = "create_notifications_table.sql"; Name = "Bang thong bao" },
    @{ File = "create_payment_table.sql"; Name = "Bang thanh toan" },
    @{ File = "add_lesson_resources.sql"; Name = "Them cot tai lieu cho bai hoc" },
    @{ File = "add_diem_toi_da_to_bai_tap.sql"; Name = "Them cot diem toi da cho bai tap" },
    @{ File = "create_deposit_transactions.sql"; Name = "Bang giao dich nap tien" },
    @{ File = "add_deposit_fields.sql"; Name = "Them cac cot cho bang deposit_transactions" },
    @{ File = "add_user_balance.sql"; Name = "Them cot so du cho bang users" }
)

Write-Host ""
Write-Host "Se chay cac migrations sau:" -ForegroundColor Yellow
foreach ($migration in $migrations) {
    Write-Host "   - $($migration.Name)" -ForegroundColor Gray
}

$confirm = Read-Host "`nBan co muon tiep tuc? (y/n)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Da huy." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Bat dau chay migrations..." -ForegroundColor Green
Write-Host ""

foreach ($migration in $migrations) {
    $filePath = Join-Path $projectRoot (Join-Path "database" $migration.File)
    
    if (-not (Test-Path $filePath)) {
        Write-Host "Canh bao: File khong ton tai: $($migration.File)" -ForegroundColor Yellow
        continue
    }
    
    Write-Host "Dang chay: $($migration.Name)..." -ForegroundColor Cyan
    Write-Host "   File: $($migration.File)" -ForegroundColor Gray
    
    & $psqlPath -U $dbUser -d $dbName -f $filePath
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "LOI: Khi chay $($migration.File)!" -ForegroundColor Red
        Write-Host "   Vui long kiem tra lai va chay thu cong." -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "Hoan thanh: $($migration.Name)" -ForegroundColor Green
    Write-Host ""
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  HOAN THANH TAT CA MIGRATIONS!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Tiep theo:" -ForegroundColor Cyan
Write-Host "   - Chay seed data (tuy chon): .\scripts\setup-database.ps1" -ForegroundColor White
Write-Host "   - Hoac xem: docs\DATABASE_SETUP.md" -ForegroundColor White
Write-Host ""
