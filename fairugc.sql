--
-- PostgreSQL database dump
--

\restrict dDUYRduYM5lr37XW5KHRfRnYbpX9RVQEmadcASkwVGyVXoAX8Ryz2PgxB6wxlxh

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

-- Started on 2025-12-05 14:32:25

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 228 (class 1259 OID 17201)
-- Name: calculations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.calculations (
    id integer NOT NULL,
    content_type character varying(50),
    niche character varying(50),
    usage_rights text,
    calculated_min integer,
    calculated_max integer,
    "timestamp" timestamp without time zone,
    updated_by character varying(100)
);


ALTER TABLE public.calculations OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 17200)
-- Name: calculations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.calculations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.calculations_id_seq OWNER TO postgres;

--
-- TOC entry 5091 (class 0 OID 0)
-- Dependencies: 227
-- Name: calculations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.calculations_id_seq OWNED BY public.calculations.id;


--
-- TOC entry 226 (class 1259 OID 17192)
-- Name: leads; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.leads (
    id integer NOT NULL,
    email character varying(120) NOT NULL,
    date_created timestamp without time zone,
    updated_by character varying(100)
);


ALTER TABLE public.leads OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 17191)
-- Name: leads_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.leads_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.leads_id_seq OWNER TO postgres;

--
-- TOC entry 5092 (class 0 OID 0)
-- Dependencies: 225
-- Name: leads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.leads_id_seq OWNED BY public.leads.id;


--
-- TOC entry 220 (class 1259 OID 17158)
-- Name: permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.permissions (
    id integer NOT NULL,
    slug character varying(50) NOT NULL,
    description character varying(200)
);


ALTER TABLE public.permissions OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 17157)
-- Name: permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.permissions_id_seq OWNER TO postgres;

--
-- TOC entry 5093 (class 0 OID 0)
-- Dependencies: 219
-- Name: permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.permissions_id_seq OWNED BY public.permissions.id;


--
-- TOC entry 233 (class 1259 OID 17246)
-- Name: pitch_templates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pitch_templates (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    mood character varying(50),
    content text NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.pitch_templates OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 17245)
-- Name: pitch_templates_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pitch_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pitch_templates_id_seq OWNER TO postgres;

--
-- TOC entry 5094 (class 0 OID 0)
-- Dependencies: 232
-- Name: pitch_templates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pitch_templates_id_seq OWNED BY public.pitch_templates.id;


--
-- TOC entry 224 (class 1259 OID 17180)
-- Name: pricing_config; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pricing_config (
    id integer NOT NULL,
    key character varying(50) NOT NULL,
    value double precision NOT NULL,
    category character varying(50),
    description character varying(200),
    updated_by character varying(100)
);


ALTER TABLE public.pricing_config OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 17179)
-- Name: pricing_config_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pricing_config_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pricing_config_id_seq OWNER TO postgres;

--
-- TOC entry 5095 (class 0 OID 0)
-- Dependencies: 223
-- Name: pricing_config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pricing_config_id_seq OWNED BY public.pricing_config.id;


--
-- TOC entry 229 (class 1259 OID 17210)
-- Name: role_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role_permissions (
    role_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.role_permissions OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 17169)
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    updated_by character varying(100)
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 17168)
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_seq OWNER TO postgres;

--
-- TOC entry 5096 (class 0 OID 0)
-- Dependencies: 221
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- TOC entry 231 (class 1259 OID 17228)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role_id integer,
    updated_by character varying(100)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 17227)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 5097 (class 0 OID 0)
-- Dependencies: 230
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4894 (class 2604 OID 17204)
-- Name: calculations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculations ALTER COLUMN id SET DEFAULT nextval('public.calculations_id_seq'::regclass);


--
-- TOC entry 4893 (class 2604 OID 17195)
-- Name: leads id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads ALTER COLUMN id SET DEFAULT nextval('public.leads_id_seq'::regclass);


--
-- TOC entry 4890 (class 2604 OID 17161)
-- Name: permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions ALTER COLUMN id SET DEFAULT nextval('public.permissions_id_seq'::regclass);


--
-- TOC entry 4896 (class 2604 OID 17249)
-- Name: pitch_templates id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pitch_templates ALTER COLUMN id SET DEFAULT nextval('public.pitch_templates_id_seq'::regclass);


