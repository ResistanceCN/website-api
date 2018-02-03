SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;


-- auto-generated definition
CREATE TABLE users (
    id         SERIAL                NOT NULL
        CONSTRAINT users_id_pk
        PRIMARY KEY,
    google_id  VARCHAR(60)           NOT NULL,
    email      VARCHAR(60)           NOT NULL,
    name       VARCHAR(16)           NOT NULL,
    is_admin   BOOLEAN DEFAULT FALSE NOT NULL,
    faction    SMALLINT              NOT NULL,
    created_at TIMESTAMP             NOT NULL
);

CREATE UNIQUE INDEX users_id_uindex ON users (id);
CREATE UNIQUE INDEX users_google_id_uindex ON users (google_id);
CREATE UNIQUE INDEX users_email_uindex ON users (email);


-- auto-generated definition
CREATE TABLE articles (
    id           SERIAL                  NOT NULL
        CONSTRAINT articles_pkey
        PRIMARY KEY,
    author_id    INTEGER                 NOT NULL,
    title        VARCHAR(60)             NOT NULL,
    content      TEXT                    NOT NULL,
    tags         JSONB DEFAULT '[]' :: JSONB,
    created_at   TIMESTAMP DEFAULT now() NOT NULL,
    updated_at   TIMESTAMP,
    published_at TIMESTAMP
);

CREATE UNIQUE INDEX articles_id_uindex ON articles (id);
