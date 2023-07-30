import firebase_admin
import extra_streamlit_components as stx
import streamlit as st
from firebase_admin import credentials
from firebase_admin import firestore


@st.cache_resource
def getDb():
    cred = credentials.Certificate("dbmsbloodtra-firebase-adminsdk-l08e9-2fbb65dd07.json")  # noqa
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
