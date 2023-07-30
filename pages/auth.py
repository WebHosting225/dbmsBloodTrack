import datetime
import hashlib

import streamlit as st
import database as db


def hasher(s):
    return hashlib.sha256(s.encode()).hexdigest()


# todo: expire session
def login():
    st.title("Login")

    username = st.text_input("Username", key="login-username")
    password = st.text_input("Password", type="password", key="login-password")

    if st.button("Login"):
        if not authenticate(username, password): st.error("Invalid username or password")


def signup():
    st.title("Sign Up")

    username = st.text_input("Username")
    password = ""
    fullName = ""
    if username:
        if db.users.where("username", "==", username).get():
            st.error("Username already exists")
        else:
            st.success("Username available")
            col1, col2 = st.columns(2)
            password = col1.text_input("Password", type="password")
            confirmPassword = col2.text_input("Confirm Password", type="password")
            if password != confirmPassword:
                st.error("Passwords do not match")
                password = ""
            fullName = st.text_input("Full Name")
            if not fullName: st.error("Full Name is required")

    if password and fullName:
        col1, col2 = st.columns(2)
        age = col1.number_input("Age", min_value=16, max_value=60)
        if not age: st.error("Age is required")
        bloodGrp = col2.selectbox("Blood Group", db.bloodTypes.keys())
        if not bloodGrp: st.error("Blood Group is required")

        col1, col2 = st.columns(2)
        email = col1.text_input("Email")
        if not email: col1.error("Email is required")
        if db.users.where("email", "==", email).get():
            col1.error("Email already exists")
            email = ""
        phoneNo = col2.text_input("Phone Number")
        if not phoneNo: col2.error("Phone Number is required")
        if db.users.where("phoneNo", "==", phoneNo).get():
            col2.error("Phone Number already exists")
            phoneNo = ""

        if st.button("Sign Up") and age and bloodGrp and email and phoneNo:
            db.users.add({
                "username": username,
                "password": hasher(password),
                "fullName": fullName,
                "age": age,
                "bloodGrp": bloodGrp,
                "email": email,
                "phoneNo": phoneNo,
            })
            authenticate(username, password)


# todo resset password
def reset():
    st.title("Forgot Password")


def authenticate(username, password):
    user = db.users.where("username", "==", username).get()
    if user:
        user = user[0]
        if user.get("password") == hasher(password):
            exp = datetime.datetime.now() + datetime.timedelta(days=31)
            sid = db.sessions.add({
                "user": user.reference,
                "expr": exp.timestamp(),
            })[1].id
            cookies.set("sid", sid, expires_at=exp)
            return True
    return False


cookies = db.getCookies()
session = db.sessions.document(cookies.get("sid"))

if session.get().exists:
    user = session.get().get("user").get()
    st.success(f"You are logged in as {user.get('username')}")
    if st.button("Logout"):
        cookies.delete("sid")
        session.delete()
    st.markdown(
        """
        Continue to <a href="/home" target="_self" onclick="return false;">Home</a>
        """,
        unsafe_allow_html=True
    )
else:
    loginCol, signupCol, resetCol = st.tabs(["Login", "Sign Up", "Forgot Password"])
    with loginCol:
        login()
    with signupCol:
        signup()
    with resetCol:
        reset()
