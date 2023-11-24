CREATE DATABASE ShooterGame;
USE ShooterGame;

CREATE TABLE player_profile(
	Username VARCHAR(50) PRIMARY KEY,
	Passkey VARCHAR(50)
);

CREATE TABLE player_statistics(
	Username VARCHAR(50) PRIMARY KEY,
    Accuracy FLOAT DEFAULT 0,
    Kills INT DEFAULT 0,
    Deaths INT DEFAULT 0,
    FOREIGN KEY(Username) REFERENCES player_profile(Username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE player_achievements(
	Username VARCHAR(50) PRIMARY KEY,
    Achievements VARCHAR(50) DEFAULT "",
    FOREIGN KEY(Username) REFERENCES player_profile(Username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Map(
	M_type VARCHAR(50) PRIMARY KEY,
    Enemy_type VARCHAR(50),
    Enemy_Colour LONGBLOB
);

CREATE TABLE Weapons(
	W_name VARCHAR(50) PRIMARY KEY,
    W_type VARCHAR(50),
    Damage INT,
    Map_type VARCHAR(50),
    FOREIGN KEY(Map_type) REFERENCES Map(M_type) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Items(
	Item_name VARCHAR(50) PRIMARY KEY,
    I_Description VARCHAR(100) 
);

CREATE TABLE Leaderboard(
	Username VARCHAR(50) PRIMARY KEY,
    Accuracy FLOAT DEFAULT 0,
    Total_kills INT DEFAULT 0,
    Score DOUBLE DEFAULT 0,
    FOREIGN KEY(Username) REFERENCES player_profile(Username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Prefers(
	Username VARCHAR(50),
    Item_name VARCHAR(50),
    PRIMARY KEY(Username, Item_name),
    FOREIGN KEY(Username) REFERENCES player_profile(Username) ON UPDATE CASCADE ON DELETE CASCADE, 
    FOREIGN KEY(Item_name) REFERENCES Items(Item_name) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Uses(
	Username VARCHAR(50),
    W_name VARCHAR(50),
    PRIMARY KEY(Username, W_name),
    FOREIGN KEY(Username) REFERENCES player_profile(Username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(W_name) REFERENCES Weapons(W_name) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Found_In(
	Item_name VARCHAR(50),
    M_type VARCHAR(50),
    PRIMARY KEY(Item_name, M_type),
    FOREIGN KEY(Item_name) REFERENCES Map(M_type) ON UPDATE CASCADE ON DELETE CASCADE
);

DELIMITER &&
CREATE TRIGGER UpdateLeaderboard
	BEFORE INSERT ON player_statistics
    FOR EACH ROW
    BEGIN 
    DECLARE new_accuracy FLOAT;
    DECLARE new_kills INT;
    DECLARE cur_user VARCHAR(50);
    UPDATE Leaderboard SET Accuracy = (Accuracy+NEW.Accuracy)/2 WHERE Username = NEW.Username;
    UPDATE Leaderboard SET Total_kills = (Total_kills + NEW.Kills) WHERE Username = NEW.Username;
    SELECT Accuracy INTO new_accuracy FROM Leaderboard WHERE Username = NEW.Username;
    SELECT Total_kills INTO new_kills FROM Leaderboard WHERE Username = NEW.Username;
    SELECT Username INTO cur_user FROM Leaderboard WHERE Username = NEW.Username;
    CALL update_score(new_accuracy, new_kills, cur_user);
    END; &&
DELIMITER ;

DELIMITER &&
CREATE TRIGGER UpdateRequirements
	AFTER INSERT ON player_profile
    FOR EACH ROW
    BEGIN
    INSERT INTO Leaderboard(`Username`) VALUES(NEW.Username);
    INSERT INTO player_achievements(`Username`) VALUES(NEW.Username);
    END; &&
DELIMITER ;

DELIMITER &&
CREATE PROCEDURE update_score(IN accuracy FLOAT, IN kills INT, IN cur_user VARCHAR(50))
	BEGIN
    UPDATE Leaderboard SET Score = Score + (accuracy*10 + total_kills) WHERE Username = cur_user;
    END; &&
DELIMITER ;
