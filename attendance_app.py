import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Staff Portal", layout="centered")

st.title("🏢 Staff Attendance & Leave System")
st.write("ဝန်ထမ်းများ အလုပ်တက်/ဆင်း မှတ်တမ်းနှင့် ခွင့်တိုင်ကြားရန်")

# Google Sheet နှင့် ချိတ်ဆက်ခြင်း
# Line 13 ဝန်းကျင်မှာ ဒီလိုလေး ပြောင်းကြည့်ပါ
conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)

# ဝန်ထမ်းစာရင်း (ဒီနေရာမှာ သင့်ဝန်ထမ်းအမည်များ ပြောင်းနိုင်ပါတယ်)
staff_list = ["Eithandar Kyaw", "Chaw Su Win", "Htar Ei Lynn", "Jeff", "HR"]

# Sidebar Menu
menu = ["🏠 Home", "⌚ Attendance", "📅 Leave Request", "📊 View Records"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "🏠 Home":
    st.info("Welcome! ဘယ်ဘက် Menu မှ မိမိလုပ်ဆောင်လိုသည်ကို ရွေးချယ်ပါ။")

elif choice == "⌚ Attendance":
    st.subheader("Daily Attendance (Check-in/out)")
    
    with st.form("attendance_form"):
        name = st.selectbox("မိမိအမည်ကို ရွေးပါ", staff_list)
        action = st.radio("လုပ်ဆောင်ချက်", ["Clock In", "Clock Out"])
        submit = st.form_submit_button("Submit")
        
        if submit:
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M:%S")
            
            # Google Sheet သို့ ပို့မည့် data ပြင်ဆင်ခြင်း
            new_data = pd.DataFrame([{
                "Name": name,
                "Date": current_date,
                "Clock_In": current_time if action == "Clock In" else "",
                "Clock_Out": current_time if action == "Clock Out" else ""
            }])
            
            # Google Sheet (Attendance tab) သို့ သိမ်းဆည်းခြင်း
            # append ကို သုံးပြီး data အသစ် ထပ်ထည့်ခိုင်းတာပါ
            conn.update(worksheet="Attendance", data=new_data)
            st.success(f"{name} အတွက် {action} လုပ်ဆောင်မှု အောင်မြင်ပါသည်။")

elif choice == "📅 Leave Request":
    st.subheader("ခွင့်တိုင်ကြားရန် ပုံစံ")
    
    with st.form("leave_form"):
        name = st.selectbox("အမည်", staff_list)
        start_date = st.date_input("စတင်မည့်ရက်")
        end_date = st.date_input("ပြီးဆုံးမည့်ရက်")
        reason = st.text_area("အကြောင်းပြချက်")
        submit = st.form_submit_button("Submit Leave Request")
        
        if submit:
            leave_data = pd.DataFrame([{
                "Name": name,
                "Start_Date": str(start_date),
                "End_Date": str(end_date),
                "Reason": reason,
                "Status": "Pending"
            }])
            
            # Google Sheet (Leave_Requests tab) သို့ သိမ်းဆည်းခြင်း
            conn.create(data=leave_data, worksheet="Leave_Requests")
            st.success("ခွင့်တိုင်ကြားမှု ပေးပို့ပြီးပါပြီ။ Admin မှ ပြန်လည် အကြောင်းပြန်ပေးပါမည်။")

elif choice == "📊 View Records":
    st.subheader("မှတ်တမ်းများ ပြန်လည်ကြည့်ရှုခြင်း")
    # Google Sheet မှ data များကို ပြန်ဖတ်ခြင်း
    attendance_df = conn.read(worksheet="Attendance")
    st.dataframe(attendance_df)