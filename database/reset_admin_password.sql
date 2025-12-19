-- Reset password cho tài khoản admin
-- Password mới: admin123
-- Hash này lấy từ seed_users.sql (đã được verify)

-- Reset password cho admin@example.com
UPDATE users 
SET password_hash = '$2b$12$KPOLHSq0g2Y3onuFWkCnpON/7Irx05K3iO3cwB3obwhtcGewbdleS'
WHERE email = 'admin@example.com' AND role = 'admin';

-- Reset password cho TẤT CẢ admin accounts (nếu có nhiều admin)
UPDATE users 
SET password_hash = '$2b$12$KPOLHSq0g2Y3onuFWkCnpON/7Irx05K3iO3cwB3obwhtcGewbdleS'
WHERE role = 'admin';

-- Kiểm tra kết quả
SELECT id, email, ho_ten, role, is_active 
FROM users 
WHERE role = 'admin';

