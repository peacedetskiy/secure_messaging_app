CREATE TABLE "user" (
  "id" SERIAL PRIMARY KEY,
  "name" character(30) UNIQUE NOT NULL,
  "password" character(60) NOT NULL,
  "salt" character(29) NOT NULL
);

CREATE TABLE message (
    "id" SERIAL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "sender" VARCHAR(30) NOT NULL,
    "recipient" VARCHAR(30) NOT NULL,
    "timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("sender") REFERENCES "user" ("name"),
    FOREIGN KEY ("recipient") REFERENCES "user" ("name")
);

CREATE EXTENSION IF NOT EXISTS "pgcrypto";