--
-- PostgreSQL database dump
--

\restrict nzbQ9FypPp0TyC4PFtaSmBg5Wg0EhEXgLTYXnFiakxkSYh7OwLu2uuvJei6PaaZ

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

-- Started on 2026-07-16 05:51:41

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

--
-- TOC entry 7 (class 2615 OID 16589)
-- Name: core; Type: SCHEMA; Schema: -; Owner: qm_admin
--

CREATE SCHEMA core;


ALTER SCHEMA core OWNER TO qm_admin;

--
-- TOC entry 9 (class 2615 OID 16591)
-- Name: integration; Type: SCHEMA; Schema: -; Owner: qm_admin
--

CREATE SCHEMA integration;


ALTER SCHEMA integration OWNER TO qm_admin;

--
-- TOC entry 8 (class 2615 OID 16590)
-- Name: software_engineering; Type: SCHEMA; Schema: -; Owner: qm_admin
--

CREATE SCHEMA software_engineering;


ALTER SCHEMA software_engineering OWNER TO qm_admin;

--
-- TOC entry 2 (class 3079 OID 17431)
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- TOC entry 5300 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


--
-- TOC entry 272 (class 1255 OID 17324)
-- Name: sync_user_role_from_role_id(); Type: FUNCTION; Schema: core; Owner: postgres
--

CREATE FUNCTION core.sync_user_role_from_role_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF NEW.role_id IS NOT NULL THEN
    SELECT r.role_name INTO NEW.role
    FROM core.roles r
    WHERE r.role_id = NEW.role_id;
  END IF;
  RETURN NEW;
END;
$$;


ALTER FUNCTION core.sync_user_role_from_role_id() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 232 (class 1259 OID 16660)
-- Name: activity_logs; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.activity_logs (
    log_id integer NOT NULL,
    user_id integer,
    action_type character varying(100),
    details text,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE core.activity_logs OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16659)
-- Name: activity_logs_log_id_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.activity_logs_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.activity_logs_log_id_seq OWNER TO postgres;

--
-- TOC entry 5301 (class 0 OID 0)
-- Dependencies: 231
-- Name: activity_logs_log_id_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.activity_logs_log_id_seq OWNED BY core.activity_logs.log_id;


--
-- TOC entry 269 (class 1259 OID 17636)
-- Name: app_feedback; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.app_feedback (
    feedback_id integer NOT NULL,
    user_id integer,
    rating integer NOT NULL,
    comment text,
    created_at timestamp with time zone DEFAULT now(),
    CONSTRAINT app_feedback_rating_check CHECK (((rating >= 1) AND (rating <= 5)))
);


ALTER TABLE core.app_feedback OWNER TO postgres;

--
-- TOC entry 268 (class 1259 OID 17635)
-- Name: app_feedback_feedback_id_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.app_feedback_feedback_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.app_feedback_feedback_id_seq OWNER TO postgres;

--
-- TOC entry 5302 (class 0 OID 0)
-- Dependencies: 268
-- Name: app_feedback_feedback_id_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.app_feedback_feedback_id_seq OWNED BY core.app_feedback.feedback_id;


--
-- TOC entry 226 (class 1259 OID 16611)
-- Name: auth_tokens; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.auth_tokens (
    token_id integer NOT NULL,
    user_id integer,
    access_token text NOT NULL,
    refresh_token text,
    expires_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE core.auth_tokens OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16610)
-- Name: auth_tokens_token_id_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.auth_tokens_token_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.auth_tokens_token_id_seq OWNER TO postgres;

--
-- TOC entry 5303 (class 0 OID 0)
-- Dependencies: 225
-- Name: auth_tokens_token_id_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.auth_tokens_token_id_seq OWNED BY core.auth_tokens.token_id;


--
-- TOC entry 228 (class 1259 OID 16628)
-- Name: departments; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.departments (
    department_id integer NOT NULL,
    department_key character varying(100) NOT NULL,
    display_name character varying(200) NOT NULL,
    description text,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE core.departments OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16627)
-- Name: departments_department_id_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.departments_department_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.departments_department_id_seq OWNER TO postgres;

--
-- TOC entry 5304 (class 0 OID 0)
-- Dependencies: 227
-- Name: departments_department_id_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.departments_department_id_seq OWNED BY core.departments.department_id;


--
-- TOC entry 230 (class 1259 OID 16643)
-- Name: feedback; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.feedback (
    feedback_id integer NOT NULL,
    user_id integer,
    rating integer,
    comments text,
    created_at timestamp with time zone DEFAULT now(),
    CONSTRAINT feedback_rating_check CHECK (((rating >= 1) AND (rating <= 5)))
);


ALTER TABLE core.feedback OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16642)
-- Name: feedback_feedback_id_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.feedback_feedback_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.feedback_feedback_id_seq OWNER TO postgres;

--
-- TOC entry 5305 (class 0 OID 0)
-- Dependencies: 229
-- Name: feedback_feedback_id_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.feedback_feedback_id_seq OWNED BY core.feedback.feedback_id;


--
-- TOC entry 261 (class 1259 OID 17516)
-- Name: notifications; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.notifications (
    notification_id integer NOT NULL,
    user_id integer NOT NULL,
    title character varying NOT NULL,
    message text NOT NULL,
    type character varying DEFAULT 'query_response'::character varying,
    is_read character varying DEFAULT 'false'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    query_id integer
);


ALTER TABLE core.notifications OWNER TO postgres;

--
-- TOC entry 260 (class 1259 OID 17515)
-- Name: notifications_notification_id_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.notifications_notification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.notifications_notification_id_seq OWNER TO postgres;

--
-- TOC entry 5306 (class 0 OID 0)
-- Dependencies: 260
-- Name: notifications_notification_id_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.notifications_notification_id_seq OWNED BY core.notifications.notification_id;


