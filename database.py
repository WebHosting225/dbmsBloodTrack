import firebase_admin
import extra_streamlit_components as stx
import streamlit as st
from firebase_admin import credentials
from firebase_admin import firestore


@st.cache_resource
def getDb():
    try:
        cred = credentials.Certificate("dbmsbloodtra-firebase-adminsdk-l08e9-0c0d545f37.json")  # noqa
    except FileNotFoundError:
        firebaseCreds = st.secrets.firebase
        cred = credentials.Certificate({
            "type": firebaseCreds["type"],
            "project_id": firebaseCreds["project_id"],
            "private_key_id": firebaseCreds["private_key_id"],
            "private_key": firebaseCreds["private_key"],
            "client_email": firebaseCreds["client_email"],
            "client_id": firebaseCreds["client_id"],
            "auth_uri": firebaseCreds["auth_uri"],
            "token_uri": firebaseCreds["token_uri"],
            "auth_provider_x509_cert_url": firebaseCreds["auth_provider_x509_cert_url"],
            "client_x509_cert_url": firebaseCreds["client_x509_cert_url"],
            "universe_domain": firebaseCreds["universe_domain"],
        })
    firebase_admin.initialize_app(cred)
    return firestore.client()


db = getDb()
users = db.collection(u"Users")
banks = db.collection(u"Banks")
sessions = db.collection(u"Sessions")

bloodTypes = {
    "AB+": ["AB+"],
    "AB-": ["AB+", "AB-"],
    "A+": ["AB+", "A+"],
    "A-": ["AB+", "AB-", "A+", "A-"],
    "B+": ["AB+", "B+"],
    "B-": ["AB+", "AB-", "B+", "B-"],
    "O+": ["AB+", "A+", "B+", "O+"],
    "O-": ["AB+", "AB-", "A+", "A-", "B+", "B-", "O+", "O-"],
    "Duffy": ["Duffy"],
    "Kell": ["Kell"],
    "Kidd": ["Kidd"],
    "Lutheran": ["Lutheran"],
    "Other": ["Other"],
}

requirements = [
    "Blood",
    "Plasma",
    "Platelets",
    "Other",
]


def getCookies():
    return stx.CookieManager()
