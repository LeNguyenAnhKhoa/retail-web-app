-- Procedure: Update Product Quantity
DELIMITER $$

DROP PROCEDURE IF EXISTS UpdateProductQuantity$$

CREATE PROCEDURE UpdateProductQuantity(
    IN p_product_id INT,
    IN p_quantity INT
)
BEGIN
    UPDATE products 
    SET stock_quantity = stock_quantity + p_quantity 
    WHERE product_id = p_product_id;
END $$

DELIMITER ;
