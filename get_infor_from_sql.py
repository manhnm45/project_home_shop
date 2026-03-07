import psycopg2
from psycopg2.extras import RealDictCursor
import os
# ====== THÔNG TIN KẾT NỐI ======
DB_CONFIG = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': '1',
        'host': 'localhost',  # Thường là 'localhost' hoặc IP của server PostgreSQL
        'port': '5432',  # Mặc định là '5432'
    }

def fetch_all_from_users():
    conn = None
    try:
        # 1. Kết nối PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Kết nối thành công")
        # 2. Tạo cursor
        # RealDictCursor giúp trả về dict thay vì tuple
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # 3. Query lấy tất cả các trường trong bảng A
        sql = "SELECT * FROM users;"
        cursor.execute(sql)

        # 4. Lấy dữ liệu
        rows = cursor.fetchall()

        print(rows[0]["name"])
        return rows

    except Exception as e:
        print("❌ Lỗi khi query DB:", e)
        return None

    finally:
        if conn:
            conn.close()
            print("🔌 Đã đóng kết nối DB")


def create_folder_image_for_search():
    folder_path = "./folder_data_search_image_relative_product_name/"
    os.makedirs(folder_path, exist_ok=True)
    rows = fetch_all_from_users()
    for row in rows:
        name = row["name"]
        os.makedirs(os.path.join(folder_path, name), exist_ok=True)

class Getinfo_from_sql():
    def __init__(self, user_name='postgres', password='1', host='localhost', port='5432', db_name='postgres'):
        self.user_name = user_name
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.db_config = {
            'dbname': self.db_name,
            'user': self.user_name,
            'password': self.password,
            'host': self.host,
            'port': self.port,
        }
        self.conn = psycopg2.connect(**self.db_config)

    def fetch_all_from_table(self, table_name):  
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        sql = f"SELECT * FROM {table_name};"
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    def get_cost_product(self, product_name, table_name="users"):
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        sql = f"SELECT cost FROM {table_name} WHERE name ='{product_name}';"
        cursor.execute(sql)
        row = cursor.fetchone()
        if row:
            return row["cost"]
        else:
            return None
    
if __name__ == "__main__":
    # fetch_all_from_users()
    create_folder_image_for_search()
    getinfo_sql = Getinfo_from_sql(user_name="postgres", password="1", host="localhost", port="5432", db_name="postgres")
    rows = getinfo_sql.fetch_all_from_table("users")
    print(rows)
    cost = getinfo_sql.get_cost_product("omachi", table_name="users")
    print(f"Cost of omachi: {cost}")