--
-- TOC entry 259 (class 1259 OID 17388)
-- Name: password_reset_otps; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.password_reset_otps (
    id integer NOT NULL,
    user_id integer NOT NULL,
    identifier character varying NOT NULL,
    otp_code character varying(6) NOT NULL,
    is_used boolean DEFAULT false,
    expires_at timestamp without time zone NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE core.password_reset_otps OWNER TO postgres;

--
-- TOC entry 258 (class 1259 OID 17387)
-- Name: password_reset_otps_id_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.password_reset_otps_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.password_reset_otps_id_seq OWNER TO postgres;

--
-- TOC entry 5307 (class 0 OID 0)
-- Dependencies: 258
-- Name: password_reset_otps_id_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.password_reset_otps_id_seq OWNED BY core.password_reset_otps.id;


--
-- TOC entry 250 (class 1259 OID 17135)
-- Name: roles; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.roles (
    role_id integer NOT NULL,
    role_name character varying(50) NOT NULL,
    description text,
    CONSTRAINT roles_role_name_check CHECK (((role_name)::text = ANY ((ARRAY['admin'::character varying, 'staff'::character varying, 'student'::character varying, 'superadmin'::character varying])::text[])))
);


ALTER TABLE core.roles OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 17134)
-- Name: roles_role_id_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.roles_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.roles_role_id_seq OWNER TO postgres;

--
-- TOC entry 5308 (class 0 OID 0)
-- Dependencies: 249
-- Name: roles_role_id_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.roles_role_id_seq OWNED BY core.roles.role_id;


--
-- TOC entry 224 (class 1259 OID 16593)
-- Name: users; Type: TABLE; Schema: core; Owner: postgres
--

CREATE TABLE core.users (
    user_id integer NOT NULL,
    full_name character varying(150) NOT NULL,
    roll_number character varying(50),
    email character varying(150),
    password_hash character varying(255),
    role character varying(20) NOT NULL,
    department character varying(100),
    phone character varying(20),
    created_at timestamp with time zone DEFAULT now(),
    last_login timestamp with time zone,
    role_id integer,
    id integer NOT NULL,
    is_active boolean DEFAULT true,
    otp_code character varying(10),
    otp_expiry timestamp with time zone,
    is_email_verified boolean DEFAULT false,
    is_deleted boolean DEFAULT false,
    deleted_at timestamp without time zone,
    CONSTRAINT users_role_check CHECK (((role)::text = ANY ((ARRAY['student'::character varying, 'staff'::character varying, 'admin'::character varying, 'superadmin'::character varying])::text[])))
);


ALTER TABLE core.users OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 17352)
-- Name: users_id_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.users_id_seq OWNER TO postgres;

--
-- TOC entry 5309 (class 0 OID 0)
-- Dependencies: 257
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.users_id_seq OWNED BY core.users.id;


--
-- TOC entry 223 (class 1259 OID 16592)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: core; Owner: postgres
--

CREATE SEQUENCE core.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE core.users_user_id_seq OWNER TO postgres;

--
-- TOC entry 5310 (class 0 OID 0)
-- Dependencies: 223
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: core; Owner: postgres
--

ALTER SEQUENCE core.users_user_id_seq OWNED BY core.users.user_id;


--
-- TOC entry 248 (class 1259 OID 17113)
-- Name: external_systems; Type: TABLE; Schema: integration; Owner: postgres
--

CREATE TABLE integration.external_systems (
    system_id integer NOT NULL,
    name character varying(100),
    api_key text,
    status character varying(20) DEFAULT 'active'::character varying,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE integration.external_systems OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 17112)
-- Name: external_systems_system_id_seq; Type: SEQUENCE; Schema: integration; Owner: postgres
--

CREATE SEQUENCE integration.external_systems_system_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE integration.external_systems_system_id_seq OWNER TO postgres;

--
-- TOC entry 5311 (class 0 OID 0)
-- Dependencies: 247
-- Name: external_systems_system_id_seq; Type: SEQUENCE OWNED BY; Schema: integration; Owner: postgres
--

ALTER SEQUENCE integration.external_systems_system_id_seq OWNED BY integration.external_systems.system_id;


--
-- TOC entry 246 (class 1259 OID 17091)
-- Name: whatsapp_messages; Type: TABLE; Schema: integration; Owner: postgres
--

CREATE TABLE integration.whatsapp_messages (
    message_id integer NOT NULL,
    whatsapp_user_id integer,
    direction character varying(10),
    message_text text,
    "timestamp" timestamp with time zone DEFAULT now(),
    query_id integer,
    message_type character varying(30) DEFAULT 'text'::character varying,
    media_url text,
    meta_message_id character varying(255),
    CONSTRAINT whatsapp_messages_direction_check CHECK (((direction)::text = ANY ((ARRAY['inbound'::character varying, 'outbound'::character varying])::text[])))
);


ALTER TABLE integration.whatsapp_messages OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 17090)
-- Name: whatsapp_messages_message_id_seq; Type: SEQUENCE; Schema: integration; Owner: postgres
--

CREATE SEQUENCE integration.whatsapp_messages_message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE integration.whatsapp_messages_message_id_seq OWNER TO postgres;

--
-- TOC entry 5312 (class 0 OID 0)
-- Dependencies: 245
-- Name: whatsapp_messages_message_id_seq; Type: SEQUENCE OWNED BY; Schema: integration; Owner: postgres
--

ALTER SEQUENCE integration.whatsapp_messages_message_id_seq OWNED BY integration.whatsapp_messages.message_id;


--
-- TOC entry 244 (class 1259 OID 17079)
-- Name: whatsapp_users; Type: TABLE; Schema: integration; Owner: postgres
--

CREATE TABLE integration.whatsapp_users (
    whatsapp_user_id integer NOT NULL,
    phone_number character varying(20) NOT NULL,
    name character varying(100),
    first_seen timestamp with time zone DEFAULT now(),
    last_seen timestamp with time zone
);


ALTER TABLE integration.whatsapp_users OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 17078)
-- Name: whatsapp_users_whatsapp_user_id_seq; Type: SEQUENCE; Schema: integration; Owner: postgres
--

CREATE SEQUENCE integration.whatsapp_users_whatsapp_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE integration.whatsapp_users_whatsapp_user_id_seq OWNER TO postgres;

--
-- TOC entry 5313 (class 0 OID 0)
-- Dependencies: 243
-- Name: whatsapp_users_whatsapp_user_id_seq; Type: SEQUENCE OWNED BY; Schema: integration; Owner: postgres
--

