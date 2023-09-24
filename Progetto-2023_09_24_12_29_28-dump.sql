--
-- PostgreSQL database dump
--

-- Dumped from database version 15.4 (Debian 15.4-1.pgdg120+1)
-- Dumped by pg_dump version 15.3

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

DROP DATABASE IF EXISTS progetto;
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
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: is_reviewer(); Type: FUNCTION; Schema: public; Owner: progetto
--

CREATE FUNCTION public.is_reviewer() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
            IF NEW.id_user_reviewer IS NOT NULL THEN
                IF (NEW.id_user_reviewer NOT IN
                (SELECT u.id
                FROM users u JOIN roles r ON u.id_role=r.id
                WHERE r.is_reviewer AND u.id=NEW.id_user_reviewer) AND
                    (NEW.id_user_reviewer != (SELECT id_user FROM projects WHERE id=NEW.id_project))
                ) THEN
                    RETURN NULL;
                END IF;
            END IF;
            RETURN NEW;
        END $$;


ALTER FUNCTION public.is_reviewer() OWNER TO progetto;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: chat; Type: TABLE; Schema: public; Owner: progetto
--

CREATE TABLE public.chat (
    id integer NOT NULL,
    id_project integer NOT NULL,
    id_user integer NOT NULL,
    message character varying NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.chat OWNER TO progetto;

--
-- Name: COLUMN chat.id_user; Type: COMMENT; Schema: public; Owner: progetto
--

COMMENT ON COLUMN public.chat.id_user IS 'User that have sent the message';


--
-- Name: chat_id_seq; Type: SEQUENCE; Schema: public; Owner: progetto
--

CREATE SEQUENCE public.chat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chat_id_seq OWNER TO progetto;

--
-- Name: chat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: progetto
--

ALTER SEQUENCE public.chat_id_seq OWNED BY public.chat.id;


--
-- Name: project_files; Type: TABLE; Schema: public; Owner: progetto
--

CREATE TABLE public.project_files (
    id integer NOT NULL,
    path character varying NOT NULL,
    id_project_history integer NOT NULL
);


ALTER TABLE public.project_files OWNER TO progetto;

--
-- Name: project_files_id_seq; Type: SEQUENCE; Schema: public; Owner: progetto
--

CREATE SEQUENCE public.project_files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_files_id_seq OWNER TO progetto;

--
-- Name: project_files_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: progetto
--

ALTER SEQUENCE public.project_files_id_seq OWNED BY public.project_files.id;


--
-- Name: project_history; Type: TABLE; Schema: public; Owner: progetto
--

CREATE TABLE public.project_history (
    id integer NOT NULL,
    id_project integer NOT NULL,
    id_state integer NOT NULL,
    id_user_reviewer integer NOT NULL,
    note text,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.project_history OWNER TO progetto;

--
-- Name: project_history_id_seq; Type: SEQUENCE; Schema: public; Owner: progetto
--

CREATE SEQUENCE public.project_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_history_id_seq OWNER TO progetto;

--
-- Name: project_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: progetto
--

ALTER SEQUENCE public.project_history_id_seq OWNED BY public.project_history.id;


--
-- Name: projects; Type: TABLE; Schema: public; Owner: progetto
--

CREATE TABLE public.projects (
    id integer NOT NULL,
    id_user integer NOT NULL,
    id_type integer NOT NULL,
    name character varying NOT NULL,
    description text,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.projects OWNER TO progetto;

--
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: progetto
--

CREATE SEQUENCE public.projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_id_seq OWNER TO progetto;

--
-- Name: projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: progetto
--

ALTER SEQUENCE public.projects_id_seq OWNED BY public.projects.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: progetto
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying NOT NULL,
    is_reviewer boolean NOT NULL
);


ALTER TABLE public.roles OWNER TO progetto;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: progetto
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roles_id_seq OWNER TO progetto;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: progetto
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: states; Type: TABLE; Schema: public; Owner: progetto
--

CREATE TABLE public.states (
    id integer NOT NULL,
    name character varying NOT NULL,
    is_closed boolean NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.states OWNER TO progetto;

--
-- Name: states_id_seq; Type: SEQUENCE; Schema: public; Owner: progetto
--

CREATE SEQUENCE public.states_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.states_id_seq OWNER TO progetto;

--
-- Name: states_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: progetto
--

ALTER SEQUENCE public.states_id_seq OWNED BY public.states.id;


--
-- Name: types; Type: TABLE; Schema: public; Owner: progetto
--

CREATE TABLE public.types (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.types OWNER TO progetto;

--
-- Name: types_id_seq; Type: SEQUENCE; Schema: public; Owner: progetto
--

CREATE SEQUENCE public.types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.types_id_seq OWNER TO progetto;

--
-- Name: types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: progetto
--

ALTER SEQUENCE public.types_id_seq OWNED BY public.types.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: progetto
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying NOT NULL,
    surname character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    id_role integer NOT NULL,
    birth_date timestamp without time zone,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    ban boolean NOT NULL
);


ALTER TABLE public.users OWNER TO progetto;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: progetto
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO progetto;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: progetto
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: chat id; Type: DEFAULT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.chat ALTER COLUMN id SET DEFAULT nextval('public.chat_id_seq'::regclass);


--
-- Name: project_files id; Type: DEFAULT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.project_files ALTER COLUMN id SET DEFAULT nextval('public.project_files_id_seq'::regclass);


--
-- Name: project_history id; Type: DEFAULT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.project_history ALTER COLUMN id SET DEFAULT nextval('public.project_history_id_seq'::regclass);


--
-- Name: projects id; Type: DEFAULT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.projects ALTER COLUMN id SET DEFAULT nextval('public.projects_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: states id; Type: DEFAULT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.states ALTER COLUMN id SET DEFAULT nextval('public.states_id_seq'::regclass);


--
-- Name: types id; Type: DEFAULT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.types ALTER COLUMN id SET DEFAULT nextval('public.types_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: chat; Type: TABLE DATA; Schema: public; Owner: progetto
--

INSERT INTO public.chat (id, id_project, id_user, message, created_at) VALUES (131, 26, 39, 'User has connected!', '2023-09-23 14:21:02.508199');
INSERT INTO public.chat (id, id_project, id_user, message, created_at) VALUES (132, 26, 38, 'User has connected!', '2023-09-23 14:21:03.638752');
INSERT INTO public.chat (id, id_project, id_user, message, created_at) VALUES (133, 26, 38, 'Salve', '2023-09-23 14:21:13.114001');
INSERT INTO public.chat (id, id_project, id_user, message, created_at) VALUES (134, 26, 39, 'Salve', '2023-09-23 14:21:18.65637');
INSERT INTO public.chat (id, id_project, id_user, message, created_at) VALUES (135, 26, 38, 'Ottima relazione!', '2023-09-23 14:21:24.312357');
INSERT INTO public.chat (id, id_project, id_user, message, created_at) VALUES (136, 26, 39, 'Grazie!', '2023-09-23 14:21:28.41709');


--
-- Data for Name: project_files; Type: TABLE DATA; Schema: public; Owner: progetto
--

INSERT INTO public.project_files (id, path, id_project_history) VALUES (22, '/app/db_files/38/26/22/sample.pdf', 22);
INSERT INTO public.project_files (id, path, id_project_history) VALUES (23, '/app/db_files/39/26/23/sample (1).pdf', 23);
INSERT INTO public.project_files (id, path, id_project_history) VALUES (24, '/app/db_files/38/26/24/sample (3).pdf', 24);
INSERT INTO public.project_files (id, path, id_project_history) VALUES (25, '/app/db_files/39/26/25/sample (5).pdf', 25);


--
-- Data for Name: project_history; Type: TABLE DATA; Schema: public; Owner: progetto
--

INSERT INTO public.project_history (id, id_project, id_state, id_user_reviewer, note, created_at) VALUES (22, 26, 2, 38, 'TEST', '2023-09-23 14:07:29.997573');
INSERT INTO public.project_history (id, id_project, id_state, id_user_reviewer, note, created_at) VALUES (23, 26, 3, 39, 'Correggere Pagina 1', '2023-09-23 14:13:56.778417');
INSERT INTO public.project_history (id, id_project, id_state, id_user_reviewer, note, created_at) VALUES (24, 26, 2, 38, 'HO CORRETTO', '2023-09-23 14:14:29.625339');
INSERT INTO public.project_history (id, id_project, id_state, id_user_reviewer, note, created_at) VALUES (25, 26, 1, 39, 'ATTESTATO DI PUBBLICAZIONE', '2023-09-23 14:15:14.671674');


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: progetto
--

INSERT INTO public.projects (id, id_user, id_type, name, description, created_at) VALUES (26, 38, 1, 'TEST', '&lt;p&gt;12345678&lt;/p&gt;', '2023-09-23 14:07:04.879445');


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: progetto
--

INSERT INTO public.roles (id, name, is_reviewer) VALUES (1, 'Admin', true);
INSERT INTO public.roles (id, name, is_reviewer) VALUES (2, 'Reviewer', true);
INSERT INTO public.roles (id, name, is_reviewer) VALUES (3, 'Researcher', false);


--
-- Data for Name: states; Type: TABLE DATA; Schema: public; Owner: progetto
--

INSERT INTO public.states (id, name, is_closed, created_at) VALUES (1, 'Approved', true, '2023-09-18 22:02:32.082357');
INSERT INTO public.states (id, name, is_closed, created_at) VALUES (2, 'Submitted', false, '2023-09-18 22:02:32.082357');
INSERT INTO public.states (id, name, is_closed, created_at) VALUES (3, 'Requires Changes', false, '2023-09-18 22:02:32.082357');
INSERT INTO public.states (id, name, is_closed, created_at) VALUES (4, 'Not Approved', true, '2023-09-18 22:02:32.082357');


--
-- Data for Name: types; Type: TABLE DATA; Schema: public; Owner: progetto
--

INSERT INTO public.types (id, name) VALUES (1, 'Data Management Plan');
INSERT INTO public.types (id, name) VALUES (2, 'Ethics');
INSERT INTO public.types (id, name) VALUES (3, 'Deliverable');


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: progetto
--

INSERT INTO public.users (id, name, surname, email, password, id_role, birth_date, created_at, ban) VALUES (38, 'Autore', 'Autore', 'autore@unive.it', 'Michael02', 3, '2002-12-10 00:00:00', '2023-09-23 13:54:45.813769', false);
INSERT INTO public.users (id, name, surname, email, password, id_role, birth_date, created_at, ban) VALUES (37, 'Admin', 'Admin', 'admin@unive.it', '97570901092fb47c02aaa8aa3fac2e47d3edc3bc508c8f8a6b3b8901d2016c9920f2d60e3e8fcb56e58f1b58fced7b939c38da7df5c9d76a48cef72e796043ad', 1, NULL, '2023-09-23 13:54:12.610949', false);
INSERT INTO public.users (id, name, surname, email, password, id_role, birth_date, created_at, ban) VALUES (39, 'Relatore', 'Relatore', 'relatore@unive.it', '97570901092fb47c02aaa8aa3fac2e47d3edc3bc508c8f8a6b3b8901d2016c9920f2d60e3e8fcb56e58f1b58fced7b939c38da7df5c9d76a48cef72e796043ad', 2, '1979-07-18 00:00:00', '2023-09-23 13:55:11.380483', false);


--
-- Name: chat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: progetto
--

SELECT pg_catalog.setval('public.chat_id_seq', 136, true);


--
-- Name: project_files_id_seq; Type: SEQUENCE SET; Schema: public; Owner: progetto
--

SELECT pg_catalog.setval('public.project_files_id_seq', 25, true);


--
-- Name: project_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: progetto
--

SELECT pg_catalog.setval('public.project_history_id_seq', 25, true);


--
-- Name: projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: progetto
--

SELECT pg_catalog.setval('public.projects_id_seq', 26, true);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: progetto
--

SELECT pg_catalog.setval('public.roles_id_seq', 1, false);


--
-- Name: states_id_seq; Type: SEQUENCE SET; Schema: public; Owner: progetto
--

SELECT pg_catalog.setval('public.states_id_seq', 1, false);


--
-- Name: types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: progetto
--

SELECT pg_catalog.setval('public.types_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: progetto
--

SELECT pg_catalog.setval('public.users_id_seq', 39, true);


--
-- Name: chat chat_pkey; Type: CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.chat
    ADD CONSTRAINT chat_pkey PRIMARY KEY (id);


--
-- Name: project_files project_files_path_key; Type: CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.project_files
    ADD CONSTRAINT project_files_path_key UNIQUE (path);


--
-- Name: project_files project_files_pkey; Type: CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.project_files
    ADD CONSTRAINT project_files_pkey PRIMARY KEY (id);


--
-- Name: project_history project_history_pkey; Type: CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.project_history
    ADD CONSTRAINT project_history_pkey PRIMARY KEY (id);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: states states_name_key; Type: CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.states
    ADD CONSTRAINT states_name_key UNIQUE (name);


--
-- Name: states states_pkey; Type: CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.states
    ADD CONSTRAINT states_pkey PRIMARY KEY (id);


--
-- Name: types types_pkey; Type: CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.types
    ADD CONSTRAINT types_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: project_history is_reviewer_trigger; Type: TRIGGER; Schema: public; Owner: progetto
--

CREATE TRIGGER is_reviewer_trigger BEFORE INSERT OR UPDATE ON public.project_history FOR EACH ROW EXECUTE FUNCTION public.is_reviewer();


--
-- Name: chat chat_id_project_fkey; Type: FK CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.chat
    ADD CONSTRAINT chat_id_project_fkey FOREIGN KEY (id_project) REFERENCES public.projects(id);


--
-- Name: chat chat_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.chat
    ADD CONSTRAINT chat_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id);


--
-- Name: project_files project_files_id_project_history_fkey; Type: FK CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.project_files
    ADD CONSTRAINT project_files_id_project_history_fkey FOREIGN KEY (id_project_history) REFERENCES public.project_history(id);


--
-- Name: project_history project_history_id_project_fkey; Type: FK CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.project_history
    ADD CONSTRAINT project_history_id_project_fkey FOREIGN KEY (id_project) REFERENCES public.projects(id);


--
-- Name: project_history project_history_id_state_fkey; Type: FK CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.project_history
    ADD CONSTRAINT project_history_id_state_fkey FOREIGN KEY (id_state) REFERENCES public.states(id);


--
-- Name: project_history project_history_id_user_reviewer_fkey; Type: FK CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.project_history
    ADD CONSTRAINT project_history_id_user_reviewer_fkey FOREIGN KEY (id_user_reviewer) REFERENCES public.users(id);


--
-- Name: projects projects_id_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_id_type_fkey FOREIGN KEY (id_type) REFERENCES public.types(id);


--
-- Name: projects projects_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id);


--
-- Name: users users_id_role_fkey; Type: FK CONSTRAINT; Schema: public; Owner: progetto
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_id_role_fkey FOREIGN KEY (id_role) REFERENCES public.roles(id);


--
-- PostgreSQL database dump complete
--