--
-- TOC entry 4892 (class 2604 OID 17183)
-- Name: pricing_config id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pricing_config ALTER COLUMN id SET DEFAULT nextval('public.pricing_config_id_seq'::regclass);


--
-- TOC entry 4891 (class 2604 OID 17172)
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- TOC entry 4895 (class 2604 OID 17231)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 5080 (class 0 OID 17201)
-- Dependencies: 228
-- Data for Name: calculations; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.calculations VALUES (1, 'photo', 'general', 'o,r,g,a,n,i,c', 50, 60, '2025-12-04 20:45:39.360817', 'system');
INSERT INTO public.calculations VALUES (2, 'photo', 'general', 'o,r,g,a,n,i,c', 50, 60, '2025-12-04 20:45:42.871893', 'system');
INSERT INTO public.calculations VALUES (3, 'photo', 'general', 'o,r,g,a,n,i,c', 100, 120, '2025-12-04 20:45:46.152328', 'system');


--
-- TOC entry 5078 (class 0 OID 17192)
-- Dependencies: 226
-- Data for Name: leads; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.leads VALUES (1, 'tosinajy@gmail.com', '2025-12-04 22:13:45.863838', 'user_submission');


--
-- TOC entry 5072 (class 0 OID 17158)
-- Dependencies: 220
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.permissions VALUES (1, 'can_manage_users', 'Access to add/delete users');
INSERT INTO public.permissions VALUES (2, 'can_manage_roles', 'Access to add/delete roles');
INSERT INTO public.permissions VALUES (3, 'can_view_dashboard', 'View Admin Dashboard');
INSERT INTO public.permissions VALUES (4, 'can_manage_pricing', 'Adjust pricing logic variables');