ALTER SEQUENCE integration.whatsapp_users_whatsapp_user_id_seq OWNED BY integration.whatsapp_users.whatsapp_user_id;


--
-- TOC entry 254 (class 1259 OID 17309)
-- Name: knowledge_base; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.knowledge_base (
    id integer NOT NULL,
    question text NOT NULL,
    answer text NOT NULL,
    department_id integer,
    source character varying,
    tags character varying,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    file_url text,
    file_name character varying(255),
    file_mime character varying(120)
);


ALTER TABLE public.knowledge_base OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 17308)
-- Name: knowledge_base_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.knowledge_base_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.knowledge_base_id_seq OWNER TO postgres;

--
-- TOC entry 5314 (class 0 OID 0)
-- Dependencies: 253
-- Name: knowledge_base_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.knowledge_base_id_seq OWNED BY public.knowledge_base.id;


--
-- TOC entry 256 (class 1259 OID 17329)
-- Name: password_reset_otps; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.password_reset_otps (
    id integer NOT NULL,
    user_id integer NOT NULL,
    identifier character varying(255) NOT NULL,
    otp_code character varying(10) NOT NULL,
    is_used boolean DEFAULT false NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.password_reset_otps OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 17328)
-- Name: password_reset_otps_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.password_reset_otps_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.password_reset_otps_id_seq OWNER TO postgres;

--
-- TOC entry 5315 (class 0 OID 0)
-- Dependencies: 255
-- Name: password_reset_otps_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.password_reset_otps_id_seq OWNED BY public.password_reset_otps.id;


--
-- TOC entry 252 (class 1259 OID 17294)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    role character varying,
    is_active boolean,
    is_email_verified boolean DEFAULT false,
    is_deleted boolean DEFAULT false
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 17293)
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
-- TOC entry 5316 (class 0 OID 0)
-- Dependencies: 251
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 238 (class 1259 OID 16989)
-- Name: attachments; Type: TABLE; Schema: software_engineering; Owner: postgres
--

CREATE TABLE software_engineering.attachments (
    attachment_id integer NOT NULL,
    kb_id integer,
    file_name character varying(255),
    drive_file_id character varying(255),
    file_url text NOT NULL,
    mime_type character varying(100),
    uploaded_by integer,
    created_at timestamp with time zone DEFAULT now(),
    stored_name character varying(255),
    file_path text,
    extracted_text text,
    file_type character varying(50),
    storage_type character varying(20) DEFAULT 'local'::character varying,
    updated_at timestamp with time zone
);


ALTER TABLE software_engineering.attachments OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16988)
-- Name: attachments_attachment_id_seq; Type: SEQUENCE; Schema: software_engineering; Owner: postgres
--

CREATE SEQUENCE software_engineering.attachments_attachment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE software_engineering.attachments_attachment_id_seq OWNER TO postgres;

--
-- TOC entry 5317 (class 0 OID 0)
-- Dependencies: 237
-- Name: attachments_attachment_id_seq; Type: SEQUENCE OWNED BY; Schema: software_engineering; Owner: postgres
--

ALTER SEQUENCE software_engineering.attachments_attachment_id_seq OWNED BY software_engineering.attachments.attachment_id;


--
-- TOC entry 271 (class 1259 OID 17660)
-- Name: chat_sessions; Type: TABLE; Schema: software_engineering; Owner: postgres
--

