# Script nhanh để chạy migrations trên Render Database
# Chạy file này từ thư mục gốc của dự án

$DatabaseUrl = "postgresql://code_do_user:AhJhY0xzA5hDDFLc8VvThh1dE3RiGXbs@dpg-d4v7vl3e5dus73a8sqtg-a.virginia-postgres.render.com:5432/elearning_r201"

Write-Host "🚀 Đang chạy migrations trên Render Database..." -ForegroundColor Cyan
Write-Host ""

& ".\scripts\run_migrations_render.ps1" -DatabaseUrl $DatabaseUrl

