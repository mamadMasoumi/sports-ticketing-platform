USE SportsTicketDB;

DROP PROCEDURE IF EXISTS GetAllUsers;
DROP PROCEDURE IF EXISTS GetAllMatches;
DROP PROCEDURE IF EXISTS GetAllPayments;
DROP PROCEDURE IF EXISTS GetAllReservations;
DROP PROCEDURE IF EXISTS CountUsers;
DROP PROCEDURE IF EXISTS CountReservations;
DROP PROCEDURE IF EXISTS GetVenueRemainingCapacity;   -- renamed
DROP PROCEDURE IF EXISTS GetUserFullName;

-- ==========================================
-- STORED PROCEDURES
-- ==========================================

DELIMITER $$

CREATE PROCEDURE GetAllUsers()
BEGIN
    SELECT id, first_name, last_name, email, phone FROM Users;
END $$

CREATE PROCEDURE GetAllMatches()
BEGIN
    SELECT m.id,
           s.sport_name,
           home.team_name AS home_team,
           away.team_name AS away_team,
           v.venue_name,
           m.match_date,
           m.status
    FROM Matches m
    JOIN Sports s ON m.sport_id = s.id
    JOIN Venues v ON m.venue_id = v.id
    JOIN Teams home ON m.home_team_id = home.id
    JOIN Teams away ON m.away_team_id = away.id
    ORDER BY m.match_date;
END $$

CREATE PROCEDURE GetAllPayments()
BEGIN
    SELECT p.id, u.first_name, u.last_name, p.amount,
           p.payment_method, p.payment_status, p.payment_time
    FROM Payments p
    JOIN Users u ON p.user_id = u.id
    ORDER BY p.payment_time DESC;
END $$

CREATE PROCEDURE GetAllReservations()
BEGIN
    SELECT r.id, u.first_name, u.last_name,
           home.team_name AS home_team,
           away.team_name AS away_team,
           r.status
    FROM Reservations r
    JOIN Users u ON r.user_id = u.id
    JOIN Tickets t ON r.ticket_id = t.id
    JOIN Matches m ON t.match_id = m.id
    JOIN Teams home ON m.home_team_id = home.id
    JOIN Teams away ON m.away_team_id = away.id;
END $$

CREATE PROCEDURE CountUsers()
BEGIN
    SELECT COUNT(*) AS total_users FROM Users;
END $$

CREATE PROCEDURE CountReservations()
BEGIN
    SELECT COUNT(*) AS reservation_count FROM Reservations;
END $$

-- Renamed to avoid conflict/confusion with the function GetRemainingCapacity
CREATE PROCEDURE GetVenueRemainingCapacity(IN venueId INT)
BEGIN
    SELECT capacity - (
        SELECT COUNT(*)
        FROM Reservations r
        JOIN Tickets t ON r.ticket_id = t.id
        JOIN Matches m ON t.match_id = m.id
        WHERE m.venue_id = venueId
    ) AS remaining_capacity
    FROM Venues
    WHERE id = venueId;
END $$

CREATE PROCEDURE GetUserFullName(IN userId INT)
BEGIN
    SELECT CONCAT(first_name, ' ', last_name) AS full_name
    FROM Users
    WHERE id = userId;
END $$

DELIMITER ;