CREATE TABLE software_engineering.chat_sessions (
    session_id integer NOT NULL,
    student_user_id integer,
    title character varying(255),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE software_engineering.chat_sessions OWNER TO postgres;

--
-- TOC entry 270 (class 1259 OID 17659)
-- Name: chat_sessions_session_id_seq; Type: SEQUENCE; Schema: software_engineering; Owner: postgres
--

CREATE SEQUENCE software_engineering.chat_sessions_session_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE software_engineering.chat_sessions_session_id_seq OWNER TO postgres;

--
-- TOC entry 5318 (class 0 OID 0)
-- Dependencies: 270
-- Name: chat_sessions_session_id_seq; Type: SEQUENCE OWNED BY; Schema: software_engineering; Owner: postgres
--

ALTER SEQUENCE software_engineering.chat_sessions_session_id_seq OWNED BY software_engineering.chat_sessions.session_id;


--
-- TOC entry 234 (class 1259 OID 16948)
-- Name: kb_category; Type: TABLE; Schema: software_engineering; Owner: postgres
--

CREATE TABLE software_engineering.kb_category (
    category_id integer NOT NULL,
    category_name character varying(150) NOT NULL,
    description text,
    created_by integer,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE software_engineering.kb_category OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16947)
-- Name: kb_category_category_id_seq; Type: SEQUENCE; Schema: software_engineering; Owner: postgres
--

CREATE SEQUENCE software_engineering.kb_category_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE software_engineering.kb_category_category_id_seq OWNER TO postgres;

--
-- TOC entry 5319 (class 0 OID 0)
-- Dependencies: 233
-- Name: kb_category_category_id_seq; Type: SEQUENCE OWNED BY; Schema: software_engineering; Owner: postgres
--

ALTER SEQUENCE software_engineering.kb_category_category_id_seq OWNED BY software_engineering.kb_category.category_id;


--
-- TOC entry 263 (class 1259 OID 17561)
-- Name: kb_chunks; Type: TABLE; Schema: software_engineering; Owner: postgres
--

CREATE TABLE software_engineering.kb_chunks (
    chunk_id integer NOT NULL,
    kb_id integer NOT NULL,
    attachment_id integer,
    chunk_index integer NOT NULL,
    chunk_text text NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE software_engineering.kb_chunks OWNER TO postgres;

--
-- TOC entry 262 (class 1259 OID 17560)
-- Name: kb_chunks_chunk_id_seq; Type: SEQUENCE; Schema: software_engineering; Owner: postgres
--

CREATE SEQUENCE software_engineering.kb_chunks_chunk_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE software_engineering.kb_chunks_chunk_id_seq OWNER TO postgres;

--
-- TOC entry 5320 (class 0 OID 0)
-- Dependencies: 262
-- Name: kb_chunks_chunk_id_seq; Type: SEQUENCE OWNED BY; Schema: software_engineering; Owner: postgres
--

ALTER SEQUENCE software_engineering.kb_chunks_chunk_id_seq OWNED BY software_engineering.kb_chunks.chunk_id;


--
-- TOC entry 236 (class 1259 OID 16965)
-- Name: knowledge_base; Type: TABLE; Schema: software_engineering; Owner: postgres
--

CREATE TABLE software_engineering.knowledge_base (
    kb_id integer NOT NULL,
    title character varying(250) NOT NULL,
    content text NOT NULL,
    category_id integer,
    department_key character varying(100) NOT NULL,
    created_by integer,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    search_vector tsvector
);


ALTER TABLE software_engineering.knowledge_base OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16964)
-- Name: knowledge_base_kb_id_seq; Type: SEQUENCE; Schema: software_engineering; Owner: postgres
--

CREATE SEQUENCE software_engineering.knowledge_base_kb_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE software_engineering.knowledge_base_kb_id_seq OWNER TO postgres;

--
-- TOC entry 5321 (class 0 OID 0)
-- Dependencies: 235
-- Name: knowledge_base_kb_id_seq; Type: SEQUENCE OWNED BY; Schema: software_engineering; Owner: postgres
--

ALTER SEQUENCE software_engineering.knowledge_base_kb_id_seq OWNED BY software_engineering.knowledge_base.kb_id;


--
-- TOC entry 240 (class 1259 OID 17041)
-- Name: queries; Type: TABLE; Schema: software_engineering; Owner: postgres
--

CREATE TABLE software_engineering.queries (
    query_id integer NOT NULL,
    query_text text NOT NULL,
    ai_response text,
    source character varying(30) NOT NULL,
    student_user_id integer,
    status character varying(30) DEFAULT 'answered'::character varying,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    whatsapp_user_id integer,
    normalized_query text,
    confidence_score double precision,
    matched_kb_id integer,
    assigned_to_email character varying,
    assigned_to_name character varying,
    resolved_by integer,
    resolved_at timestamp without time zone,
    normalized_text text,
    detected_language character varying(50),
    intent_label character varying(100),
    matched_attachment_id integer,
    escalation_reason text,
    assigned_to integer,
    resolution_type character varying(20),
    last_response_at timestamp without time zone,
    escalated_at timestamp without time zone,
    session_id integer,
    whatsapp_number character varying,
    CONSTRAINT chk_query_source CHECK (((source)::text = ANY ((ARRAY['mobile'::character varying, 'whatsapp'::character varying])::text[]))),
    CONSTRAINT chk_query_status CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'processing'::character varying, 'answered'::character varying, 'escalated'::character varying, 'assigned'::character varying, 'resolved'::character varying, 'closed'::character varying])::text[]))),
    CONSTRAINT queries_source_check CHECK (((source)::text = ANY ((ARRAY['mobile'::character varying, 'web'::character varying, 'whatsapp'::character varying, 'admin'::character varying])::text[]))),
    CONSTRAINT queries_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'processing'::character varying, 'answered'::character varying, 'escalated'::character varying, 'assigned'::character varying, 'resolved'::character varying, 'closed'::character varying])::text[])))
);


ALTER TABLE software_engineering.queries OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 17040)
-- Name: queries_query_id_seq; Type: SEQUENCE; Schema: software_engineering; Owner: postgres
--

CREATE SEQUENCE software_engineering.queries_query_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE software_engineering.queries_query_id_seq OWNER TO postgres;

--
-- TOC entry 5322 (class 0 OID 0)
-- Dependencies: 239
-- Name: queries_query_id_seq; Type: SEQUENCE OWNED BY; Schema: software_engineering; Owner: postgres
--

ALTER SEQUENCE software_engineering.queries_query_id_seq OWNED BY software_engineering.queries.query_id;


--
-- TOC entry 265 (class 1259 OID 17585)
-- Name: query_events; Type: TABLE; Schema: software_engineering; Owner: postgres
--

CREATE TABLE software_engineering.query_events (
    event_id integer NOT NULL,
    query_id integer NOT NULL,
    event_type character varying(50) NOT NULL,
    event_message text,
    created_by integer,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE software_engineering.query_events OWNER TO postgres;

--
-- TOC entry 264 (class 1259 OID 17584)
-- Name: query_events_event_id_seq; Type: SEQUENCE; Schema: software_engineering; Owner: postgres
--

CREATE SEQUENCE software_engineering.query_events_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE software_engineering.query_events_event_id_seq OWNER TO postgres;

--
-- TOC entry 5323 (class 0 OID 0)
-- Dependencies: 264
-- Name: query_events_event_id_seq; Type: SEQUENCE OWNED BY; Schema: software_engineering; Owner: postgres
--

ALTER SEQUENCE software_engineering.query_events_event_id_seq OWNED BY software_engineering.query_events.event_id;


--
-- TOC entry 242 (class 1259 OID 17062)
-- Name: responses; Type: TABLE; Schema: software_engineering; Owner: postgres
--

CREATE TABLE software_engineering.responses (
    response_id integer NOT NULL,
    responder_id integer,
    response_text text NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    query_id integer,
    response_source character varying(20) DEFAULT 'ai'::character varying,
    document_name character varying(255),
    document_url text,
    response_type character varying(20) DEFAULT 'ai'::character varying,
    confidence_score double precision DEFAULT 0,
    tone_used character varying(50),
    source_evidence text,
    attachment_id integer,
    updated_at timestamp without time zone,
    CONSTRAINT chk_response_source CHECK (((response_source)::text = ANY ((ARRAY['ai'::character varying, 'staff'::character varying])::text[])))
);


ALTER TABLE software_engineering.responses OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 17061)
-- Name: responses_response_id_seq; Type: SEQUENCE; Schema: software_engineering; Owner: postgres
--

CREATE SEQUENCE software_engineering.responses_response_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE software_engineering.responses_response_id_seq OWNER TO postgres;

--
-- TOC entry 5324 (class 0 OID 0)
-- Dependencies: 241
-- Name: responses_response_id_seq; Type: SEQUENCE OWNED BY; Schema: software_engineering; Owner: postgres
--

