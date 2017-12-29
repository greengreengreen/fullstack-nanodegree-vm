-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE TABLE Players(
	ID SERIAL PRIMARY KEY,
	NAME VARCHAR(30) NOT NULL
);

CREATE TABLE Matches(
	WINNER INT NOT NULL,
	LOSER INT NOT NULL,
	PRIMARY KEY (WINNER, LOSER)
);



