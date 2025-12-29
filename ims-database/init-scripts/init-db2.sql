-- Sample data for new schema

-- Insert Users (Admin123, Staff123, Stock123)
INSERT INTO users (username, email, password_hash, full_name, phone, role, is_active) VALUES 
('admin', 'admin@example.com', '$2b$12$.6oSf2E6tWBi90pLze1fuOwmdhAKjaQ5Oew1BOVmV9bMqSJigTMIO', 'Nguyễn Văn Admin', '0901234567', 'MANAGER', TRUE),
('staff1', 'staff1@example.com', '$2b$12$tdvrGlQg25Ch.Ya2UBZBhOl3Ti89/5RZFOoTdFzyRvHVzqFoiSxFC', 'Trần Thị Nhân Viên', '0902345678', 'STAFF', TRUE),
('stock1', 'stock1@example.com', '$2b$12$h7.hvQ3SZ4Xc64N.gJBzR.xAnwhALBUYeT4ey3obDmHe3hgYpaa0i', 'Lê Văn Thủ Kho', '0903456789', 'STOCKKEEPER', TRUE);

-- Insert Categories
INSERT INTO categories (name, description) VALUES 
('Nước ngọt', 'Các loại nước giải khát có gas'),
('Snack', 'Đồ ăn vặt các loại'),
('Mì gói', 'Mì ăn liền'),
('Bánh kẹo', 'Bánh kẹo các loại'),
('Gia vị', 'Gia vị nấu ăn');

-- Insert Suppliers
INSERT INTO suppliers (name, contact_name, phone, address, email) VALUES 
('Công ty TNHH Coca Cola VN', 'Nguyễn Văn A', '0281234567', '123 Đường ABC, Q1, TP.HCM', 'contact@cocacola.vn'),
('Công ty CP Kido', 'Trần Thị B', '0282345678', '456 Đường DEF, Q2, TP.HCM', 'info@kido.com.vn'),
('Công ty TNHH Acecook VN', 'Lê Văn C', '0283456789', '789 Đường GHI, Q3, TP.HCM', 'sales@acecook.com.vn'),
('Công ty CP Kinh Đô', 'Phạm Thị D', '0284567890', '321 Đường JKL, Q4, TP.HCM', 'contact@kinhdo.com.vn'),
('Công ty TNHH Masan', 'Hoàng Văn E', '0285678901', '654 Đường MNO, Q5, TP.HCM', 'info@masan.com.vn');

-- Insert Products (created_by = 3 is stock1 - thủ kho)
INSERT INTO products (code, name, category_id, unit, import_price, selling_price, stock_quantity, created_by, is_active, description, supplier_id) VALUES 
('CC001', 'Coca Cola 330ml', 1, 'Lon', 6000, 8000, 100, 3, TRUE, 'Nước ngọt Coca Cola lon 330ml', 1),
('PP001', 'Pepsi 330ml', 1, 'Lon', 5500, 7500, 150, 3, TRUE, 'Nước ngọt Pepsi lon 330ml', 1),
('ST001', 'Sting Dâu 330ml', 1, 'Lon', 7000, 9000, 80, 3, TRUE, 'Nước tăng lực Sting vị dâu', 1),
('SN001', 'Snack Ostar Phô Mai', 2, 'Gói', 3000, 5000, 200, 3, TRUE, 'Snack khoai tây vị phô mai', 2),
('SN002', 'Snack Swing Cay', 2, 'Gói', 2500, 4000, 180, 3, TRUE, 'Snack bắp vị cay', 2),
('MI001', 'Hao Hao Tôm Chua Cay', 3, 'Gói', 3500, 5000, 300, 3, TRUE, 'Mì Hao Hao tôm chua cay', 3),
('MI002', 'Mì Kokomi Tôm', 3, 'Gói', 3000, 4500, 250, 3, TRUE, 'Mì Kokomi vị tôm', 5),
('BK001', 'Bánh Chocopie', 4, 'Hộp', 25000, 32000, 50, 3, TRUE, 'Bánh Chocopie hộp 12 cái', 4),
('BK002', 'Kẹo Alpenliebe', 4, 'Gói', 15000, 20000, 100, 3, TRUE, 'Kẹo sữa Alpenliebe', 4),
('GV001', 'Mắm Tôm Nam Ngư', 5, 'Chai', 18000, 25000, 60, 3, TRUE, 'Mắm tôm đặc biệt Nam Ngư 250g', 5);

-- Insert Customers
INSERT INTO customers (name, phone, address) VALUES 
('Nguyễn Thị Khách Hàng', '0911111111', '123 Nguyễn Văn Linh, Q7, TP.HCM'),
('Trần Văn Mua Sỉ', '0922222222', '456 Lê Văn Việt, Q9, TP.HCM'),
('Phạm Thị Thường Xuyên', '0933333333', '789 Võ Văn Kiệt, Q6, TP.HCM');

-- Insert Inventory Tickets (Nhập hàng)
INSERT INTO inventory_tickets (code, type, supplier_id, user_id, note) VALUES 
('NK001', 'IMPORT', 1, 3, 'Nhập hàng đợt 1 từ Coca Cola'),
('NK002', 'IMPORT', 3, 3, 'Nhập hàng mì gói từ Acecook'),
('XK001', 'EXPORT_CANCEL', NULL, 3, 'Xuất hủy hàng hết hạn'),
('KK001', 'STOCK_CHECK', NULL, 3, 'Kiểm kê định kỳ tháng 11');

-- Insert Inventory Ticket Details
INSERT INTO inventory_ticket_details (ticket_id, product_id, quantity, price) VALUES 
-- Nhập hàng đợt 1
(1, 1, 100, 6000),
(1, 2, 150, 5500),
(1, 3, 80, 7000),
-- Nhập hàng mì
(2, 6, 300, 3500),
(2, 7, 250, 3000),
-- Xuất hủy (số âm)
(3, 1, -5, NULL),
(3, 6, -10, NULL),
-- Kiểm kê điều chỉnh
(4, 1, 5, NULL),
(4, 4, -2, NULL);

-- Insert Orders (created by staff1 - user_id=2)
INSERT INTO orders (code, customer_id, user_id, total_amount, payment_method, status) VALUES 
('HD001', 1, 2, 45000, 'CASH', 'COMPLETED'),
('HD002', 2, 2, 180000, 'TRANSFER', 'COMPLETED'),
('HD003', 3, 2, 72000, 'CARD', 'COMPLETED');

-- Insert Order Details
INSERT INTO order_details (order_id, product_id, quantity, unit_price, cost_price, receive, give_back) VALUES 
-- HD001
(1, 1, 3, 8000, 6000, 24000, 0),
(1, 4, 2, 5000, 3000, 10000, 0),
(1, 6, 2, 5000, 3500, 10000, 0),
-- HD002 (mua sỉ nhiều)
(2, 6, 20, 5000, 3500, 100000, 0),
(2, 7, 20, 4500, 3000, 90000, 0),
-- HD003
(3, 1, 5, 8000, 6000, 40000, 0),
(3, 8, 1, 32000, 25000, 32000, 0);
