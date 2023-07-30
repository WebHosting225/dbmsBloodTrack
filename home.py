import streamlit as st
import pandas as pd

import database as db


def requestBlood():
    for_me = st.checkbox("For me", value=True)
    with st.form("requestBlood", clear_on_submit=True):
        col1, col2 = st.columns(2)
        if for_me:
            col1.write("")
            col1.info(f"Blood Type: {user.get('bloodGrp')}")
            blood_type = user.get("bloodGrp")
        else:
            blood_type = col1.selectbox("Blood Type", db.bloodTypes.keys(),
                                        index=list(db.bloodTypes.keys()).index(user.get("bloodGrp")) if for_me else 0)
        quantity = col2.number_input("Quantity (mL)", min_value=100, step=50)
        requirement = st.selectbox("Requirement", db.requirements)

        if not for_me:
            col1, col2 = st.columns(2)
            fullName = col1.text_input("Full Name")
            if not fullName: col1.error("Full Name is required")
            age = col2.number_input("Age", min_value=1, max_value=60, value=18)
            if not age: col2.error("Age is required")
            col1, col2 = st.columns(2)
            email = col1.text_input("Email")
            if not email: col1.error("Email is required")
            phone = col2.text_input("Phone")
            if not phone: col2.error("Phone is required")

        if st.form_submit_button("Request Blood"):
            if for_me:
                db.banks.add({
                    "user": user.reference,
                    "qnty": quantity,
                    "req": requirement,
                    "bloodGrp": blood_type,
                    "donor": None,
                    "for": {
                        "fullName": user.get("fullName"),
                        "age": user.get("age"),
                        "email": user.get("email"),
                        "phone": user.get("phoneNo"),
                    }
                })
            elif fullName and age and email and phone:
                db.banks.add({
                    "user": user.reference,
                    "qnty": quantity,
                    "req": requirement,
                    "bloodGrp": blood_type,
                    "donor": None,
                    "for": {
                        "fullName": fullName,
                        "age": age,
                        "email": email,
                        "phone": phone,
                    }
                })


def donateBlood():
    bankList = db.banks.where("user", "!=", user.reference).where("donor", "==", None)
    if not st.checkbox("Show All", value=False):
        bankList = bankList.where("bloodGrp", "in", db.bloodTypes[user.get("bloodGrp")])

    st.info(f"Your Blood Group {user.get('bloodGrp')} can donate to {', '.join(db.bloodTypes[user.get('bloodGrp')])}")
    items = list(map(lambda x: {**x.to_dict(), 'id': x.id}, bankList.get()))
    df = pd.DataFrame(items, columns=["id", "qnty", "req", "bloodGrp"])
    df.set_index("id", inplace=True)
    cols = st.columns((4, 2, 2, 2, 2))
    cols[0].write("RefId")
    cols[1].write("Quantity")
    cols[2].write("Requirement")
    cols[3].write("Blood Group")
    cols[4].write("Action")
    for i in df.index:
        cnt = st.empty()
        cols = cnt.columns((4, 2, 2, 2, 2))
        cols[0].write(i)
        cols[1].write(f"{df.loc[i, 'qnty']} mL")
        cols[2].write(df.loc[i, "req"])
        cols[3].write(df.loc[i, "bloodGrp"])
        if cols[4].button("Donate", key=i):
            db.banks.document(i).set({
                "donor": user.reference,
                "verified": False,
            }, merge=True)
            st.success("Your response has been recorded. Please wait for the Blood Bank to verify your request")
            cnt.empty()
    st.write("---")


cookies = db.getCookies()
session = db.sessions.document(cookies.get("sid"))

if not session.get().exists:
    st.markdown(
        """
        <a href="/auth" target="_self" onclick="return false;">Login or SignUp</a> to continue
        """,
        unsafe_allow_html=True
    )
else:
    st.header("Blood Bank")
    user = session.get().get("user").get()

    req, don = st.tabs(["Request Blood", "Donate Blood"])
    with req:
        requestBlood()
    with don:
        pass
        donateBlood()
