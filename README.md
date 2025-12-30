# 🚀 RETAIL WEB APP - INVENTORY MANAGEMENT SYSTEM

## 📋 Yêu cầu đã có sẵn
- ✅ Docker Desktop (optional)
- ✅ Node.js & Next.js (v18+)
- ✅ Python 3.8+
- ✅ MySQL 8.0+ (local)
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
2. Chạy lần lượt 5 file SQL trong `ims-database/init-scripts/`

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

cd ..\inventory
pip install -r requirements.txt

cd ..\gateway
pip install -r requirements.txt
```

---

### **Bước 5: Chạy Backend Services**

**Mở 7 terminal riêng biệt (QUAN TRỌNG - phải chạy Gateway TRƯỚC):**

```powershell
# Terminal 1 - API Gateway (CHẠY ĐẦU TIÊN - Port 8000)
cd services\gateway
python gateway.py

# Terminal 2 - User Service (Port 8001)
cd services\user
python main.py

# Terminal 3 - Product Service (Port 8002)
cd services\product
python main.py

# Terminal 4 - Order Service (Port 8003)
cd services\order
python main.py

# Terminal 5 - Customer Service (Port 8004)
cd services\customer
python main.py

# Terminal 6 - Supplier Service (Port 8005)
cd services\supplier
python main.py
```

> **Lưu ý:** Mỗi service đã có uvicorn runner trong main.py, không cần gọi uvicorn trực tiếp.

---

### **Bước 6: Chạy Frontend (Next.js)**

```powershell
# Mở terminal mới (Terminal 8)
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

## 👤 TÀI KHOẢN MẪU

Hệ thống đã tạo sẵn 3 tài khoản để test với các vai trò khác nhau:

### 1. MANAGER (Quản lý)
- **Email:** `admin@example.com`
- **Password:** `Admin123`
- **Quyền:** Toàn quyền - quản lý user, xem báo cáo, duyệt phiếu kho, quản lý toàn bộ hệ thống

### 2. STAFF (Nhân viên bán hàng)
- **Email:** `staff1@example.com`
- **Password:** `Staff123`
- **Quyền:** Bán hàng, quản lý đơn hàng, quản lý khách hàng, xem sản phẩm

### 3. STOCKKEEPER (Thủ kho)
- **Email:** `stock1@example.com`
- **Password:** `Stock123`
- **Quyền:** Quản lý kho, nhập/xuất/kiểm kê hàng, quản lý nhà cung cấp

> **Lưu ý:** Đây là tài khoản demo, nên đổi password sau khi deploy production!

---

## 🔍 KIỂM TRA

### API Gateway:
- Gateway Health: http://localhost:8000/health

### Backend APIs:
- User Service: http://localhost:8001/docs
- Product Service: http://localhost:8002/docs
- Order Service: http://localhost:8003/docs
- Customer Service: http://localhost:8004/docs
- Supplier Service: http://localhost:8005/docs
- Inventory Service: http://localhost:8007/docs

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
- **Backend services** (port 8001-8007) chạy sau Gateway
- **MinIO** phải chạy liên tục (giữ terminal mở)
- **Frontend** gọi API qua Gateway (port 8000), không gọi trực tiếp tới services
- Tổng cộng cần **9 terminals**: 1 MinIO + 1 Gateway + 6 Services + 1 Frontend
- Nếu dùng Docker sau này, chỉ cần `docker-compose up`

---

## 🏗️ KIẾN TRÚC HỆ THỐNG

### Database Schema (9 bảng chính):
1. **users** - Quản lý người dùng (MANAGER, STAFF, STOCKKEEPER)
2. **categories** - Danh mục sản phẩm
3. **suppliers** - Nhà cung cấp
4. **products** - Sản phẩm (code, unit, import_price, selling_price, stock_quantity)
5. **customers** - Khách hàng
6. **orders** - Đơn hàng bán
7. **order_details** - Chi tiết đơn hàng
8. **inventory_tickets** - Phiếu nhập/xuất/kiểm kê kho
9. **inventory_ticket_details** - Chi tiết phiếu kho

### Microservices (6 services):
1. **User Service (8001)** - Xác thực, quản lý user, dashboard stats
2. **Product Service (8002)** - Quản lý sản phẩm và danh mục
3. **Order Service (8003)** - Quản lý đơn hàng bán
4. **Customer Service (8004)** - Quản lý khách hàng
5. **Supplier Service (8005)** - Quản lý nhà cung cấp
6. **Inventory Service (8007)** - Quản lý phiếu nhập/xuất/kiểm kê kho

### Roles & Permissions:
- **MANAGER** - Toàn quyền (quản lý user, xem báo cáo, duyệt phiếu kho)
- **STAFF** - Bán hàng, quản lý đơn hàng, khách hàng
- **STOCKKEEPER** - Quản lý kho, nhập/xuất/kiểm kê

### Key Features:
- ✅ JWT Authentication với Redis caching
- ✅ RBAC (Role-Based Access Control)
- ✅ Real-time inventory tracking
- ✅ Stored procedures for complex operations
- ✅ Database views for reporting
- ✅ MinIO for file storage
- ✅ Pydantic V2 models

---

## 🔄 THAY ĐỔI MỚI NHẤT

### Database Changes:
- ❌ Removed: `warehouses` table (simplified to single warehouse)
- ✅ Added: `inventory_tickets` và `inventory_ticket_details` tables
- ✅ Updated: All tables use `created_at/updated_at` (thay vì created_time/updated_time)
- ✅ Added: Role ENUM (MANAGER, STAFF, STOCKKEEPER) trong users table
- ✅ Added: 8 database views for reporting
- ✅ Added: Stored procedures (CreateOrderWithDetails, CreateInventoryTicketWithDetails)

### New Service:
- ✅ **Inventory Service** - Quản lý phiếu kho với 3 loại:
  - **IMPORT**: Nhập hàng từ nhà cung cấp
  - **EXPORT_CANCEL**: Xuất hủy hàng hỏng/lỗi
  - **STOCK_CHECK**: Kiểm kê điều chỉnh tồn kho

### Code Updates:
- ✅ All Pydantic models migrated to V2 (orm_mode → from_attributes)
- ✅ All services have uvicorn runner in main.py
- ✅ RBAC middleware implemented in shared/rbac.py
- ✅ Database utility classes standardized across services
