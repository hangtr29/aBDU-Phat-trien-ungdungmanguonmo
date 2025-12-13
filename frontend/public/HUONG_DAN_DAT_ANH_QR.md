# 📸 Hướng dẫn đặt ảnh QR Code

## Bước 1: Chuẩn bị ảnh QR Code

Bạn cần có file ảnh QR code với:
- **Tên file**: `qr-code-payment.png` (hoặc `.jpg`, `.jpeg`)
- **Kích thước**: Khuyến nghị 300x300px trở lên
- **Format**: PNG hoặc JPG

## Bước 2: Đặt ảnh vào thư mục

Copy file ảnh QR code của bạn vào thư mục:
```
frontend/public/qr-code-payment.png
```

## Bước 3: Kiểm tra

1. Restart Frontend server (nếu đang chạy)
2. Refresh trang `/addfunds`
3. Ảnh QR code sẽ hiển thị ở cột giữa

## Lưu ý

- File phải có tên chính xác: `qr-code-payment.png`
- Đặt trực tiếp trong thư mục `frontend/public/` (không có thư mục con)
- Sau khi đặt file, có thể cần restart Vite dev server

## Nếu ảnh vẫn không hiển thị

1. Kiểm tra tên file có đúng không
2. Kiểm tra file có trong `frontend/public/` không
3. Mở Developer Tools (F12) → Console để xem lỗi
4. Thử dùng đường dẫn tuyệt đối: `http://localhost:3000/qr-code-payment.png`

