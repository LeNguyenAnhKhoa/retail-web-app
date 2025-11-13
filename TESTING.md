# 🧪 HƯỚNG DẪN TEST CHỨC NĂNG IMS

## 📱 CÁC CHỨC NĂNG CHÍNH

### 1. **Đăng nhập / Đăng ký**
- **Đăng ký**: Truy cập `/register` để tạo tài khoản mới
- **Đăng nhập**: Truy cập `/login` với username và password
- Sau khi đăng nhập thành công, token sẽ được lưu tự động

### 2. **Quản lý sản phẩm (Products)**
- **Xem danh sách**: Truy cập `/products` 
- **Thêm sản phẩm**: Click nút "Add Product", điền thông tin
- **Sửa sản phẩm**: Click biểu tượng edit trên từng sản phẩm
- **Xóa sản phẩm**: Click biểu tượng delete
- **Tìm kiếm**: Dùng thanh search để tìm theo tên/category/supplier

### 3. **Quản lý đơn hàng (Orders)**
- **Xem đơn hàng**: Truy cập `/orders`
- **Tạo đơn mới**: Click "Create Order", chọn khách hàng và sản phẩm
- **Cập nhật trạng thái**: Click vào đơn hàng để thay đổi status (Pending → Processing → Completed)
- **Tìm kiếm**: Tìm theo mã đơn (ORD-1000) hoặc tên khách hàng

### 4. **Quản lý khách hàng (Customers)**
- **Xem danh sách**: Truy cập `/customers`
- **Thêm khách hàng**: Click "Add Customer"
- **Sửa/Xóa**: Tương tự như Products

### 5. **Quản lý nhà cung cấp (Suppliers)**
- **Xem danh sách**: Truy cập `/suppliers`
- **Thêm/Sửa/Xóa**: Tương tự như Products

### 6. **Quản lý người dùng (Users)**
- **Xem danh sách**: Truy cập `/users` (chỉ Admin)
- **Thêm user mới**: Click "Add User"
- **Phân quyền**: Admin, Manager, Staff

---

## 🔍 XEM DỮ LIỆU TRONG DATABASE

### **Cách 1: Dùng MySQL Workbench**

```sql
-- Xem tất cả users
SELECT * FROM users;

-- Xem tất cả products
SELECT * FROM products;

-- Xem tất cả orders
SELECT * FROM orders;

-- Xem tất cả customers
SELECT * FROM customers;

-- Xem tất cả suppliers
SELECT * FROM suppliers;

-- Xem chi tiết đơn hàng (bao gồm sản phẩm)
SELECT o.order_id, o.order_date, o.total_amount, 
       c.customer_name, 
       p.product_name, oi.quantity, oi.unit_price
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;
```

### **Cách 2: Dùng API (Postman/Thunder Client)**

```bash
# Đăng nhập để lấy token
POST http://localhost:8000/api/user/login
Body: {"username": "admin", "password": "password123"}

# Lấy danh sách users (cần token)
GET http://localhost:8000/api/user/get-all-users
Header: Authorization: Bearer <your_token>

# Lấy danh sách products
GET http://localhost:8000/api/product/get-all-products?limit=100&offset=0

# Lấy danh sách orders
GET http://localhost:8000/api/order/get-all-orders
```

---

## 🎯 CÁCH THỰC HIỆN CÁC CHỨC NĂNG

### **Scenario 1: Đăng ký và đăng nhập**
1. Truy cập: `http://localhost:3000/register`
2. Điền: username, email, password, full_name
3. Click "Register"
4. Quay lại `/login` và đăng nhập

### **Scenario 2: Thêm sản phẩm mới**
1. Đăng nhập vào hệ thống
2. Truy cập `/products`
3. Click nút "Add Product"
4. Điền thông tin:
   - Product Name: Áo thun
   - Category: Clothes
   - Price: 150000
   - Stock: 100
   - Supplier: Chọn từ dropdown
5. Click "Save"

### **Scenario 3: Tạo đơn hàng**
1. Truy cập `/orders`
2. Click "Create Order"
3. Chọn khách hàng từ dropdown
4. Thêm sản phẩm:
   - Chọn sản phẩm
   - Nhập số lượng
   - Click "Add Item"
5. Kiểm tra tổng tiền
6. Click "Create Order"

### **Scenario 4: Xem báo cáo tồn kho**
1. Truy cập `/products`
2. Xem cột "Stock" để biết số lượng còn
3. Sản phẩm có stock < 10 sẽ hiển thị cảnh báo "Low Stock"

### **Scenario 5: Cập nhật trạng thái đơn hàng**
1. Truy cập `/orders`
2. Click vào một đơn hàng
3. Thay đổi status:
   - Pending → Processing (đang xử lý)
   - Processing → Completed (hoàn thành)
   - Hoặc → Cancelled (hủy)
4. Click "Update Status"

---

## 🔐 TÀI KHOẢN MẶC ĐỊNH (Nếu đã chạy init script)

```
Username: admin
Password: admin123
Role: Admin

Username: manager
Password: manager123
Role: Manager

Username: staff
Password: staff123
Role: Staff
```

---

## 🐛 TROUBLESHOOTING

### Lỗi "Unauthorized" khi gọi API
→ Kiểm tra token đã hết hạn chưa, đăng nhập lại

### Không hiển thị data
→ Kiểm tra MySQL đã chạy init scripts chưa

### Lỗi kết nối Redis
→ Kiểm tra Redis Cloud endpoint và password trong `.env`

### Không upload được ảnh
→ Kiểm tra MinIO đã chạy và đã tạo bucket `ims-bucket`

---

## 📞 LƯU Ý

- Mỗi lần thay đổi code backend cần restart service
- Frontend Next.js sẽ tự reload khi save file
- Database cần chạy 4 file init scripts theo thứ tự: `init-db1.sql` → `init-db2.sql` → `init-db3.sql` → `init-db4.sql`
- Token có thời hạn 24h, sau đó cần đăng nhập lại
