-- ==========================================
-- Sports Ticket Reservation System
-- Queries
-- ==========================================

USE SportsTicketDB;

-- ==========================================
-- Query 1
-- Users with no reservations
-- ==========================================

SELECT
    u.id,
    u.first_name,
    u.last_name
FROM Users u
LEFT JOIN Reservations r
ON u.id = r.user_id
WHERE r.user_id IS NULL;

-- ==========================================
-- Query 2
-- Users with paid reservations
-- ==========================================

SELECT DISTINCT
    u.id,
    u.first_name,
    u.last_name
FROM Users u
JOIN Reservations r
ON u.id = r.user_id
WHERE r.status='Paid';

-- ==========================================
-- Query 3
-- Reservation count for each user
-- ==========================================

SELECT
    u.id,
    u.first_name,
    u.last_name,
    COUNT(r.id) AS reservation_count
FROM Users u
LEFT JOIN Reservations r
ON u.id = r.user_id
GROUP BY
    u.id,
    u.first_name,
    u.last_name;

-- ==========================================
-- Query 4
-- Match information with team names
-- ==========================================

SELECT
    m.id,
    s.sport_name,
    ht.team_name AS home_team,
    at.team_name AS away_team,
    v.venue_name,
    m.match_date
FROM Matches m
JOIN Sports s ON m.sport_id = s.id
JOIN Venues v ON m.venue_id = v.id
JOIN Teams ht ON m.home_team_id = ht.id
JOIN Teams at ON m.away_team_id = at.id;

-- ==========================================
-- Query 5
-- Remaining ticket capacity
-- ==========================================

SELECT
    t.id,
    tt.type_name,
    t.price,
    t.remaining_capacity
FROM Tickets t
JOIN TicketTypes tt
ON t.ticket_type_id = tt.id;

-- ==========================================
-- Query 6
-- Successful Payments
-- ==========================================

SELECT
    p.id,
    u.first_name,
    u.last_name,
    p.amount,
    p.payment_method,
    p.payment_time
FROM Payments p
JOIN Users u
ON p.user_id = u.id
WHERE p.payment_status = 'Success';

-- ==========================================
-- Query 7
-- Upcoming Matches
-- ==========================================

SELECT
    m.id,
    ht.team_name AS home_team,
    at.team_name AS away_team,
    m.match_date
FROM Matches m
JOIN Teams ht ON m.home_team_id = ht.id
JOIN Teams at ON m.away_team_id = at.id
WHERE m.match_date > NOW()
ORDER BY m.match_date;

-- ==========================================
-- Query 8
-- Average Ticket Price per Match with Team Names
-- ==========================================

SELECT
    m.id,
    ht.team_name AS home_team,
    at.team_name AS away_team,
    AVG(t.price) AS average_price
FROM Matches m
JOIN Teams ht ON m.home_team_id = ht.id
JOIN Teams at ON m.away_team_id = at.id
JOIN Tickets t ON m.id = t.match_id
GROUP BY
    m.id,
    ht.team_name,
    at.team_name;

-- ==========================================
-- Query 9 
-- Ticket Count for Each Match
-- ==========================================

SELECT
    m.id,
    ht.team_name AS home_team,
    at.team_name AS away_team,
    COUNT(t.id) AS total_tickets
FROM Matches m
JOIN Teams ht ON m.home_team_id = ht.id
JOIN Teams at ON m.away_team_id = at.id
LEFT JOIN Tickets t ON m.id = t.match_id
GROUP BY
    m.id,
    ht.team_name,
    at.team_name;

-- ==========================================
-- Query 10
-- Total Revenue
-- ==========================================

SELECT
    SUM(amount) AS total_revenue
FROM Payments
WHERE payment_status='Success';

-- ==========================================
-- Query 11
-- Number of Payments by Payment Method
-- ==========================================

SELECT
    payment_method,
    COUNT(*) AS total_payments
FROM Payments
GROUP BY payment_method;

