from typing import Optional, Dict, Any

import streamlit as st
from fastapi.testclient import TestClient
from backend.app.main import app


client = TestClient(app)


def api_post(
    path: str,
    json: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    files: Any = None,
):
    token = st.session_state.get("token")
    headers: Dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return client.post(path, json=json, data=data, files=files, headers=headers)


def do_register(email: str, password: str, full_name: str) -> None:
    payload = {"email": email, "password": password, "full_name": full_name}
    resp = api_post("/auth/register", json=payload)
    if resp.status_code != 200:
        st.error(f"Register failed: {resp.text}")
        return
    st.success("Registration successful. You can now log in.")


def do_login(email: str, password: str) -> None:
    data = {"username": email, "password": password}
    resp = api_post("/auth/login", data=data)
    if resp.status_code != 200:
        st.error(f"Login failed: {resp.text}")
        return
    token = resp.json().get("access_token")
    if not token:
        st.error("No access token returned")
        return
    st.session_state["token"] = token
    st.success("Logged in successfully.")


def do_logout() -> None:
    try:
        api_post("/auth/logout")
    except Exception:
        pass
    st.session_state["token"] = None
    st.success("Logged out.")


def do_ocr(file) -> None:
    if not file:
        st.warning("Please upload a file first.")
        return
    files = {"file": (file.name, file.getvalue(), file.type)}
    resp = api_post("/api/ocr/routed", files=files)
    if resp.status_code != 200:
        st.error(f"OCR failed: {resp.text}")
        return
    data = resp.json()
    st.subheader("OCR Result")
    st.json(data)


def main() -> None:
    st.set_page_config(page_title="DocVision AI OCR", layout="wide")

    if "token" not in st.session_state:
        st.session_state["token"] = None

    st.markdown(
        """
        <style>
        .auth-panel {
            border-radius: 16px;
            box-shadow: 0 18px 35px rgba(0,0,0,0.08);
            padding: 32px 36px;
            background: #ffffff;
        }
        .auth-panel-gradient {
            background: linear-gradient(135deg, #ff416c, #ff4b2b);
            color: #ffffff;
        }
        .auth-heading {
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 12px;
        }
        .auth-text {
            font-size: 14px;
            color: #777;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h1 style='text-align: center; margin-top: 1rem;'>DocVision AI OCR</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #666;'>Sign in to your account or create a new one to continue.</p>",
        unsafe_allow_html=True,
    )

    main_left, main_right = st.columns([2, 1])

    with main_left:
        left_col, right_col = st.columns(2)

        with left_col:
            st.markdown("<div class='auth-panel'>", unsafe_allow_html=True)
            st.markdown("<div class='auth-heading'>Sign in</div>", unsafe_allow_html=True)
            st.markdown(
                "<div class='auth-text'>Use your email and password to sign in.</div>",
                unsafe_allow_html=True,
            )

            with st.form("login_form"):
                log_email = st.text_input("Email", key="log_email")
                log_password = st.text_input("Password", type="password", key="log_password")
                submitted_login = st.form_submit_button("Sign in")
                if submitted_login:
                    do_login(log_email, log_password)

            if st.session_state.get("token"):
                if st.button("Logout"):
                    do_logout()

            st.markdown("</div>", unsafe_allow_html=True)

        with right_col:
            st.markdown("<div class='auth-panel auth-panel-gradient'>", unsafe_allow_html=True)
            st.markdown(
                "<div class='auth-heading'>Hello, Friend!</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='auth-text' style='color: rgba(255,255,255,0.9);'>Enter your personal details and start your journey with us.</div>",
                unsafe_allow_html=True,
            )

            with st.form("register_form"):
                reg_email = st.text_input("Email", key="reg_email")
                reg_name = st.text_input("Full name", key="reg_name")
                reg_password = st.text_input("Password", type="password", key="reg_password")
                submitted = st.form_submit_button("Sign up")
                if submitted:
                    do_register(reg_email, reg_password, reg_name)

            st.markdown("</div>", unsafe_allow_html=True)

    with main_right:
        st.subheader("Upload and OCR")
        if not st.session_state.get("token"):
            st.info("You must login before uploading documents.")
            return

        file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if st.button("Run OCR"):
            do_ocr(file)


if __name__ == "__main__":
    main()
