import psycopg2
import os
class PostgreSQLProcessor:
    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        """Kết nối đến PostgreSQL"""
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor()
            print("Kết nối thành công!")
        except Exception as e:
            print("Lỗi kết nối:", e)

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            print("Database error:", e)
            self.conn.rollback()

    def create_table(self):
        """Tạo bảng users nếu chưa có"""
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            imge_path VARCHAR(300) UNIQUE NOT NULL,
            cost INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.execute_query(query)

    def insert_user(self, name, imge_path, cost):
        """Thêm một người dùng vào bảng"""
        query = "INSERT INTO users (name, imge_path, cost) VALUES (%s, %s, %s)"
        self.execute_query(query, (name, imge_path, cost))

    def update_user(self, obj_id, name=None, imge_path=None, cost=None):
        """Cập nhật thông tin người dùng"""
        query = "UPDATE users SET "
        params = []
        if name:
            query += "name = %s, "
            params.append(name)
        if email:
            query += "imge_path = %s, "
            params.append(imge_path)
        if age is not None:
            query += "cost = %s, "
            params.append(cost)
        
        query = query.rstrip(", ") + " WHERE id = %s"
        params.append(obj_id)

        self.execute_query(query, tuple(params))

    def delete_user(self, obj_id):
        """Xóa một object theo ID"""
        query = "DELETE FROM object WHERE id = %s"
        self.execute_query(query, (obj_id,))

    def fetch_users(self):
        """Lấy danh sách tất cả object"""
        query = "SELECT * FROM users"
        return self.fetch_query(query)

    def query_as_name(self,params=None):
        query = "SELECT * FROM users WHERE name = %s ;"
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchall()  # Lấy tất cả dữ liệu
                return result
        
        except Exception as e:
            print("Lỗi:", e)
            self.conn.rollback()
            return None

    def fetch_query(self, query, params=None):
        """Hàm thực thi truy vấn SELECT"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()
        except Exception as e:
            print("Lỗi:", e)
            return []

    def close_connection(self):
        """Đóng kết nối"""
        if self.conn:
            self.conn.close()
            print("Đã đóng kết nối!")

# ---------------------- Chạy thử ----------------------
if __name__ == "__main__":
    db = PostgreSQLProcessor(dbname="postgres", user="postgres", password="1")
    db.connect()
    db.create_table()
    
    # Thêm dữ liệu
    # db.insert_user(name="Bột giặt OMO 3Kg", imge_path="/home/minhanh/Downloads/project_home/img_sell_obj/BOT-GIAT-OMO-3-KG-BICH-1.jpg", cost = 150000)
    
    # Đọc dữ liệu
    # users = db.fetch_users()
    # params = ("Bột giặt OMO 3Kg",)
    # data = db.query_as_name(params)[0][3]
    # print("Danh sách users:", data)
    # Xóa dữ liệu
    # db.delete_user(1)
    folder_avatar_obj_sell = "/home/minhanh/Downloads/project_home/web_sell/media/image_avata_obj_sell"
    for folder_name in os.listdir(folder_avatar_obj_sell):
        folder_path = os.path.join(folder_avatar_obj_sell, folder_name)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                file_path = file_path.replace("/home/minhanh/Downloads/project_home/web_sell/", "/")
                print("file_path", file_path)
                name = folder_name
                imge_path = file_path
                cost = 150000
                db.insert_user(name=name, imge_path=imge_path, cost=cost)
    db.close_connection()
