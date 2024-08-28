CREATE TABLE Users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  hash_password VARCHAR(255) NOT NULL,
  verify BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE Tokens (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  token VARCHAR(510) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expired TIMESTAMP,
  FOREIGN KEY user_id FOREIGN KEY Users (id)
);

CREATE TABLE Cards (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  balance INTEGER NOT NULL DEFAULT 0,
  num_card VARCHAR(20) NOT NULL,
  FOREIGN KEY user_id FOREIGN KEY Users (id)
);

CREATE TABLE Transactions (
  id SERIAL PRIMARY KEY,
  operation VARCHAR(50) NOT NULL CHECK (operation IN ('debit', 'withdrawal')),
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  amount INTEGER NOT NULL DEFAULT 0 CHECK (balance >= 0),
  card_id INTEGER NOT NULL,
  FOREIGN KEY card_id FOREIGN KEY Cards (id)
);

CREATE TABLE labels (
  id SERIAL PRIMARY KEY,
  label_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Transaction_Labels (
  transaction_id INTEGER NOT NULL,
  label_id INTEGER NOT NULL,
  PRIMARY KEY (transaction_id, label_id),
  FOREIGN KEY (transaction_id) REFERENCES Transactions(id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (label_id) REFERENCES labels(id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- CRUD Команды PostgreSQL
-- Users
INSERT INTO Users (username, hash_password, verify)
VALUES ('test_user', 'hashed_password', FALSE);

SELECT * FROM Users WHERE id = 1;

UPDATE Users SET verify = TRUE WHERE id = 1;

DELETE FROM Users WHERE id = 1;


-- Transaction
INSERT INTO Cards (user_id, balance, num_card)
VALUES (2, 10000, '0000 0000 0000 0000')

INSERT INTO Transactions (operation, timestamp, amount, card_id) 
VALUES ('deposit', CURRENT_TIMESTAMP, 100, 1);

SELECT * FROM Transactions WHERE card_id = 1;


-- Labels
INSERT INTO labels (label_name) VALUES ('food');

SELECT * FROM labels WHERE id = 1;

UPDATE labels SET label_name = 'bus' WHERE id = 1;

DELETE FROM labels WHERE id = 1;

-- Trasaction_labels - тут CRUD для many-to-many, они же метки транзакций или теги
SELECT t.id, t.amount, l.label_name 
FROM transactions AS t
JOIN transaction_labels as t_l ON t_l.transaction_id = t.id
JOIN labels AS l ON t_l.label_id = l.id
WHERE l.label_name = 'food';

-- Тут я взял все транзакции с меткой 'food'
