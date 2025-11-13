# 🚀 SETUP NHANH - IMS PROJECT

## 📋 Yêu cầu đã có sẵn
- ✅ Docker Desktop
- ✅ Node.js & Next.js
- ✅ MySQL (local)
- ✅ Redis Cloud (đã có endpoint)

## ⚡ CÀI ĐẶT & CHẠY

### **Bước 1: Cài đặt MinIO (Local) bằng powershell (chạy từng lệnh)** 

```powershell
# Tải MinIO cho Windows
Invoke-WebRequest -Uri "https://dl.min.io/server/minio/release/windows-amd64/minio.exe" -OutFile "$env:USERPROFILE\minio.exe"

# Tạo thư mục lưu data
mkdir $env:USERPROFILE\minio-data

# Chạy MinIO (mở terminal mới và giữ terminal này)
cd $env:USERPROFILE
.\minio.exe server .\minio-data --console-address ":9001"
```

**Truy cập MinIO Console:**
- URL: http://localhost:9001
- Username/Password: `minioadmin` / `minioadmin`
- Tạo bucket mới tên: `ims-bucket`

---

### **Bước 2: Tạo file `.env` trong thư mục gốc**

```bash
# MySQL (Local)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=ims_database
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_ROOT_PASSWORD=your_mysql_password

# Redis (Cloud)
REDIS_HOST=redis-19565.c292.ap-southeast-1-1.ec2.cloud.redislabs.com
REDIS_PORT=19565
REDIS_PASSWORD=your_redis_password
REDIS_DB=0

# MinIO (Local)
MINIO_URL=http://localhost:9000
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_BUCKET=ims-bucket

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
```

> **Lưu ý:** Thay `your_mysql_password` và `your_redis_password` bằng mật khẩu thực của bạn (root-password khi mới tải mysql).

---

### **Bước 3: Setup MySQL Database**

Dùng MySQL Workbench:
1. Tạo database mới: `ims_database`
2. Chạy lần lượt 4 file SQL trong `ims-database/init-scripts/`

---

### **Bước 4: Cài đặt Backend Services**

```powershell
# Cài Python dependencies cho từng service
cd services\user
pip install -r requirements.txt

cd ..\product
pip install -r requirements.txt

cd ..\order
pip install -r requirements.txt

cd ..\supplier
pip install -r requirements.txt

cd ..\customer
pip install -r requirements.txt
```

---

### **Bước 5: Chạy Backend Services**

**Mở 5 terminal riêng biệt:**

```powershell
# Terminal 1 - User Service
cd services\user
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2 - Product Service
cd services\product
uvicorn main:app --host 0.0.0.0 --port 8002 --reload

# Terminal 3 - Order Service
cd services\order
uvicorn main:app --host 0.0.0.0 --port 8003 --reload

# Terminal 4 - Supplier Service
cd services\supplier
uvicorn main:app --host 0.0.0.0 --port 8004 --reload

# Terminal 5 - Customer Service
cd services\customer
uvicorn main:app --host 0.0.0.0 --port 8005 --reload
```

---

### **Bước 6: Chạy Frontend (Next.js)**

```powershell
# Mở terminal mới
cd client

# Cài dependencies
npm install

# Chạy dev server
npm run dev
```

Frontend sẽ chạy tại: **http://localhost:3000**

---

## 🔍 KIỂM TRA

### Backend APIs:
- User Service: http://localhost:8001/docs
- Product Service: http://localhost:8002/docs
- Order Service: http://localhost:8003/docs
- Supplier Service: http://localhost:8004/docs
- Customer Service: http://localhost:8005/docs

### MinIO Console:
- http://localhost:9001

### Frontend:
- http://localhost:3000

---

## 🐛 XỬ LÝ LỖI

**Lỗi kết nối Redis:**
- Kiểm tra endpoint và password Redis Cloud
- Test connection: `redis-cli -h redis-19565.c292.ap-southeast-1-1.ec2.cloud.redislabs.com -p 19565 -a your_password`

**Lỗi MySQL:**
- Kiểm tra MySQL service đang chạy: `mysql -u root -p`
- Kiểm tra port 3306 có bị chiếm dụng không

**Lỗi MinIO:**
- Đảm bảo MinIO đang chạy (terminal không bị tắt)
- Đã tạo bucket `ims-bucket` trong console

---

## 📝 GHI CHÚ

- **Backend services** phải chạy TRƯỚC khi start frontend
- **MinIO** phải chạy liên tục (giữ terminal mở)
- Mỗi service cần 1 terminal riêng
- Nếu dùng Docker sau này, chỉ cần `docker-compose up`
