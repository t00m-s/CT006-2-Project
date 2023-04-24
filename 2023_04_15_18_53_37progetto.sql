--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2 (Debian 15.2-1.pgdg110+1)
-- Dumped by pg_dump version 15.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE progetto;
--
-- Name: progetto; Type: DATABASE; Schema: -; Owner: progetto
--

CREATE DATABASE progetto WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE progetto OWNER TO progetto;

\connect progetto

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: mypublic; Type: SCHEMA; Schema: -; Owner: progetto
--

CREATE SCHEMA mypublic;


ALTER SCHEMA mypublic OWNER TO progetto;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: users; Type: TABLE; Schema: mypublic; Owner: progetto
--

CREATE TABLE mypublic.users (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    surname character varying(255) NOT NULL,
    username character varying(255) NOT NULL,
    email character varying(255) NOT NULL
);


ALTER TABLE mypublic.users OWNER TO progetto;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: mypublic; Owner: progetto
--

CREATE SEQUENCE mypublic.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mypublic.users_id_seq OWNER TO progetto;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: mypublic; Owner: progetto
--

ALTER SEQUENCE mypublic.users_id_seq OWNED BY mypublic.users.id;


--
-- Name: users id; Type: DEFAULT; Schema: mypublic; Owner: progetto
--

ALTER TABLE ONLY mypublic.users ALTER COLUMN id SET DEFAULT nextval('mypublic.users_id_seq'::regclass);


--
-- Data for Name: users; Type: TABLE DATA; Schema: mypublic; Owner: progetto
--



--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: mypublic; Owner: progetto
--

SELECT pg_catalog.setval('mypublic.users_id_seq', 1, false);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: mypublic; Owner: progetto
--

ALTER TABLE ONLY mypublic.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

