USE SportsTicketDB;

DROP FUNCTION IF EXISTS GetUserFullName;
DROP FUNCTION IF EXISTS GetRemainingCapacity;
DROP FUNCTION IF EXISTS GetUserReservationCount;

DELIMITER $$

CREATE FUNCTION GetUserFullName(userId INT)
RETURNS VARCHAR(250)
DETERMINISTIC
BEGIN
    DECLARE fullname VARCHAR(250);

    SELECT CONCAT(first_name,' ',last_name)
    INTO fullname
    FROM Users
    WHERE id=userId;

    RETURN fullname;
END $$

CREATE FUNCTION GetRemainingCapacity(ticketId INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE cap INT;

    SELECT remaining_capacity
    INTO cap
    FROM Tickets
    WHERE id=ticketId;

    RETURN cap;
END $$

CREATE FUNCTION GetUserReservationCount(userId INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total INT;

    SELECT COUNT(*)
    INTO total
    FROM Reservations
    WHERE user_id=userId;

    RETURN total;
END $$

DELIMITER ;