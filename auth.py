import hashlib
import hmac
import secrets

import streamlit as st

from models import User, get_session


def init_auth_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""


def _clean_text(value):
    return (value or "").strip()


def hash_password(password):
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()
    return f"{salt}${digest}"


def verify_password(password, stored_password):
    try:
        salt, stored_digest = stored_password.split("$", 1)
    except ValueError:
        return False

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()
    return hmac.compare_digest(digest, stored_digest)


def set_logged_in_user(user):
    st.session_state.authenticated = True
    st.session_state.user_id = user.id
    st.session_state.user_name = user.name
    st.session_state.user_email = user.email


def signup_user(name, email, password):
    name = _clean_text(name)
    email = _clean_text(email).lower()

    if not name:
        return False, "Please enter your name."
    if not email:
        return False, "Please enter your email."
    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address."
    if len(password or "") < 6:
        return False, "Password must be at least 6 characters long."

    session = get_session()
    try:
        existing_user = session.query(User).filter(User.email == email).first()
        if existing_user:
            return False, "An account with this email already exists."

        user = User(
            name=name,
            email=email,
            password=hash_password(password)
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        set_logged_in_user(user)
        return True, "Signup successful."
    finally:
        session.close()


def login_user(email, password):
    email = _clean_text(email).lower()

    if not email or not password:
        return False, "Please enter both email and password."

    session = get_session()
    try:
        user = session.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password):
            return False, "Invalid email or password."

        set_logged_in_user(user)
        return True, "Login successful."
    finally:
        session.close()


def logout_user():
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.user_name = ""
    st.session_state.user_email = ""
    st.session_state.page = "home"


def get_current_user():
    user_id = st.session_state.get("user_id")
    if not user_id:
        return None

    session = get_session()
    try:
        return session.query(User).filter(User.id == user_id).first()
    finally:
        session.close()
