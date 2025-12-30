-- Script to remove Inventory Service tables and related objects
-- Run this script in your MySQL database (ims_database)

-- 1. Drop Views
DROP VIEW IF EXISTS stock_movement_view;
DROP VIEW IF EXISTS inventory_ticket_summary_view;

-- 2. Drop Stored Procedures
DROP PROCEDURE IF EXISTS CreateInventoryTicketWithDetails;

-- 3. Drop Tables
DROP TABLE IF EXISTS inventory_ticket_details;
DROP TABLE IF EXISTS inventory_tickets;

-- 4. Clean up any other references if needed (none found critical)
