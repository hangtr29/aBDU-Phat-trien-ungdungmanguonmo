# Hướng dẫn Commit lên GitHub

## Repository: https://github.com/hangtr29/Web-vnl.git

### Các bước thực hiện:

1. **Mở PowerShell/Terminal và chuyển vào thư mục Webhoctructuyen:**

   **Cách 1: Sử dụng dấu ngoặc kép (khuyến nghị)**
   ```powershell
   cd "D:\Nhóm 6_Webhoctructuyen\Webhoctructuyen"
   ```

   **Cách 2: Sử dụng Set-Location với -LiteralPath**
   ```powershell
   Set-Location -LiteralPath "D:\Nhóm 6_Webhoctructuyen\Webhoctructuyen"
   ```

   **Cách 3: Sử dụng tab completion (gõ một phần tên rồi nhấn Tab)**
   ```powershell
   cd D:\Nh<nhấn Tab để tự động hoàn thành>
   ```

   **Cách 4: Kéo thả thư mục vào PowerShell**
   - Mở File Explorer, tìm thư mục `Webhoctructuyen`
   - Kéo thả thư mục vào cửa sổ PowerShell
   - PowerShell sẽ tự động chuyển vào thư mục đó

2. **Khởi tạo Git (nếu chưa có):**
   ```bash
   git init
   ```

3. **Thêm remote repository:**
   ```bash
   git remote add origin https://github.com/hangtr29/Web-vnl.git
   ```
   (Nếu đã có remote, cập nhật bằng: `git remote set-url origin https://github.com/hangtr29/Web-vnl.git`)

4. **Thêm tất cả file vào staging:**
   ```bash
   git add .
   ```

5. **Commit:**
   ```bash
   git commit -m "Add Webhoctructuyen project"
   ```

6. **Đặt tên branch (nếu cần):**
   ```bash
   git branch -M main
   ```

7. **Push lên GitHub:**
   ```bash
   git push -u origin main
   ```

### Hoặc chạy script tự động:

**Cách 1: Chạy file .bat (Dễ nhất - Double-click)**
- Mở File Explorer
- Tìm file `commit_to_github.bat` trong thư mục `Webhoctructuyen`
- Double-click vào file để chạy
- Script sẽ tự động thực hiện tất cả các bước

**Cách 2: Chạy file PowerShell**
```powershell
cd "D:\Nhóm 6_Webhoctructuyen\Webhoctructuyen"
.\commit_to_github.ps1
```

**Cách 3: Chạy từ File Explorer**
- Mở File Explorer, tìm thư mục `Webhoctructuyen`
- Kéo thả thư mục vào PowerShell
- Chạy: `.\commit_to_github.ps1` hoặc `.\commit_to_github.bat`

### Lưu ý:
- Nếu chưa đăng nhập GitHub, bạn sẽ cần Personal Access Token
- Nếu repository đã có code, có thể cần pull trước: `git pull origin main --allow-unrelated-histories`