-- ==========================================
-- Query 12
-- Payment Status Report
-- ==========================================

SELECT
    payment_status,
    COUNT(*) AS total
FROM Payments
GROUP BY payment_status;

-- ==========================================
-- Query 13
-- Number of Matches for Each Sport
-- ==========================================

SELECT
    s.sport_name,
    COUNT(m.id) AS total_matches
FROM Sports s
LEFT JOIN Matches m
ON s.id = m.sport_id
GROUP BY
    s.id,
    s.sport_name;

-- ==========================================
-- Query 14
-- Users in Each City
-- ==========================================

SELECT
    c.city_name,
    COUNT(u.id) AS total_users
FROM Cities c
LEFT JOIN Users u
ON c.id = u.city_id
GROUP BY
    c.id,
    c.city_name;

-- ==========================================
-- Query 15
-- Most Expensive Ticket
-- ==========================================

SELECT
    t.id,
    ht.team_name AS home_team,
    at.team_name AS away_team,
    tt.type_name,
    t.price
FROM Tickets t
JOIN Matches m ON t.match_id = m.id
JOIN Teams ht ON m.home_team_id = ht.id
JOIN Teams at ON m.away_team_id = at.id
JOIN TicketTypes tt ON t.ticket_type_id = tt.id
ORDER BY t.price DESC
LIMIT 1;

-- ==========================================
-- Query 16
-- User Total Payments
-- ==========================================

SELECT
    u.id,
    u.first_name,
    u.last_name,
    SUM(p.amount) AS total_amount
FROM Users u
JOIN Payments p
ON u.id = p.user_id
WHERE p.payment_status = 'Success'
GROUP BY
    u.id,
    u.first_name,
    u.last_name
ORDER BY total_amount DESC;

-- ==========================================
-- Query 17
-- Reservations by Status
-- ==========================================

SELECT
    status,
    COUNT(*) AS total
FROM Reservations
GROUP BY status;

-- ==========================================
-- Query 18
-- Matches in Each Venue
-- ==========================================

SELECT
    v.venue_name,
    COUNT(m.id) AS total_matches
FROM Venues v
LEFT JOIN Matches m
ON v.id = m.venue_id
GROUP BY
    v.id,
    v.venue_name;

-- ==========================================
-- Query 19
-- Average Price by Ticket Type
-- ==========================================

SELECT
    tt.type_name,
    AVG(t.price) AS average_price
FROM TicketTypes tt
JOIN Tickets t
ON tt.id = t.ticket_type_id
GROUP BY
    tt.id,
    tt.type_name;

-- ==========================================
-- Query 20
-- Users by Registration Date
-- ==========================================

SELECT
    id,
    first_name,
    last_name,
    created_at
FROM Users
ORDER BY created_at;

-- ==========================================
-- Query 21
-- Matches by Sport
-- ==========================================

SELECT
    s.sport_name,
    ht.team_name AS home_team,
    at.team_name AS away_team,
    m.match_date
FROM Sports s
JOIN Matches m ON s.id = m.sport_id
JOIN Teams ht ON m.home_team_id = ht.id
JOIN Teams at ON m.away_team_id = at.id
ORDER BY
    s.sport_name,
    m.match_date;

-- ==========================================
-- Query 22
-- Reservation Report
-- ==========================================

SELECT
    r.id AS reservation_id,
    u.first_name,
    u.last_name,
    ht.team_name AS home_team,
    at.team_name AS away_team,
    tt.type_name,
    p.amount,
    r.status
FROM Reservations r
JOIN Users u ON r.user_id = u.id
JOIN Tickets t ON r.ticket_id = t.id
JOIN Matches m ON t.match_id = m.id
JOIN Teams ht ON m.home_team_id = ht.id
JOIN Teams at ON m.away_team_id = at.id
JOIN TicketTypes tt ON t.ticket_type_id = tt.id
LEFT JOIN Payments p ON r.id = p.reservation_id;




