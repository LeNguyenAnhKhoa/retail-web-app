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

cd ..\gateway
pip install -r requirements.txt
```

---

### **Bước 5: Chạy Backend Services**

**Mở 6 terminal riêng biệt (QUAN TRỌNG - phải chạy Gateway TRƯỚC):**

```powershell
# Terminal 1 - API Gateway (CHẠY ĐẦU TIÊN - Port 8000)
cd services\gateway
python gateway.py

# Terminal 2 - User Service
cd services\user
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 3 - Product Service
cd services\product
uvicorn main:app --host 0.0.0.0 --port 8002 --reload

# Terminal 4 - Order Service
cd services\order
uvicorn main:app --host 0.0.0.0 --port 8003 --reload

# Terminal 5 - Supplier Service
cd services\supplier
uvicorn main:app --host 0.0.0.0 --port 8004 --reload

# Terminal 6 - Customer Service
cd services\customer
uvicorn main:app --host 0.0.0.0 --port 8005 --reload
```

---

### **Bước 6: Chạy Frontend (Next.js)**

```powershell
# Mở terminal mới (Terminal 7)
cd client

# Cài dependencies (nếu chưa cài)
npm install

# Chạy dev server
npm run dev
```

Tạo file `.env.local` trong folder `/client` (nếu chưa có):

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

Frontend sẽ chạy tại: **http://localhost:3000**

---

## 🔍 KIỂM TRA

### API Gateway:
- Gateway Health: http://localhost:8000/health

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

**Lỗi "Failed to fetch" khi đăng ký/đăng nhập:**
- **Nguyên nhân:** Thiếu API Gateway (port 8000)
- **Giải pháp:** Chạy Gateway TRƯỚC các service khác (xem Bước 5)
- **Kiểm tra:** Truy cập http://localhost:8000/health phải thấy `{"status":"ok"}`

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

- **API Gateway (port 8000)** phải chạy TRƯỚC và LUÔN LUÔN chạy
- **Backend services** (port 8001-8005) chạy sau Gateway
- **MinIO** phải chạy liên tục (giữ terminal mở)
- **Frontend** gọi API qua Gateway (port 8000), không gọi trực tiếp tới services
- Tổng cộng cần **7 terminals**: 1 MinIO + 1 Gateway + 5 Services + 1 Frontend
- Nếu dùng Docker sau này, chỉ cần `docker-compose up`
