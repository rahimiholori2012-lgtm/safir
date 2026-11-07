import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="ثبت‌نام سفیران سلامت", page_icon="🥗", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f0f9ff; }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        border-radius: 12px;
        padding: 10px 24px;
        border: none;
        width: 100%;
    }
    h1, h2, h3 { color: #1e3a8a; text-align: center; }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "registered_students.csv"

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["name", "father_name", "grade", "school", "role", "phone", "messenger"])
    df_init.to_csv(DATA_FILE, index=False)

def get_data():
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

CAPACITIES = {"اول": 4, " دوم": 4, "سوم": 6, "چهارم": 6, "پنجم": 4, "ششم": 6}
ROLES = ["سفیر سلامت تغذیه", "سفیر سلامت بهداشت", "سفیر سلامت محیط‌یار", "سفیر سلامت ایمنی و کمک‌های اولیه"]

st.title("🌟 سامانه ثبت‌نام سفیران سلامت 🌟")
st.subheader("سال تحصیلی ۱۴۰۵–۱۴۰۶ | مراقب سلامت: رحیمی")

menu = st.sidebar.radio("منو", ["ثبت‌نام دانش‌آموز", "پنل مدیریت (مراقب سلامت)"])

if menu == "ثبت‌نام دانش‌آموز":
    st.info("🎈 دانش‌آموز عزیز، لطفاً اطلاعات خود را وارد کن!")

    with st.form("registration_form"):
        name = st.text_input("نام و نام خانوادگی دانش‌آموز")
        father_name = st.text_input("نام پدر")
        grade = st.selectbox("پایه تحصیلی", ["انتخاب کنید...", "اول", " دوم", "سوم", "چهارم", "پنجم", "ششم"])
        
        school = ""
        if grade in ["اول", " دوم", "سوم"]:
            school = "مدرسه مهدیه"
        elif grade in ["چهارم", "پنجم", "ششم"]:
            school = "مدرسه پیام"
            
        if school:
            st.success(f"🏫 مدرسه شما: **{school}**")

        phone = st.text_input("شماره تماس والد (واتساپ / شاد)")
        messenger = st.radio("روش ارتباطی اصلی", ["واتساپ", "شاد"])
        
        uploaded_file = st.file_uploader("عکس پرسنلی دانش‌آموز", type=["jpg", "png", "jpeg"])
        is_test = st.checkbox("🧪 حالت تست (مخصوص مراقب سلامت - بدون کسر ظرفیت)")

        submit = st.form_submit_button("🎓 ثبت‌نام و دریافت کارت و ابلاغیه")

    if submit:
        if not name or not father_name or grade == "انتخاب کنید..." or not phone or not uploaded_file:
            st.error("لطفاً تمامی موارد را کامل کنید.")
        else:
            df = get_data()
            if not is_test:
                new_row = {"name": name, "father_name": father_name, "grade": grade, "school": school, "role": "سفیر سلامت", "phone": phone, "messenger": messenger}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df)
                st.balloons()
            st.success("ثبت‌نام با موفقیت انجام شد! کارت و ابلاغیه شما آماده است.")
            st.image(uploaded_file, width=180, caption=name)

elif menu == "پنل مدیریت (مراقب سلامت)":
    password = st.sidebar.text_input("رمز عبور مدیر", type="password")
    if password == "rahimi1405":
        st.success("پنل مدیریت:")
        df = get_data()
        st.dataframe(df)
    else:
        st.error("رمز عبور اشتباه است.")
