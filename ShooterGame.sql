CREATE DATABASE ShooterGame;
USE ShooterGame;

CREATE TABLE player_profile(
	Username VARCHAR(50) PRIMARY KEY,
	Passkey VARCHAR(50)
);

CREATE TABLE player_statistics(
	Username VARCHAR(50) PRIMARY KEY,
    Accuracy FLOAT,
    Kills INT,
    Deaths INT,
    FOREIGN KEY(Username) REFERENCES player_profile(Username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE player_achievements(
	Username VARCHAR(50) PRIMARY KEY,
    Achievements VARCHAR(50),
    FOREIGN KEY(Username) REFERENCES player_profile(Username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Map(
	M_type VARCHAR(50) PRIMARY KEY,
    Enemy_type VARCHAR(50),
    Enemy_Colour VARCHAR(50)
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
    Accuracy FLOAT,
    Total_kills INT,
    Score DOUBLE,
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
	AFTER INSERT ON player_statistics
    FOR EACH ROW
    BEGIN 
    UPDATE Leaderboard SET Accuracy = (Accuracy+NEW.Accuracy)/2 WHERE Username = NEW.Username;
    UPDATE Leaderboard SET Total_kills = (Total_kills + NEW.Kills) WHERE Username = NEW.Username;
    UPDATE Leaderboard SET Score = (Total_kills + 10*Accuracy) WHERE Username = NEW.Username;
    END; &&
DELIMITER ;