--
-- TOC entry 5085 (class 0 OID 17246)
-- Dependencies: 233
-- Data for Name: pitch_templates; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.pitch_templates VALUES (1, 'Professional/Corporate', 'professional', 'Hi {brand_name},

I’ve been following your brand for a while and love your approach to the market. I’m a content creator specializing in {product_type} and would love to help tell your story.

Attached is my portfolio.

Best,
[Your Name]', '2025-12-04 21:02:20.784625');
INSERT INTO public.pitch_templates VALUES (2, 'Casual/Authentic', 'casual', 'Hey {brand_name} team! 👋

Huge fan of your {product_type}! I actually use it daily. I create authentic UGC that feels just like a friend recommending a product. Let''s chat about how we can make some viral content together!

Cheers,
[Your Name]', '2025-12-04 21:02:20.784625');
INSERT INTO public.pitch_templates VALUES (3, 'Bold/High Energy', 'bold', 'What''s up {brand_name}!

Your {product_type} is a game changer, but I think we can make it pop even more on TikTok. I specialize in high-energy, fast-paced edits that stop the scroll.

Let''s crush Q4 together.

- [Your Name]', '2025-12-04 21:02:20.784625');


--
-- TOC entry 5076 (class 0 OID 17180)
-- Dependencies: 224
-- Data for Name: pricing_config; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.pricing_config VALUES (1, 'base_video', 150, 'base', 'Base rate for 1 UGC Video', 'system');
INSERT INTO public.pricing_config VALUES (2, 'base_photo', 50, 'base', 'Base rate for Photo Bundle', 'system');
INSERT INTO public.pricing_config VALUES (3, 'base_testimonial', 75, 'base', 'Base rate for Testimonial', 'system');
INSERT INTO public.pricing_config VALUES (4, 'mult_exp_inter', 0.2, 'multiplier', 'Intermediate Experience Multiplier', 'system');
INSERT INTO public.pricing_config VALUES (5, 'mult_exp_pro', 1, 'multiplier', 'Pro Experience Multiplier', 'system');
INSERT INTO public.pricing_config VALUES (6, 'mult_niche_tech', 0.5, 'multiplier', 'Tech/Finance Niche Multiplier', 'system');
INSERT INTO public.pricing_config VALUES (7, 'mult_niche_beauty', 0.2, 'multiplier', 'Beauty Niche Multiplier', 'system');
INSERT INTO public.pricing_config VALUES (8, 'usage_ads_30', 0.3, 'usage', 'Paid Ads 30 Days', 'system');
INSERT INTO public.pricing_config VALUES (9, 'usage_ads_90', 0.5, 'usage', 'Paid Ads 90 Days', 'system');
INSERT INTO public.pricing_config VALUES (10, 'usage_exclusivity', 0.4, 'usage', 'Exclusivity Clause', 'system');
INSERT INTO public.pricing_config VALUES (11, 'usage_whitelisting', 0.25, 'usage', 'Whitelisting Access', 'system');


--
-- TOC entry 5081 (class 0 OID 17210)
-- Dependencies: 229
-- Data for Name: role_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.role_permissions VALUES (1, 4);
INSERT INTO public.role_permissions VALUES (1, 3);
INSERT INTO public.role_permissions VALUES (2, 3);
INSERT INTO public.role_permissions VALUES (1, 2);
INSERT INTO public.role_permissions VALUES (1, 1);


--
-- TOC entry 5074 (class 0 OID 17169)
-- Dependencies: 222
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.roles VALUES (1, 'admin', 'system');
INSERT INTO public.roles VALUES (2, 'editor', 'system');


--
-- TOC entry 5083 (class 0 OID 17228)
-- Dependencies: 231
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users VALUES (1, 'admin', '$2b$12$MAOy86IoKRDkD7cn4V3/3uFjB4n.Ol77cG3mqrvYqFN5SEcOVaemS', 1, 'system');


--
-- TOC entry 5098 (class 0 OID 0)
-- Dependencies: 227
-- Name: calculations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.calculations_id_seq', 3, true);


--
-- TOC entry 5099 (class 0 OID 0)
-- Dependencies: 225
-- Name: leads_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.leads_id_seq', 1, true);


--
-- TOC entry 5100 (class 0 OID 0)
-- Dependencies: 219
-- Name: permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.permissions_id_seq', 4, true);


--
-- TOC entry 5101 (class 0 OID 0)
-- Dependencies: 232
-- Name: pitch_templates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pitch_templates_id_seq', 3, true);


--
-- TOC entry 5102 (class 0 OID 0)
-- Dependencies: 223
-- Name: pricing_config_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pricing_config_id_seq', 11, true);


--
-- TOC entry 5103 (class 0 OID 0)
-- Dependencies: 221
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_seq', 2, true);


--
-- TOC entry 5104 (class 0 OID 0)
-- Dependencies: 230
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- TOC entry 4912 (class 2606 OID 17209)
-- Name: calculations calculations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calculations
    ADD CONSTRAINT calculations_pkey PRIMARY KEY (id);


--
-- TOC entry 4910 (class 2606 OID 17199)
-- Name: leads leads_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_pkey PRIMARY KEY (id);


--
-- TOC entry 4898 (class 2606 OID 17165)
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 4900 (class 2606 OID 17167)
-- Name: permissions permissions_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_slug_key UNIQUE (slug);


--
-- TOC entry 4920 (class 2606 OID 17256)
-- Name: pitch_templates pitch_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pitch_templates
    ADD CONSTRAINT pitch_templates_pkey PRIMARY KEY (id);


--
-- TOC entry 4906 (class 2606 OID 17190)
-- Name: pricing_config pricing_config_key_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pricing_config
    ADD CONSTRAINT pricing_config_key_key UNIQUE (key);


--
-- TOC entry 4908 (class 2606 OID 17188)
-- Name: pricing_config pricing_config_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pricing_config
    ADD CONSTRAINT pricing_config_pkey PRIMARY KEY (id);


--
-- TOC entry 4914 (class 2606 OID 17216)
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (role_id, permission_id);


--
-- TOC entry 4902 (class 2606 OID 17178)
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- TOC entry 4904 (class 2606 OID 17176)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- TOC entry 4916 (class 2606 OID 17236)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4918 (class 2606 OID 17238)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4921 (class 2606 OID 17222)
-- Name: role_permissions role_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id);


--
-- TOC entry 4922 (class 2606 OID 17217)
-- Name: role_permissions role_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- TOC entry 4923 (class 2606 OID 17239)
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


-- Completed on 2025-12-05 14:32:25

--
-- PostgreSQL database dump complete
--

\unrestrict dDUYRduYM5lr37XW5KHRfRnYbpX9RVQEmadcASkwVGyVXoAX8Ryz2PgxB6wxlxh

