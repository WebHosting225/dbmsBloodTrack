import streamlit as st
import database as db


def donations():
    donationList = db.banks.where("donor", "==", user.reference).get()
    cols = st.columns((4, 2, 2, 2, 2))
    cols[0].write("RefId")
    cols[1].write("Quantity")
    cols[2].write("Requirement")
    cols[3].write("Blood Group")
    cols[4].write("Verified")
    for donation in donationList:
        cnt = st.empty()
        cols = cnt.columns((4, 2, 2, 2, 2))
        cols[0].write(donation.id)
        cols[1].write(f"{donation.get('qnty')} mL")
        cols[2].write(donation.get("req"))
        cols[3].write(donation.get("bloodGrp"))
        cols[4].write(donation.get("verified"))
    st.write("---")


def requests():
    requestList = db.banks.where("user", "==", user.reference).get()
    cols = st.columns((4, 2, 2, 2, 2))
    cols[0].write("RefId")
    cols[1].write("Quantity")
    cols[2].write("Requirement")
    cols[3].write("Blood Group")
    cols[4].write("Verified")
    for request in requestList:
        cnt = st.empty()
        cols = cnt.columns((4, 2, 2, 2, 2))
        cols[0].write(request.id)
        cols[1].write(f"{request.get('qnty')} mL")
        cols[2].write(request.get("req"))
        cols[3].write(request.get("bloodGrp"))
        if request.get("donor") is None:
            cols[4].write("Pending")
        elif request.get("verified"):
            cols[4].write(True)
        elif cols[4].button("Verify", key=request.id):
            db.banks.document(request.id).set({
                "verified": True,
            }, merge=True)
            st.experimental_rerun()
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

    dons, reqs = st.tabs(["Donations", "Requests"])
    with dons:
        donations()
    with reqs:
        requests()
