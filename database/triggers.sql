USE SportsTicketDB;

DROP TRIGGER IF EXISTS BeforeReservationInsert;
DROP TRIGGER IF EXISTS AfterPaymentSuccess;

DELIMITER $$

CREATE TRIGGER BeforeReservationInsert
BEFORE INSERT ON Reservations
FOR EACH ROW
BEGIN
    IF NEW.expire_time <= COALESCE(NEW.reserve_time, CURRENT_TIMESTAMP) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Expire time must be after reserve time';
    END IF;
END $$

CREATE TRIGGER AfterPaymentSuccess
AFTER UPDATE ON Payments
FOR EACH ROW
BEGIN
    IF NEW.payment_status = 'Success'
       AND OLD.payment_status <> 'Success' THEN

        UPDATE Reservations
        SET status = 'Paid'
        WHERE id = NEW.reservation_id;

    END IF;
END $$

DELIMITER ;