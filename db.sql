SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;


CREATE TABLE users (
    id integer NOT NULL,
    username character varying(16) NOT NULL,
    is_admin boolean DEFAULT false NOT NULL,
    faction smallint NOT NULL,
    created_at timestamp without time zone NOT NULL,
    google_id character varying(60) NOT NULL,
    email character varying(60) NOT NULL
);
ALTER TABLE users OWNER TO cantonres;

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE users_id_seq OWNER TO cantonres;
ALTER SEQUENCE users_id_seq OWNED BY users.id;
ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);

ALTER TABLE ONLY users ADD CONSTRAINT users_id_pk PRIMARY KEY (id);
CREATE UNIQUE INDEX users_email_uindex ON users USING btree (email);
CREATE UNIQUE INDEX users_google_id_uindex ON users USING btree (google_id);
CREATE UNIQUE INDEX users_id_uindex ON users USING btree (id);


CREATE TABLE articles (
    id integer NOT NULL,
    author_id integer NOT NULL,
    title character varying(60) NOT NULL,
    content text NOT NULL,
    tag jsonb,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    published_at timestamp without time zone
);
ALTER TABLE articles OWNER TO cantonres;

CREATE SEQUENCE articles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE articles_id_seq OWNER TO cantonres;
ALTER SEQUENCE articles_id_seq OWNED BY articles.id;
ALTER TABLE ONLY articles ALTER COLUMN id SET DEFAULT nextval('articles_id_seq'::regclass);

ALTER TABLE ONLY articles ADD CONSTRAINT articles_pkey PRIMARY KEY (id);
CREATE UNIQUE INDEX articles_id_uindex ON articles USING btree (id);
