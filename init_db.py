"""
Script khởi tạo database và tạo tài khoản mặc định
Chạy: python init_db.py
"""
from werkzeug.security import generate_password_hash
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Khởi tạo database và tạo tài khoản mặc định"""
    try:
        # Kết nối MySQL (không chỉ định database)
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', '')
        )
        
        cursor = conn.cursor()
        
        # Đọc và chạy schema.sql
        print("Đang tạo database...")
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
            # Tách các câu lệnh
            for statement in sql_script.split(';'):
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except Error as e:
                        if "already exists" not in str(e).lower():
                            print(f"Warning: {e}")
        
        conn.commit()
        
        # Kết nối vào database đã tạo
        conn.close()
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DB', 'webhoctructuyen')
        )
        cursor = conn.cursor()
        
        # Tạo tài khoản admin
        admin_password_hash = generate_password_hash('admin123')
        cursor.execute("""
            INSERT IGNORE INTO users (ho_ten, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
        """, ('Admin', 'admin@example.com', admin_password_hash, 'admin'))
        
        # Tạo tài khoản giáo viên
        teacher_password_hash = generate_password_hash('teacher123')
        cursor.execute("""
            INSERT IGNORE INTO users (ho_ten, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
        """, ('Nguyễn Văn A', 'teacher@example.com', teacher_password_hash, 'teacher'))
        
        conn.commit()
        print("✅ Database đã được khởi tạo thành công!")
        print("\nTài khoản mặc định:")
        print("Admin: admin@example.com / admin123")
        print("Teacher: teacher@example.com / teacher123")
        
    except Error as e:
        print(f"❌ Lỗi: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    init_database()


