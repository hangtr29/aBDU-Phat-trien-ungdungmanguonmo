-- Script tổng hợp để chạy tất cả migrations
-- Chạy trong psql: \i /path/to/run_all_migrations.sql
-- Hoặc copy-paste từng phần vào psql shell

-- ========================================
-- 1. Schema cơ bản
-- ========================================
\i D:/aWebhoctructuyen/Webhoctructuyen/database/schema_pg.sql

-- ========================================
-- 2. Tạo các bảng
-- ========================================
\i D:/aWebhoctructuyen/Webhoctructuyen/database/create_enrollment_table.sql
\i D:/aWebhoctructuyen/Webhoctructuyen/database/create_notifications_table.sql
\i D:/aWebhoctructuyen/Webhoctructuyen/database/create_payment_table.sql
\i D:/aWebhoctructuyen/Webhoctructuyen/database/create_deposit_transactions.sql
\i D:/aWebhoctructuyen/Webhoctructuyen/database/create_messages_table.sql

-- ========================================
-- 3. Thêm các cột
-- ========================================
\i D:/aWebhoctructuyen/Webhoctructuyen/database/add_lesson_resources.sql
\i D:/aWebhoctructuyen/Webhoctructuyen/database/add_diem_toi_da_to_bai_tap.sql
\i D:/aWebhoctructuyen/Webhoctructuyen/database/add_assignment_file.sql
\i D:/aWebhoctructuyen/Webhoctructuyen/database/add_discussion_image.sql
\i D:/aWebhoctructuyen/Webhoctructuyen/database/add_discussion_parent_id.sql
\i D:/aWebhoctructuyen/Webhoctructuyen/database/add_deposit_fields.sql
\i D:/aWebhoctructuyen/Webhoctructuyen/database/add_user_balance.sql

-- ========================================
-- 4. Fix các bảng (nếu cần)
-- ========================================
\i D:/aWebhoctructuyen/Webhoctructuyen/database/fix_notifications_table.sql

-- ========================================
-- 5. Seed data (tùy chọn)
-- ========================================
-- \i D:/aWebhoctructuyen/Webhoctructuyen/database/seed_users.sql
-- \i D:/aWebhoctructuyen/Webhoctructuyen/database/seed_programming_courses_fixed_utf8.sql
-- \i D:/aWebhoctructuyen/Webhoctructuyen/database/seed_lesson_resources.sql

-- ========================================
-- Hoàn thành!
-- ========================================
SELECT 'All migrations completed successfully!' AS status;

