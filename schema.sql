DROP TABLE IF EXISTS questions_easy;
DROP TABLE IF EXISTS questions_hard;

CREATE TABLE questions_easy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    json TEXT NOT NULL
);

CREATE TABLE questions_hard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    json TEXT NOT NULL
);