ALTER SEQUENCE software_engineering.responses_response_id_seq OWNED BY software_engineering.responses.response_id;


--
-- TOC entry 267 (class 1259 OID 17604)
-- Name: staff_assignments; Type: TABLE; Schema: software_engineering; Owner: postgres
--

CREATE TABLE software_engineering.staff_assignments (
    assignment_id integer NOT NULL,
    query_id integer NOT NULL,
    assigned_to integer NOT NULL,
    assigned_by integer,
    notes text,
    status character varying(20) DEFAULT 'assigned'::character varying,
    assigned_at timestamp without time zone DEFAULT now()
);


ALTER TABLE software_engineering.staff_assignments OWNER TO postgres;

--
-- TOC entry 266 (class 1259 OID 17603)
-- Name: staff_assignments_assignment_id_seq; Type: SEQUENCE; Schema: software_engineering; Owner: postgres
--

CREATE SEQUENCE software_engineering.staff_assignments_assignment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE software_engineering.staff_assignments_assignment_id_seq OWNER TO postgres;

--
-- TOC entry 5325 (class 0 OID 0)
-- Dependencies: 266
-- Name: staff_assignments_assignment_id_seq; Type: SEQUENCE OWNED BY; Schema: software_engineering; Owner: postgres
--

ALTER SEQUENCE software_engineering.staff_assignments_assignment_id_seq OWNED BY software_engineering.staff_assignments.assignment_id;


--
-- TOC entry 4989 (class 2604 OID 16663)
-- Name: activity_logs log_id; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.activity_logs ALTER COLUMN log_id SET DEFAULT nextval('core.activity_logs_log_id_seq'::regclass);


--
-- TOC entry 5038 (class 2604 OID 17639)
-- Name: app_feedback feedback_id; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.app_feedback ALTER COLUMN feedback_id SET DEFAULT nextval('core.app_feedback_feedback_id_seq'::regclass);


--
-- TOC entry 4983 (class 2604 OID 16614)
-- Name: auth_tokens token_id; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.auth_tokens ALTER COLUMN token_id SET DEFAULT nextval('core.auth_tokens_token_id_seq'::regclass);


--
-- TOC entry 4985 (class 2604 OID 16631)
-- Name: departments department_id; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.departments ALTER COLUMN department_id SET DEFAULT nextval('core.departments_department_id_seq'::regclass);


--
-- TOC entry 4987 (class 2604 OID 16646)
-- Name: feedback feedback_id; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.feedback ALTER COLUMN feedback_id SET DEFAULT nextval('core.feedback_feedback_id_seq'::regclass);


--
-- TOC entry 5027 (class 2604 OID 17519)
-- Name: notifications notification_id; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.notifications ALTER COLUMN notification_id SET DEFAULT nextval('core.notifications_notification_id_seq'::regclass);


--
-- TOC entry 5024 (class 2604 OID 17391)
-- Name: password_reset_otps id; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.password_reset_otps ALTER COLUMN id SET DEFAULT nextval('core.password_reset_otps_id_seq'::regclass);


--
-- TOC entry 5014 (class 2604 OID 17138)
-- Name: roles role_id; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.roles ALTER COLUMN role_id SET DEFAULT nextval('core.roles_role_id_seq'::regclass);


--
-- TOC entry 4977 (class 2604 OID 16596)
-- Name: users user_id; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.users ALTER COLUMN user_id SET DEFAULT nextval('core.users_user_id_seq'::regclass);


--
-- TOC entry 4979 (class 2604 OID 17353)
-- Name: users id; Type: DEFAULT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.users ALTER COLUMN id SET DEFAULT nextval('core.users_id_seq'::regclass);


--
-- TOC entry 5011 (class 2604 OID 17116)
-- Name: external_systems system_id; Type: DEFAULT; Schema: integration; Owner: postgres
--

ALTER TABLE ONLY integration.external_systems ALTER COLUMN system_id SET DEFAULT nextval('integration.external_systems_system_id_seq'::regclass);


--
-- TOC entry 5008 (class 2604 OID 17094)
-- Name: whatsapp_messages message_id; Type: DEFAULT; Schema: integration; Owner: postgres
--

ALTER TABLE ONLY integration.whatsapp_messages ALTER COLUMN message_id SET DEFAULT nextval('integration.whatsapp_messages_message_id_seq'::regclass);


--
-- TOC entry 5006 (class 2604 OID 17082)
-- Name: whatsapp_users whatsapp_user_id; Type: DEFAULT; Schema: integration; Owner: postgres
--

ALTER TABLE ONLY integration.whatsapp_users ALTER COLUMN whatsapp_user_id SET DEFAULT nextval('integration.whatsapp_users_whatsapp_user_id_seq'::regclass);


--
-- TOC entry 5018 (class 2604 OID 17312)
-- Name: knowledge_base id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.knowledge_base ALTER COLUMN id SET DEFAULT nextval('public.knowledge_base_id_seq'::regclass);


--
-- TOC entry 5021 (class 2604 OID 17332)
-- Name: password_reset_otps id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_otps ALTER COLUMN id SET DEFAULT nextval('public.password_reset_otps_id_seq'::regclass);


--
-- TOC entry 5015 (class 2604 OID 17297)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4995 (class 2604 OID 16992)
-- Name: attachments attachment_id; Type: DEFAULT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.attachments ALTER COLUMN attachment_id SET DEFAULT nextval('software_engineering.attachments_attachment_id_seq'::regclass);


--
-- TOC entry 5040 (class 2604 OID 17663)
-- Name: chat_sessions session_id; Type: DEFAULT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.chat_sessions ALTER COLUMN session_id SET DEFAULT nextval('software_engineering.chat_sessions_session_id_seq'::regclass);


--
-- TOC entry 4991 (class 2604 OID 16951)
-- Name: kb_category category_id; Type: DEFAULT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.kb_category ALTER COLUMN category_id SET DEFAULT nextval('software_engineering.kb_category_category_id_seq'::regclass);


