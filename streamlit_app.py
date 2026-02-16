import threading
import time
from typing import Optional, Dict, Any

import requests
import streamlit as st
import uvicorn


BACKEND_URL = "http://localhost:8000"


def start_backend() -> None:
    config = uvicorn.Config("backend.app.main:app", host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    time.sleep(3)


@st.cache_resource
def init_backend() -> bool:
    start_backend()
    return True


def api_post(path: str, json: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None, files: Any = None) -> requests.Response:
    token = st.session_state.get("token")
    headers: Dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = f"{BACKEND_URL}{path}"
    return requests.post(url, json=json, data=data, files=files, headers=headers, timeout=300)


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

    init_backend()

    if "token" not in st.session_state:
        st.session_state["token"] = None

    st.title("DocVision AI OCR")
    st.write("Register or login, then upload a document to run routed OCR.")

    login_tab, upload_tab = st.tabs(["Auth", "Upload and OCR"])

    with login_tab:
        st.subheader("Register")
        with st.form("register_form"):
            reg_email = st.text_input("Email", key="reg_email")
            reg_name = st.text_input("Full name", key="reg_name")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            submitted = st.form_submit_button("Register")
            if submitted:
                do_register(reg_email, reg_password, reg_name)

        st.subheader("Login")
        with st.form("login_form"):
            log_email = st.text_input("Email", key="log_email")
            log_password = st.text_input("Password", type="password", key="log_password")
            submitted_login = st.form_submit_button("Login")
            if submitted_login:
                do_login(log_email, log_password)

        if st.session_state.get("token"):
            if st.button("Logout"):
                do_logout()

    with upload_tab:
        if not st.session_state.get("token"):
            st.info("You must login before uploading documents.")
            return

        st.subheader("Upload Document")
        file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if st.button("Run OCR"):
            do_ocr(file)


if __name__ == "__main__":
    main()

