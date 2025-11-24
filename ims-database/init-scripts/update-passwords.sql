-- UPDATE password hashes for existing user accounts
-- Run these SQL commands if you already have the database set up with old passwords

UPDATE users SET password_hash = '$2b$12$.6oSf2E6tWBi90pLze1fuOwmdhAKjaQ5Oew1BOVmV9bMqSJigTMIO' WHERE email = 'admin@example.com';
-- Password: Admin123

UPDATE users SET password_hash = '$2b$12$tdvrGlQg25Ch.Ya2UBZBhOl3Ti89/5RZFOoTdFzyRvHVzqFoiSxFC' WHERE email = 'staff1@example.com';
-- Password: Staff123

UPDATE users SET password_hash = '$2b$12$h7.hvQ3SZ4Xc64N.gJBzR.xAnwhALBUYeT4ey3obDmHe3hgYpaa0i' WHERE email = 'stock1@example.com';
-- Password: Stock123