--
-- TOC entry 5031 (class 2604 OID 17564)
-- Name: kb_chunks chunk_id; Type: DEFAULT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.kb_chunks ALTER COLUMN chunk_id SET DEFAULT nextval('software_engineering.kb_chunks_chunk_id_seq'::regclass);


--
-- TOC entry 4993 (class 2604 OID 16968)
-- Name: knowledge_base kb_id; Type: DEFAULT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.knowledge_base ALTER COLUMN kb_id SET DEFAULT nextval('software_engineering.knowledge_base_kb_id_seq'::regclass);


--
-- TOC entry 4998 (class 2604 OID 17044)
-- Name: queries query_id; Type: DEFAULT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.queries ALTER COLUMN query_id SET DEFAULT nextval('software_engineering.queries_query_id_seq'::regclass);


--
-- TOC entry 5033 (class 2604 OID 17588)
-- Name: query_events event_id; Type: DEFAULT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.query_events ALTER COLUMN event_id SET DEFAULT nextval('software_engineering.query_events_event_id_seq'::regclass);


--
-- TOC entry 5001 (class 2604 OID 17065)
-- Name: responses response_id; Type: DEFAULT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.responses ALTER COLUMN response_id SET DEFAULT nextval('software_engineering.responses_response_id_seq'::regclass);


--
-- TOC entry 5035 (class 2604 OID 17607)
-- Name: staff_assignments assignment_id; Type: DEFAULT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.staff_assignments ALTER COLUMN assignment_id SET DEFAULT nextval('software_engineering.staff_assignments_assignment_id_seq'::regclass);


--
-- TOC entry 5068 (class 2606 OID 16669)
-- Name: activity_logs activity_logs_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.activity_logs
    ADD CONSTRAINT activity_logs_pkey PRIMARY KEY (log_id);


--
-- TOC entry 5115 (class 2606 OID 17647)
-- Name: app_feedback app_feedback_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.app_feedback
    ADD CONSTRAINT app_feedback_pkey PRIMARY KEY (feedback_id);


--
-- TOC entry 5060 (class 2606 OID 16621)
-- Name: auth_tokens auth_tokens_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.auth_tokens
    ADD CONSTRAINT auth_tokens_pkey PRIMARY KEY (token_id);


--
-- TOC entry 5062 (class 2606 OID 16641)
-- Name: departments departments_department_key_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.departments
    ADD CONSTRAINT departments_department_key_key UNIQUE (department_key);


--
-- TOC entry 5064 (class 2606 OID 16639)
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (department_id);


--
-- TOC entry 5066 (class 2606 OID 16653)
-- Name: feedback feedback_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.feedback
    ADD CONSTRAINT feedback_pkey PRIMARY KEY (feedback_id);


--
-- TOC entry 5107 (class 2606 OID 17530)
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (notification_id);


--
-- TOC entry 5105 (class 2606 OID 17402)
-- Name: password_reset_otps password_reset_otps_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.password_reset_otps
    ADD CONSTRAINT password_reset_otps_pkey PRIMARY KEY (id);


--
-- TOC entry 5092 (class 2606 OID 17145)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role_id);


--
-- TOC entry 5094 (class 2606 OID 17147)
-- Name: roles roles_role_name_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.roles
    ADD CONSTRAINT roles_role_name_key UNIQUE (role_name);


--
-- TOC entry 5054 (class 2606 OID 16609)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 5056 (class 2606 OID 16605)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 5058 (class 2606 OID 16607)
-- Name: users users_roll_number_key; Type: CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.users
    ADD CONSTRAINT users_roll_number_key UNIQUE (roll_number);


--
-- TOC entry 5090 (class 2606 OID 17123)
-- Name: external_systems external_systems_pkey; Type: CONSTRAINT; Schema: integration; Owner: postgres
--

ALTER TABLE ONLY integration.external_systems
    ADD CONSTRAINT external_systems_pkey PRIMARY KEY (system_id);


--
-- TOC entry 5088 (class 2606 OID 17101)
-- Name: whatsapp_messages whatsapp_messages_pkey; Type: CONSTRAINT; Schema: integration; Owner: postgres
--

ALTER TABLE ONLY integration.whatsapp_messages
    ADD CONSTRAINT whatsapp_messages_pkey PRIMARY KEY (message_id);


--
-- TOC entry 5083 (class 2606 OID 17089)
-- Name: whatsapp_users whatsapp_users_phone_number_key; Type: CONSTRAINT; Schema: integration; Owner: postgres
--

ALTER TABLE ONLY integration.whatsapp_users
    ADD CONSTRAINT whatsapp_users_phone_number_key UNIQUE (phone_number);


--
-- TOC entry 5085 (class 2606 OID 17087)
-- Name: whatsapp_users whatsapp_users_pkey; Type: CONSTRAINT; Schema: integration; Owner: postgres
--

ALTER TABLE ONLY integration.whatsapp_users
    ADD CONSTRAINT whatsapp_users_pkey PRIMARY KEY (whatsapp_user_id);


--
-- TOC entry 5101 (class 2606 OID 17321)
-- Name: knowledge_base knowledge_base_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.knowledge_base
    ADD CONSTRAINT knowledge_base_pkey PRIMARY KEY (id);


--
-- TOC entry 5103 (class 2606 OID 17343)
-- Name: password_reset_otps password_reset_otps_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_otps
    ADD CONSTRAINT password_reset_otps_pkey PRIMARY KEY (id);


--
-- TOC entry 5098 (class 2606 OID 17305)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 5077 (class 2606 OID 16999)
-- Name: attachments attachments_pkey; Type: CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.attachments
    ADD CONSTRAINT attachments_pkey PRIMARY KEY (attachment_id);


--
-- TOC entry 5117 (class 2606 OID 17668)
-- Name: chat_sessions chat_sessions_pkey; Type: CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.chat_sessions
    ADD CONSTRAINT chat_sessions_pkey PRIMARY KEY (session_id);


--
-- TOC entry 5070 (class 2606 OID 16958)
-- Name: kb_category kb_category_pkey; Type: CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.kb_category
    ADD CONSTRAINT kb_category_pkey PRIMARY KEY (category_id);


