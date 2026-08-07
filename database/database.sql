-- ==========================================================
-- Sports Ticket Reservation System
-- Database Project
-- DBMS : MySQL 8
-- ==========================================================

DROP DATABASE IF EXISTS SportsTicketDB;

CREATE DATABASE SportsTicketDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE SportsTicketDB;

-- ==========================================================
-- TABLE : Cities
-- ==========================================================

CREATE TABLE Cities(

    id INT AUTO_INCREMENT PRIMARY KEY,

    province VARCHAR(100) NOT NULL,

    city_name VARCHAR(100) NOT NULL

);

-- ==========================================================
-- TABLE : Users
-- ==========================================================

CREATE TABLE Users(

    id INT AUTO_INCREMENT PRIMARY KEY,

    first_name VARCHAR(100) NOT NULL,

    last_name VARCHAR(100) NOT NULL,

    email VARCHAR(150)  UNIQUE,

    phone VARCHAR(20)  UNIQUE,

    password VARCHAR(255) NOT NULL,

    role ENUM(
        'user',
        'support',
        'admin'
    ) DEFAULT 'user',

    city_id INT,

    birth_date DATE,

    profile_image VARCHAR(255),

    status ENUM(
        'active',
        'inactive'
    ) DEFAULT 'active',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT chk_user_contact
        CHECK (
            email IS NOT NULL
            OR
            phone IS NOT NULL
        ),
        
    CONSTRAINT fk_user_city
        FOREIGN KEY(city_id)
        REFERENCES Cities(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE

);

-- ==========================================================
-- TABLE : Sports
-- ==========================================================

CREATE TABLE Sports(

    id INT AUTO_INCREMENT PRIMARY KEY,

    sport_name VARCHAR(100) NOT NULL UNIQUE,

    description TEXT

);

-- ==========================================================
-- TABLE : Venues
-- ==========================================================

CREATE TABLE Venues(

    id INT AUTO_INCREMENT PRIMARY KEY,

    venue_name VARCHAR(150) NOT NULL,

    city_id INT NOT NULL,

    address VARCHAR(255),

    capacity INT NOT NULL,

    CONSTRAINT chk_capacity
        CHECK(capacity>0),

    CONSTRAINT fk_venue_city
        FOREIGN KEY(city_id)
        REFERENCES Cities(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

);


-- ==========================================================
-- TABLE : Teams
-- ==========================================================

CREATE TABLE Teams(
    id INT AUTO_INCREMENT PRIMARY KEY,

    team_name VARCHAR(120) NOT NULL UNIQUE,

    city_id INT,

    sport_id INT NOT NULL,

    CONSTRAINT fk_team_city
        FOREIGN KEY(city_id)
        REFERENCES Cities(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    CONSTRAINT fk_team_sport
        FOREIGN KEY(sport_id)
        REFERENCES Sports(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ==========================================================
-- TABLE : Matches
-- ==========================================================

CREATE TABLE Matches(

    id INT AUTO_INCREMENT PRIMARY KEY,

    sport_id INT NOT NULL,

	home_team_id INT NOT NULL,
	
    away_team_id INT NOT NULL,

    venue_id INT NOT NULL,

    match_date DATETIME NOT NULL,

    status ENUM(
        'Scheduled',
        'Finished',
        'Canceled'
    ) DEFAULT 'Scheduled',

    CONSTRAINT fk_match_sport
        FOREIGN KEY(sport_id)
        REFERENCES Sports(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_match_venue
        FOREIGN KEY(venue_id)
        REFERENCES Venues(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        
        
	CONSTRAINT fk_match_home_team
    FOREIGN KEY(home_team_id)
    REFERENCES Teams(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

	CONSTRAINT fk_match_away_team
    FOREIGN KEY(away_team_id)
    REFERENCES Teams(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

	CONSTRAINT chk_teams_diff
    CHECK (home_team_id <> away_team_id)

);


-- ==========================================================
-- TABLE : TicketTypes
-- ==========================================================

CREATE TABLE TicketTypes(

    id INT AUTO_INCREMENT PRIMARY KEY,

    type_name VARCHAR(100) UNIQUE NOT NULL,

    description TEXT

);

-- ==========================================================
-- TABLE : Tickets
-- ==========================================================

CREATE TABLE Tickets(

    id INT AUTO_INCREMENT PRIMARY KEY,

    match_id INT NOT NULL,

    ticket_type_id INT NOT NULL,

    price DECIMAL(10,2) NOT NULL,

    remaining_capacity INT NOT NULL,

    CONSTRAINT chk_remaining_capacity
        CHECK(remaining_capacity >= 0),

    CONSTRAINT fk_ticket_match
        FOREIGN KEY(match_id)
        REFERENCES Matches(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_ticket_type
        FOREIGN KEY(ticket_type_id)
        REFERENCES TicketTypes(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        
	CONSTRAINT chk_ticket_price CHECK(price >= 0)

);

-- ==========================================================
-- TABLE : FootballDetails
-- ==========================================================

CREATE TABLE FootballDetails(

    id INT AUTO_INCREMENT PRIMARY KEY,

    ticket_id INT NOT NULL UNIQUE,

    league VARCHAR(100),

    seat VARCHAR(20),

    seat_row INT,

    parking BOOLEAN DEFAULT FALSE,

    roof BOOLEAN DEFAULT FALSE,

    vip_service BOOLEAN DEFAULT FALSE,

    CONSTRAINT fk_football_ticket
        FOREIGN KEY(ticket_id)
        REFERENCES Tickets(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

);

-- ==========================================================
-- TABLE : BasketballDetails
-- ==========================================================

CREATE TABLE BasketballDetails(

    id INT AUTO_INCREMENT PRIMARY KEY,

    ticket_id INT NOT NULL UNIQUE,

    league VARCHAR(100),

    seat VARCHAR(20),

    seat_row INT,

    vip_service BOOLEAN DEFAULT FALSE,

    CONSTRAINT fk_basketball_ticket
        FOREIGN KEY(ticket_id)
        REFERENCES Tickets(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

);

-- ==========================================================
-- TABLE : VolleyballDetails
-- ==========================================================

CREATE TABLE VolleyballDetails(

    id INT AUTO_INCREMENT PRIMARY KEY,

    ticket_id INT NOT NULL UNIQUE,

    league VARCHAR(100),

    seat VARCHAR(20),

    seat_row INT,

    special_service BOOLEAN DEFAULT FALSE,

    CONSTRAINT fk_volleyball_ticket
        FOREIGN KEY(ticket_id)
        REFERENCES Tickets(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

);

-- ==========================================================
-- TABLE : Wallet
-- ==========================================================

CREATE TABLE Wallet(

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL UNIQUE,

    balance DECIMAL(12,2) DEFAULT 0,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_wallet_user
        FOREIGN KEY(user_id)
        REFERENCES Users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

);

-- ==========================================================
-- TABLE : Reservations
-- ==========================================================

CREATE TABLE Reservations(

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    ticket_id INT NOT NULL,

    status ENUM(
        'Reserved',
        'Paid',
        'Canceled',
        'Expired'
    ) DEFAULT 'Reserved',

    reserve_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    expire_time DATETIME NOT NULL,

    support_id INT NULL,

    CONSTRAINT chk_reserve_time
        CHECK(expire_time > reserve_time),

    CONSTRAINT fk_reservation_user
        FOREIGN KEY(user_id)
        REFERENCES Users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_reservation_ticket
        FOREIGN KEY(ticket_id)
        REFERENCES Tickets(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_support_user
        FOREIGN KEY(support_id)
        REFERENCES Users(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE

);

-- ==========================================================
-- TABLE : Payments
-- ==========================================================

CREATE TABLE Payments(

    id INT AUTO_INCREMENT PRIMARY KEY,

    reservation_id INT NOT NULL,

    user_id INT NOT NULL,

    amount DECIMAL(10,2) NOT NULL,

    payment_method ENUM(
        'BankCard',
        'Wallet',
        'Crypto'
    ) NOT NULL,

    payment_status ENUM(
        'Pending',
        'Success',
        'Failed'
    ) DEFAULT 'Pending',

    payment_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    transaction_code VARCHAR(120) UNIQUE,

    CONSTRAINT fk_payment_reservation
        FOREIGN KEY(reservation_id)
        REFERENCES Reservations(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_payment_user
        FOREIGN KEY(user_id)
        REFERENCES Users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        
	CONSTRAINT chk_payment_amount CHECK(amount >= 0)

);

-- ==========================================================
-- TABLE : Reports
-- ==========================================================

CREATE TABLE Reports(

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    reservation_id INT NULL,
    
	ticket_id INT NULL,

    category VARCHAR(100),

    description TEXT,

    status ENUM(
        'Pending',
        'Reviewed'
    ) DEFAULT 'Pending',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_report_user
        FOREIGN KEY(user_id)
        REFERENCES Users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_report_reservation
        FOREIGN KEY(reservation_id)
        REFERENCES Reservations(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
        
	
    CONSTRAINT fk_report_ticket
		FOREIGN KEY(ticket_id)
		REFERENCES Tickets(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
	
    CHECK(
    reservation_id IS NOT NULL
    OR
    ticket_id IS NOT NULL
	)

);

-- ==========================================================
-- TABLE : OTP
-- ==========================================================

CREATE TABLE OTP(

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    otp_code VARCHAR(10) NOT NULL,

    expire_at DATETIME NOT NULL,

    CONSTRAINT fk_otp_user
        FOREIGN KEY(user_id)
        REFERENCES Users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE

);

-- ==========================================================
-- INDEXES
-- ==========================================================

CREATE INDEX idx_users_email
ON Users(email);

CREATE INDEX idx_users_phone
ON Users(phone);

CREATE INDEX idx_matches_date
ON Matches(match_date);

CREATE INDEX idx_matches_status
ON Matches(status);

CREATE INDEX idx_tickets_price
ON Tickets(price);

CREATE INDEX idx_reservations_status
ON Reservations(status);

CREATE INDEX idx_payments_time
ON Payments(payment_time);

CREATE INDEX idx_reports_status
ON Reports(status);

-- ==========================================================
-- INSERT CITIES (10 rows)
-- ==========================================================
INSERT INTO Cities(province, city_name) VALUES
('Tehran','Tehran'),
('Isfahan','Isfahan'),
('Fars','Shiraz'),
('East Azerbaijan','Tabriz'),
('Razavi Khorasan','Mashhad'),
('Mazandaran','Sari'),
('Gilan','Rasht'),
('Khuzestan','Ahvaz'),
('Kerman','Kerman'),
('Qom','Qom');

-- ==========================================================
-- INSERT SPORTS (exactly 3 rows)
-- ==========================================================
INSERT INTO Sports(sport_name, description) VALUES
('Football','Football League'),
('Basketball','Basketball League'),
('Volleyball','Volleyball League');

-- ==========================================================
-- INSERT USERS (10 rows, roles: user/support/admin)
-- ==========================================================
INSERT INTO Users (first_name, last_name, email, phone, password, role, city_id, birth_date, status) VALUES
('Ali','Ahmadi','ali@example.com','09120000001','hashed_pw1','user',1,'2000-05-10','active'),
('Sara','Mohammadi','sara@example.com','09120000002','hashed_pw2','user',2,'1999-08-21','active'),
('Reza','Karimi','reza@example.com','09120000003','hashed_pw3','support',3,'1998-01-15','active'),
('Neda','Hosseini','neda@example.com','09120000004','hashed_pw4','user',4,'2001-11-09','active'),
('Mohammad','Rahimi','mohammad@example.com','09120000005','hashed_pw5','admin',5,'1995-02-18','active'),
('Fatemeh','Akbari','fatemeh@example.com','09120000006','hashed_pw6','user',6,'1997-03-11','active'),
('Hossein','Moradi','hossein@example.com','09120000007','hashed_pw7','user',7,'1996-12-20','active'),
('Maryam','Jafari','maryam@example.com','09120000008','hashed_pw8','user',8,'2002-04-04','active'),
('Amir','Yousefi','amir@example.com','09120000009','hashed_pw9','support',9,'1994-09-13','active'),
('Parisa','Soleimani','parisa@example.com','09120000010','hashed_pw10','user',10,'2003-06-27','active');

-- ==========================================================
-- INSERT VENUES (10 rows)
-- ==========================================================
INSERT INTO Venues (venue_name, city_id, address, capacity) VALUES
('Azadi Stadium',1,'Tehran, Azadi Blvd',78000),
('Naghsh-e Jahan Stadium',2,'Isfahan, Naqsh-e Jahan Sq',75000),
('Hafezieh Stadium',3,'Shiraz, Hafezieh St',20000),
('Yadegar-e Imam Stadium',4,'Tabriz, Imam Khomeini Blvd',66000),
('Imam Reza Stadium',5,'Mashhad, Vakilabad Blvd',27000),
('Shohada Stadium',6,'Sari, Shohada Sq',15000),
('Sardar Jangal Stadium',7,'Rasht, Sardar Jangal St',18000),
('Takhti Stadium',8,'Ahvaz, Takhti St',30000),
('Bahar Stadium',9,'Kerman, Bahar Blvd',12000),
('Qom Stadium',10,'Qom, Enghelab St',10000);

-- ==========================================================
-- INSERT TEAMS (10 rows, sport_id correct)
-- ==========================================================
INSERT INTO Teams (team_name, city_id, sport_id) VALUES
('Persepolis FC',1,1),           -- Football
('Esteghlal FC',1,1),            -- Football
('Sepahan SC',2,1),              -- Football
('Tractor SC',4,1),              -- Football
('Foolad Khuzestan',8,1),        -- Football
('Mahram Tehran',1,2),           -- Basketball
('Shahrdari Gorgan',6,2),        -- Basketball
('Paykan Tehran',1,3),           -- Volleyball
('Shahdab Yazd',NULL,3),         -- Volleyball (city not in list)
('Saipa Tehran',1,3);            -- Volleyball

-- ==========================================================
-- INSERT MATCHES (10 rows, sport matches teams)
-- ==========================================================
INSERT INTO Matches (sport_id, home_team_id, away_team_id, venue_id, match_date, status) VALUES
(1,1,2,1,'2026-08-15 18:00:00','Scheduled'),   -- Persepolis vs Esteghlal (Football)
(1,3,4,2,'2026-08-18 19:00:00','Scheduled'),   -- Sepahan vs Tractor (Football)
(1,5,1,3,'2026-08-20 18:30:00','Scheduled'),   -- Foolad vs Persepolis (Football)
(1,2,3,4,'2026-08-23 17:00:00','Scheduled'),   -- Esteghlal vs Sepahan (Football)
(1,4,5,5,'2026-08-26 20:00:00','Scheduled'),   -- Tractor vs Foolad (Football)
(2,6,7,6,'2026-09-02 16:00:00','Scheduled'),   -- Mahram vs Shahrdari Gorgan (Basketball)
(2,7,6,7,'2026-09-05 18:00:00','Scheduled'),   -- Shahrdari vs Mahram (Basketball)
(3,8,9,8,'2026-09-10 17:30:00','Scheduled'),   -- Paykan vs Shahdab Yazd (Volleyball)
(3,10,8,9,'2026-09-14 18:00:00','Scheduled'),  -- Saipa vs Paykan (Volleyball)
(3,9,10,10,'2026-09-18 18:00:00','Scheduled'); -- Shahdab vs Saipa (Volleyball)

-- ==========================================================
-- INSERT TICKET TYPES (10 rows)
-- ==========================================================
INSERT INTO TicketTypes (type_name, description) VALUES
('VIP','VIP Seat'),
('Premium','Premium Seat'),
('Standard','Standard Seat'),
('Economy','Economy Seat'),
('Student','Student Discount'),
('Family','Family Package'),
('Early Bird','Early Bird Discount'),
('Group','Group Discount'),
('Disabled','Accessible Seating'),
('Season','Season Pass');

-- ==========================================================
-- INSERT TICKETS (10 rows, each match gets at least one)
-- ==========================================================
INSERT INTO Tickets (match_id, ticket_type_id, price, remaining_capacity) VALUES
(1,1,1500000,200),   -- Football VIP
(2,2,900000,500),    -- Football Premium
(3,3,450000,700),    -- Football Standard
(4,4,300000,900),    -- Football Economy
(5,5,150000,500),    -- Football Student
(6,1,1200000,120),   -- Basketball VIP
(7,2,800000,400),    -- Basketball Premium
(8,3,450000,600),    -- Volleyball Standard
(9,4,300000,800),    -- Volleyball Economy
(10,1,1300000,180);  -- Volleyball VIP

-- ==========================================================
-- INSERT SPORT DETAILS (10 rows, no duplicate ticket_id)
-- ==========================================================
-- Football details (tickets 1-5)
INSERT INTO FootballDetails (ticket_id, league, seat, seat_row, parking, roof, vip_service) VALUES
(1,'Persian Gulf League','A12',1,TRUE,TRUE,TRUE),
(2,'Persian Gulf League','B15',3,FALSE,TRUE,FALSE),
(3,'Persian Gulf League','D8',2,TRUE,FALSE,FALSE),
(4,'Hazfi Cup','C18',4,FALSE,FALSE,FALSE),
(5,'Persian Gulf League','A5',1,TRUE,FALSE,TRUE);

-- Basketball details (tickets 6-7)
INSERT INTO BasketballDetails (ticket_id, league, seat, seat_row, vip_service) VALUES
(6,'Basketball Super League','B3',2,TRUE),
(7,'Basketball Super League','C4',3,FALSE);

-- Volleyball details (tickets 8-10)
INSERT INTO VolleyballDetails (ticket_id, league, seat, seat_row, special_service) VALUES
(8,'Volleyball League','D2',1,TRUE),
(9,'Volleyball League','E4',2,FALSE),
(10,'Volleyball League','F1',1,TRUE);

-- ==========================================================
-- INSERT WALLET (10 rows, one per user)
-- ==========================================================
INSERT INTO Wallet (user_id, balance) VALUES
(1,2500000),
(2,1800000),
(3,3500000),
(4,900000),
(5,10000000),
(6,750000),
(7,4200000),
(8,600000),
(9,5100000),
(10,1200000);

-- ==========================================================
-- INSERT RESERVATIONS (10 rows, support users are 3 and 9)
-- ==========================================================
INSERT INTO Reservations (user_id, ticket_id, status, expire_time, support_id) VALUES
(1,1,'Paid','2026-08-15 17:30:00',3),
(2,2,'Reserved','2026-08-18 18:30:00',3),
(3,3,'Paid','2026-08-20 18:00:00',9),
(4,4,'Canceled','2026-08-23 16:30:00',9),
(5,5,'Paid','2026-08-26 19:30:00',3),
(6,6,'Reserved','2026-09-02 15:30:00',9),
(7,7,'Paid','2026-09-05 17:30:00',3),
(8,8,'Reserved','2026-09-10 17:00:00',9),
(9,9,'Paid','2026-09-14 17:30:00',3),
(10,10,'Reserved','2026-09-18 17:30:00',9);

-- ==========================================================
-- INSERT PAYMENTS (10 rows, NULL transaction_code for non-success)
-- ==========================================================
INSERT INTO Payments (reservation_id, user_id, amount, payment_method, payment_status, transaction_code) VALUES
(1,1,1500000,'BankCard','Success','TXN100001'),
(3,3,450000,'Wallet','Success','TXN100002'),
(5,5,150000,'BankCard','Success','TXN100003'),
(7,7,800000,'Wallet','Success','TXN100004'),
(9,9,300000,'Wallet','Success','TXN100005'),
(2,2,900000,'BankCard','Pending',NULL),
(6,6,1200000,'Crypto','Failed',NULL),
(8,8,450000,'BankCard','Pending',NULL),
(10,10,1300000,'Wallet','Failed',NULL),
(4,4,300000,'BankCard','Failed',NULL);

-- ==========================================================
-- INSERT REPORTS (10 rows, constraint satisfied)
-- ==========================================================
INSERT INTO Reports (user_id, reservation_id, ticket_id, category, description, status) VALUES
-- Reports with only reservation_id
(2,2,NULL,'Payment','Payment is pending','Pending'),
(4,4,NULL,'Cancellation','Reservation canceled unexpectedly','Reviewed'),
(6,6,NULL,'Wallet','Wallet balance insufficient','Pending'),
(8,8,NULL,'Ticket','Incorrect ticket information','Pending'),
(10,10,NULL,'Support','Late support response','Reviewed'),
-- Reports with only ticket_id
(1,NULL,1,'Seat','Request seat upgrade','Pending'),
(3,NULL,3,'Refund','Double charge refund request','Reviewed'),
(5,NULL,5,'Venue','Wrong venue info on ticket','Pending'),
(7,NULL,7,'Payment','Wallet deducted but payment failed','Pending'),
(9,NULL,9,'Ticket','Duplicate ticket issued','Reviewed');

-- ==========================================================
-- INSERT OTP (10 rows, one per user)
-- ==========================================================
INSERT INTO OTP (user_id, otp_code, expire_at) VALUES
(1,'452781','2026-08-15 17:10:00'),
(2,'784512','2026-08-18 18:10:00'),
(3,'125487','2026-08-20 18:00:00'),
(4,'963258','2026-08-23 16:10:00'),
(5,'741852','2026-08-26 19:10:00'),
(6,'258963','2026-09-02 15:10:00'),
(7,'369147','2026-09-05 17:10:00'),
(8,'456123','2026-09-10 17:10:00'),
(9,'852456','2026-09-14 17:10:00'),
(10,'147369','2026-09-18 17:10:00');