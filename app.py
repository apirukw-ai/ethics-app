import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Decision-Making Dashboard", page_icon="📊", layout="wide"
)

st.title("📊 Class Discussion Decision Dashboard")
st.subheader("Pre vs Post Discussion Voting for Each Scenario")

# ข้อมูล Scenario ทั้ง 4 แบบ
scenarios_info = {
    "Scenario A": {
        "title": "Scenario A: มีเหตุจำเป็นทั่วไป",
        "desc": "เพื่อนไม่ได้ทำงาน แต่ขอใส่ชื่อเพราะมีเหตุจำเป็นจริง ๆ",
    },
    "Scenario B": {
        "title": "Scenario B: ดูแลคนป่วยในครอบครัว",
        "desc": "เพื่อนไม่ได้ทำงาน เพราะต้องดูแลสมาชิกในครอบครัวที่ป่วย",
    },
    "Scenario C": {
        "title": "Scenario C: มีผลงานส่วนอื่นช่วยกลุ่ม",
        "desc": "เพื่อนไม่ได้ทำงาน แต่ผลงานของเขาในส่วนอื่นช่วยให้กลุ่มประสบความสำเร็จ",
    },
    "Scenario D": {
        "title": "Scenario D: เพื่อนสนิท ไม่มีเหตุจำเป็น",
        "desc": "เพื่อนไม่ได้ทำงาน และไม่มีเหตุจำเป็น แต่เป็นเพื่อนสนิทของคุณ",
    },
}

# เก็บข้อมูลโหวตจำลองของแต่ละ Scenario (Pre และ Post)
if "class_votes" not in st.session_state:
    st.session_state.class_votes = {
        key: {
            "Pre (ก่อนอภิปราย)": {"A": 15, "B": 30, "C": 25, "D": 20, "E": 5},
            "Post (หลังอภิปราย)": {"A": 10, "B": 25, "C": 35, "D": 25, "E": 0},
        }
        for key in scenarios_info.keys()
    }

options_list = [
    "A. ใส่ชื่อให้ เพราะเป็นเพื่อน",
    "B. ไม่ใส่ชื่อ เพราะไม่ได้ทำงาน",
    "C. คุยกับเพื่อนก่อนแล้วหาทางออก",
    "D. ขึ้นอยู่กับรายละเอียดของสถานการณ์",
    "E. อื่น ๆ",
]

# Sidebar สำหรับเลือกเปลี่ยน Scenario ที่กำลังดำเนินกิจกรรมในห้องเรียน
st.sidebar.markdown("### 🎛️ ควบคุมบทเรียนในห้อง")
selected_scenario = st.sidebar.radio(
    "เลือกสถานการณ์ปัจจุบัน:", list(scenarios_info.keys()), format_func=lambda x: scenarios_info[x]["title"]
)

current_s = scenarios_info[selected_scenario]

st.markdown(f"## 📌 {current_s['title']}")
st.info(f"**สถานการณ์:** {current_s['desc']}")
st.markdown("---")

# แบ่งหน้าจอซ้าย-ขวา สำหรับการโหวต และ กราฟเปรียบเทียบ Pre-Post ใน Scenario นี้
col1, col2 = st.columns([1, 1.2])

vote_data = st.session_state.class_votes[selected_scenario]

with col1:
    st.markdown("### 🗳️ บันทึกผลโหวตในห้องเรียน")

    # ฟอร์มโหวต Pre
    st.markdown("#### 1️⃣ Pre-Vote (ก่อนอภิปราย)")
    with st.form(f"pre_{selected_scenario}"):
        pre_choice = st.radio("เลือกคำตอบของคุณ (Pre):", options_list, key=f"r_pre_{selected_scenario}")
        pre_submit = st.form_submit_button("ส่งโหวต Pre-Vote")
        if pre_submit:
            vote_data["Pre (ก่อนอภิปราย)"][pre_choice[0]] += 1
            st.success("บันทึกผล Pre-Vote สำเร็จ!")

    st.markdown("---")

    # ฟอร์มโหวต Post
    st.markdown("#### 2️⃣ Post-Vote (หลังอภิปรายในห้อง)")
    with st.form(f"post_{selected_scenario}"):
        post_choice = st.radio("เลือกคำตอบของคุณ (Post):", options_list, key=f"r_post_{selected_scenario}")
        post_submit = st.form_submit_button("ส่งโหวต Post-Vote")
        if post_submit:
            vote_data["Post (หลังอภิปราย)"][post_choice[0]] += 1
            st.success("บันทึกผล Post-Vote สำเร็จ!")

with col2:
    st.markdown("### 📈 กราฟเปรียบเทียบ Pre vs Post")
    st.markdown(f"**ผลลัพธ์ของ: {current_s['title']}**")

    # สร้าง DataFrame เทียบ Pre กับ Post ใน Scenario ปัจจุบัน
    df_current = pd.DataFrame(
        {
            "Pre (ก่อนอภิปราย)": pd.Series(vote_data["Pre (ก่อนอภิปราย)"]),
            "Post (หลังอภิปราย)": pd.Series(vote_data["Post (หลังอภิปราย)"]),
        }
    )

    st.bar_chart(df_current)
    st.caption("💡 กราฟแสดงการเปลี่ยนแปลงความคิดเห็นของนักศึกษาก่อนและหลังการอภิปรายสำหรับสถานการณ์นี้โดยเฉพาะ")