--
-- TOC entry 5109 (class 2606 OID 17573)
-- Name: kb_chunks kb_chunks_pkey; Type: CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.kb_chunks
    ADD CONSTRAINT kb_chunks_pkey PRIMARY KEY (chunk_id);


--
-- TOC entry 5075 (class 2606 OID 16977)
-- Name: knowledge_base knowledge_base_pkey; Type: CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.knowledge_base
    ADD CONSTRAINT knowledge_base_pkey PRIMARY KEY (kb_id);


--
-- TOC entry 5079 (class 2606 OID 17055)
-- Name: queries queries_pkey; Type: CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.queries
    ADD CONSTRAINT queries_pkey PRIMARY KEY (query_id);


--
-- TOC entry 5111 (class 2606 OID 17596)
-- Name: query_events query_events_pkey; Type: CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.query_events
    ADD CONSTRAINT query_events_pkey PRIMARY KEY (event_id);


--
-- TOC entry 5081 (class 2606 OID 17072)
-- Name: responses responses_pkey; Type: CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.responses
    ADD CONSTRAINT responses_pkey PRIMARY KEY (response_id);


--
-- TOC entry 5113 (class 2606 OID 17616)
-- Name: staff_assignments staff_assignments_pkey; Type: CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.staff_assignments
    ADD CONSTRAINT staff_assignments_pkey PRIMARY KEY (assignment_id);


--
-- TOC entry 5086 (class 1259 OID 17680)
-- Name: uq_whatsapp_messages_meta_message_id; Type: INDEX; Schema: integration; Owner: postgres
--

CREATE UNIQUE INDEX uq_whatsapp_messages_meta_message_id ON integration.whatsapp_messages USING btree (meta_message_id) WHERE (meta_message_id IS NOT NULL);


--
-- TOC entry 5099 (class 1259 OID 17322)
-- Name: ix_knowledge_base_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_knowledge_base_id ON public.knowledge_base USING btree (id);


--
-- TOC entry 5095 (class 1259 OID 17307)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 5096 (class 1259 OID 17306)
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- TOC entry 5071 (class 1259 OID 17514)
-- Name: kb_content_trgm_idx; Type: INDEX; Schema: software_engineering; Owner: postgres
--

CREATE INDEX kb_content_trgm_idx ON software_engineering.knowledge_base USING gin (content public.gin_trgm_ops);


--
-- TOC entry 5072 (class 1259 OID 17512)
-- Name: kb_search_vector_idx; Type: INDEX; Schema: software_engineering; Owner: postgres
--

CREATE INDEX kb_search_vector_idx ON software_engineering.knowledge_base USING gin (search_vector);


--
-- TOC entry 5073 (class 1259 OID 17513)
-- Name: kb_title_trgm_idx; Type: INDEX; Schema: software_engineering; Owner: postgres
--

CREATE INDEX kb_title_trgm_idx ON software_engineering.knowledge_base USING gin (title public.gin_trgm_ops);


--
-- TOC entry 5147 (class 2620 OID 17325)
-- Name: users trg_sync_user_role; Type: TRIGGER; Schema: core; Owner: postgres
--

CREATE TRIGGER trg_sync_user_role BEFORE INSERT OR UPDATE OF role_id ON core.users FOR EACH ROW EXECUTE FUNCTION core.sync_user_role_from_role_id();


--
-- TOC entry 5121 (class 2606 OID 16670)
-- Name: activity_logs activity_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.activity_logs
    ADD CONSTRAINT activity_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES core.users(user_id) ON DELETE SET NULL;


--
-- TOC entry 5145 (class 2606 OID 17648)
-- Name: app_feedback app_feedback_user_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.app_feedback
    ADD CONSTRAINT app_feedback_user_id_fkey FOREIGN KEY (user_id) REFERENCES core.users(user_id) ON DELETE SET NULL;


--
-- TOC entry 5119 (class 2606 OID 16622)
-- Name: auth_tokens auth_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.auth_tokens
    ADD CONSTRAINT auth_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES core.users(user_id) ON DELETE CASCADE;


--
-- TOC entry 5120 (class 2606 OID 16654)
-- Name: feedback feedback_user_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.feedback
    ADD CONSTRAINT feedback_user_id_fkey FOREIGN KEY (user_id) REFERENCES core.users(user_id) ON DELETE SET NULL;


--
-- TOC entry 5138 (class 2606 OID 17531)
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES core.users(user_id);


--
-- TOC entry 5137 (class 2606 OID 17403)
-- Name: password_reset_otps password_reset_otps_user_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.password_reset_otps
    ADD CONSTRAINT password_reset_otps_user_id_fkey FOREIGN KEY (user_id) REFERENCES core.users(user_id);


--
-- TOC entry 5118 (class 2606 OID 17148)
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: postgres
--

ALTER TABLE ONLY core.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES core.roles(role_id) ON DELETE SET NULL;


--
-- TOC entry 5133 (class 2606 OID 17654)
-- Name: whatsapp_messages fk_whatsapp_messages_query; Type: FK CONSTRAINT; Schema: integration; Owner: postgres
--

ALTER TABLE ONLY integration.whatsapp_messages
    ADD CONSTRAINT fk_whatsapp_messages_query FOREIGN KEY (query_id) REFERENCES software_engineering.queries(query_id) ON DELETE SET NULL;


--
-- TOC entry 5134 (class 2606 OID 17107)
-- Name: whatsapp_messages whatsapp_messages_query_id_fkey; Type: FK CONSTRAINT; Schema: integration; Owner: postgres
--

ALTER TABLE ONLY integration.whatsapp_messages
    ADD CONSTRAINT whatsapp_messages_query_id_fkey FOREIGN KEY (query_id) REFERENCES software_engineering.queries(query_id) ON DELETE SET NULL;


--
-- TOC entry 5135 (class 2606 OID 17102)
-- Name: whatsapp_messages whatsapp_messages_whatsapp_user_id_fkey; Type: FK CONSTRAINT; Schema: integration; Owner: postgres
--

ALTER TABLE ONLY integration.whatsapp_messages
    ADD CONSTRAINT whatsapp_messages_whatsapp_user_id_fkey FOREIGN KEY (whatsapp_user_id) REFERENCES integration.whatsapp_users(whatsapp_user_id) ON DELETE CASCADE;


--
-- TOC entry 5136 (class 2606 OID 17344)
-- Name: password_reset_otps password_reset_otps_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_otps
    ADD CONSTRAINT password_reset_otps_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5125 (class 2606 OID 17000)
-- Name: attachments attachments_kb_id_fkey; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.attachments
    ADD CONSTRAINT attachments_kb_id_fkey FOREIGN KEY (kb_id) REFERENCES software_engineering.knowledge_base(kb_id) ON DELETE CASCADE;


--
-- TOC entry 5126 (class 2606 OID 17005)
-- Name: attachments attachments_uploaded_by_fkey; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.attachments
    ADD CONSTRAINT attachments_uploaded_by_fkey FOREIGN KEY (uploaded_by) REFERENCES core.users(user_id);


--
-- TOC entry 5146 (class 2606 OID 17669)
-- Name: chat_sessions chat_sessions_student_user_id_fkey; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.chat_sessions
    ADD CONSTRAINT chat_sessions_student_user_id_fkey FOREIGN KEY (student_user_id) REFERENCES core.users(user_id);


--
-- TOC entry 5127 (class 2606 OID 17422)
-- Name: queries fk_queries_matched_kb; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.queries
    ADD CONSTRAINT fk_queries_matched_kb FOREIGN KEY (matched_kb_id) REFERENCES software_engineering.knowledge_base(kb_id);


--
-- TOC entry 5128 (class 2606 OID 17124)
-- Name: queries fk_queries_whatsapp_user; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.queries
    ADD CONSTRAINT fk_queries_whatsapp_user FOREIGN KEY (whatsapp_user_id) REFERENCES integration.whatsapp_users(whatsapp_user_id) ON DELETE SET NULL;


--
-- TOC entry 5131 (class 2606 OID 17129)
-- Name: responses fk_responses_query; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.responses
    ADD CONSTRAINT fk_responses_query FOREIGN KEY (query_id) REFERENCES software_engineering.queries(query_id) ON DELETE CASCADE;


--
-- TOC entry 5122 (class 2606 OID 16959)
-- Name: kb_category kb_category_created_by_fkey; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.kb_category
    ADD CONSTRAINT kb_category_created_by_fkey FOREIGN KEY (created_by) REFERENCES core.users(user_id);


--
-- TOC entry 5139 (class 2606 OID 17579)
-- Name: kb_chunks kb_chunks_attachment_id_fkey; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.kb_chunks
    ADD CONSTRAINT kb_chunks_attachment_id_fkey FOREIGN KEY (attachment_id) REFERENCES software_engineering.attachments(attachment_id) ON DELETE SET NULL;


--
-- TOC entry 5140 (class 2606 OID 17574)
-- Name: kb_chunks kb_chunks_kb_id_fkey; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.kb_chunks
    ADD CONSTRAINT kb_chunks_kb_id_fkey FOREIGN KEY (kb_id) REFERENCES software_engineering.knowledge_base(kb_id) ON DELETE CASCADE;


--
-- TOC entry 5123 (class 2606 OID 16978)
-- Name: knowledge_base knowledge_base_category_id_fkey; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.knowledge_base
    ADD CONSTRAINT knowledge_base_category_id_fkey FOREIGN KEY (category_id) REFERENCES software_engineering.kb_category(category_id);


--
-- TOC entry 5124 (class 2606 OID 16983)
-- Name: knowledge_base knowledge_base_created_by_fkey; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.knowledge_base
    ADD CONSTRAINT knowledge_base_created_by_fkey FOREIGN KEY (created_by) REFERENCES core.users(user_id);


--
-- TOC entry 5129 (class 2606 OID 17674)
-- Name: queries queries_session_id_fkey; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.queries
    ADD CONSTRAINT queries_session_id_fkey FOREIGN KEY (session_id) REFERENCES software_engineering.chat_sessions(session_id);


--
-- TOC entry 5130 (class 2606 OID 17056)
-- Name: queries queries_student_user_id_fkey; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.queries
    ADD CONSTRAINT queries_student_user_id_fkey FOREIGN KEY (student_user_id) REFERENCES core.users(user_id) ON DELETE SET NULL;


--
-- TOC entry 5141 (class 2606 OID 17597)
-- Name: query_events query_events_query_id_fkey; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.query_events
    ADD CONSTRAINT query_events_query_id_fkey FOREIGN KEY (query_id) REFERENCES software_engineering.queries(query_id) ON DELETE CASCADE;


--
-- TOC entry 5132 (class 2606 OID 17073)
-- Name: responses responses_responder_id_fkey; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.responses
    ADD CONSTRAINT responses_responder_id_fkey FOREIGN KEY (responder_id) REFERENCES core.users(user_id);


--
-- TOC entry 5142 (class 2606 OID 17627)
-- Name: staff_assignments staff_assignments_assigned_by_fkey; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.staff_assignments
    ADD CONSTRAINT staff_assignments_assigned_by_fkey FOREIGN KEY (assigned_by) REFERENCES core.users(user_id) ON DELETE SET NULL;


--
-- TOC entry 5143 (class 2606 OID 17622)
-- Name: staff_assignments staff_assignments_assigned_to_fkey; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.staff_assignments
    ADD CONSTRAINT staff_assignments_assigned_to_fkey FOREIGN KEY (assigned_to) REFERENCES core.users(user_id) ON DELETE CASCADE;


--
-- TOC entry 5144 (class 2606 OID 17617)
-- Name: staff_assignments staff_assignments_query_id_fkey; Type: FK CONSTRAINT; Schema: software_engineering; Owner: postgres
--

ALTER TABLE ONLY software_engineering.staff_assignments
    ADD CONSTRAINT staff_assignments_query_id_fkey FOREIGN KEY (query_id) REFERENCES software_engineering.queries(query_id) ON DELETE CASCADE;


-- Completed on 2026-07-16 05:51:42

--
-- PostgreSQL database dump complete
--

\unrestrict nzbQ9FypPp0TyC4PFtaSmBg5Wg0EhEXgLTYXnFiakxkSYh7OwLu2uuvJei6PaaZ

