from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics & Decision-Making Workshop",
    page_icon="🧭",
    layout="wide",
)

# เชื่อมต่อ Google Sheets (อ่านค่าจาก st.secrets["connections"]["gsheets"])
# หมายเหตุ: ต้องตั้งค่า secrets บน Streamlit Cloud ก่อนใช้งานจริง
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None  # กรณีรันเทสบนเครื่องแล้วยังไม่ได้ตั้งค่า secrets

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "step" not in st.session_state:
    st.session_state.step = 4

# --- Sidebar แสดงความคืบหน้า ---
st.sidebar.markdown("### 🧭 ขั้นตอนกิจกรรม (Workflow)")
steps_name = {
    4: "Page 4: Warm-up (Ethics)",
    5: "Page 5: Dilemma 1",
    6: "Page 6: Why? (Reasoning)",
    7: "Page 7: Small Group Discussion",
    8: "Page 8: Challenge",
    9: "Page 9: Dilemma 2 (Pharmacy)",
    10: "Page 10: Ethical Framework",
    11: "Page 11: Re-Vote",
    12: "Page 12: Final Reflection",
}

for s_num, s_title in steps_name.items():
    if st.session_state.step == s_num:
        st.sidebar.markdown(f"👉 **{s_title}**")
    else:
        st.sidebar.markdown(f"{s_title}")

st.sidebar.markdown("---")
col_sb1, col_sb2 = st.sidebar.columns(2)
with col_sb1:
    if st.button("⬅️ ก่อนหน้า") and st.session_state.step > 4:
        st.session_state.step -= 1
        st.rerun()
with col_sb2:
    if st.button("ถัดไป ➡️") and st.session_state.step < 12:
        st.session_state.step += 1
        st.rerun()


# ==========================================
# PAGE 4 — Warm-up: What is Ethics?
# ==========================================
if st.session_state.step == 4:
    st.title("💬 PAGE 4 — Warm-up: What is Ethics?")
    st.write(
        "### “เมื่อคุณได้ยินคำว่า Ethics คุณนึกถึงอะไรเป็นสิ่งแรก?”"
    )

    with st.form("warmup_form"):
        user_word = st.text_input(
            "พิมพ์คำตอบสั้น ๆ 1–3 คำ (เช่น หน้าศีลธรรม, ความถูกต้อง):"
        )
        submitted = st.form_submit_button("ส่งคำตอบ")

        if submitted and user_word:
            new_data = pd.DataFrame(
                [
                    {
                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Step": "Page 4 - Warmup",
                        "Data": user_word,
                    }
                ]
            )

            if conn:
                try:
                    # ดึงข้อมูลเดิมมาต่อท้ายแล้วบันทึกกลับไปที่ Google Sheets
                    existing_data = conn.read(worksheet="Responses", ttl=0)
                    updated_data = pd.concat(
                        [existing_data, new_data], ignore_index=True
                    )
                    conn.update(worksheet="Responses", data=updated_data)
                    st.success("บันทึกคำตอบลง Google Sheets เรียบร้อย!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาดในการบันทึก: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ (ยังไม่ได้เชื่อม Google Sheets)")

    st.markdown("---")
    st.markdown("### ☁️ Word Cloud (ข้อมูลจาก Google Sheets)")
    if conn:
        try:
            df = conn.read(worksheet="Responses", ttl=5)
            warmup_words = df[df["Step"] == "Page 4 - Warmup"][
                "Data"
            ].tolist()
            if warmup_words:
                st.info(" ".join([f"` {w} `" for w in warmup_words]))
            else:
                st.write("ยังไม่มีข้อมูลคำตอบ")
        except:
            st.info("`ถูกต้อง` `ศีลธรรม` `หน้าที่`")
    else:
        st.info("`ถูกต้อง` `ศีลธรรม` `หน้าที่`")
    st.write("“Our classroom's first picture of Ethics”")


# ==========================================
# PAGE 5 — Dilemma 1
# ==========================================
elif st.session_state.step == 5:
    st.title("⚖️ PAGE 5 — Dilemma 1")
    st.markdown(
        "## “ถ้าการกระทำนั้นไม่ผิดกฎหมาย แสดงว่าการกระทำนั้นถูกต้องทางจริยธรรมหรือไม่?”"
    )

    choice = st.radio(
        "เลือกคำตอบของคุณ:",
        [
            "A. ถูกต้อง (ไม่ผิดกฎหมาย = ถูกต้องทางจริยธรรม)",
            "B. ไม่ถูกต้องเสมอไป (กฎหมายกับจริยธรรมอาจต่างกัน)",
            "C. ไม่แน่ใจ / ขึ้นอยู่กับบริบท",
        ],
    )

    if st.button("ยืนยันคำตอบ"):
        st.success("บันทึกผลโหวตเรียบร้อย!")


# ==========================================
# PAGE 6 — Why?
# ==========================================
elif st.session_state.step == 6:
    st.title("🧠 PAGE 6 — Why?")
    st.write(
        "### “อะไรเป็นเหตุผลสำคัญที่สุดที่ทำให้คุณเลือกคำตอบนั้น?”"
    )

    with st.form("reason_form"):
        reason_text = st.text_area("อธิบายเหตุผลของคุณสั้น ๆ:")
        sub_reason = st.form_submit_button("ส่งเหตุผล")

        if sub_reason and reason_text:
            new_data = pd.DataFrame(
                [
                    {
                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Step": "Page 6 - Why",
                        "Data": reason_text,
                    }
                ]
            )
            if conn:
                try:
                    existing_data = conn.read(worksheet="Responses", ttl=0)
                    updated_data = pd.concat(
                        [existing_data, new_data], ignore_index=True
                    )
                    conn.update(worksheet="Responses", data=updated_data)
                    st.success("ส่งเหตุผลและบันทึกลง Google Sheets สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")


# ==========================================
# PAGE 7 — Small Group Discussion
# ==========================================
elif st.session_state.step == 7:
    st.title("👥 PAGE 7 — Small Group Discussion")
    st.warning(
        "**โจทย์อภิปราย:** “การไม่ผิดกฎหมายเพียงอย่างเดียวเพียงพอที่จะบอกว่าการกระทำนั้นถูกต้องทางจริยธรรมหรือไม่”"
    )


# ==========================================
# PAGE 8 — Challenge
# ==========================================
elif st.session_state.step == 8:
    st.title("⚔️ PAGE 8 — Challenge")
    st.info(
        "“ถ้ามีคนแย้งกับความเห็นของกลุ่มคุณว่า\n*‘ถ้าไม่ผิดกฎหมาย ก็ไม่มีเหตุผลที่จะบอกว่าผิด’*\nคุณจะตอบอย่างไร?”"
    )
    st.text_area("พิมพ์แนวทางการโต้แย้งของกลุ่ม:")


# ==========================================
# PAGE 9 — Dilemma 2: Pharmacy Context
# ==========================================
elif st.session_state.step == 9:
    st.title("💊 PAGE 9 — Dilemma 2: Pharmacy Context")
    st.error(
        "**สถานการณ์:** คุณเป็นเภสัชกรและพบว่าเพื่อนร่วมงานมีพฤติกรรมที่ไม่เหมาะสม แต่ในเหตุการณ์นั้นยังไม่มีผู้ป่วยได้รับอันตราย คุณจะทำอย่างไร?"
    )
    st.radio(
        "การตัดสินใจของคุณ:",
        [
            "1. ตักเตือนเพื่อนร่วมงานเป็นการส่วนตัวทันที",
            "2. รายงานผู้มีอำนาจหรือหัวหน้างานทันที",
            "3. รอดูสถานการณ์ไปก่อนเพราะยังไม่มีใครเสียหาย",
            "4. เพิกเฉยเพราะไม่ใช่เรื่องของเรา",
        ],
    )


# ==========================================
# PAGE 10 — Ethical Reasoning
# ==========================================
elif st.session_state.step == 10:
    st.title("📋 PAGE 10 — Ethical Reasoning Framework")
    st.text_area("บันทึกผลการวิเคราะห์ของกลุ่ม:")


# ==========================================
# PAGE 11 — Re-Vote
# ==========================================
elif st.session_state.step == 11:
    st.title("🔄 PAGE 11 — Re-Vote")
    st.info(
        "“หลังจากฟังเหตุผลของเพื่อนและอภิปรายในกลุ่มแล้ว คุณยังเลือกคำตอบเดิมหรือไม่?”"
    )
    st.radio("การตัดสินใจใหม่ (Re-Vote):", ["เปลี่ยนใจ", "ยังคงเลือกคำตอบเดิม"])


# ==========================================
# PAGE 12 — Final Reflection
# ==========================================
elif st.session_state.step == 12:
    st.title("🎯 PAGE 12 — Final Reflection")

    with st.form("reflection_form"):
        q1 = st.text_area(
            "1. หลังจากกิจกรรมวันนี้ คุณคิดว่า ‘จริยธรรม’ แตกต่างจาก ‘กฎหมาย’ หรือ ‘ความรู้สึกส่วนตัว’ อย่างไร?"
        )
        q2 = st.text_area(
            "2. สิ่งหนึ่งที่คุณจะนำไปใช้เมื่อเผชิญสถานการณ์ทางจริยธรรมในอนาคตคืออะไร?"
        )
        sub_ref = st.form_submit_button("ส่งแบบสะท้อนความคิด")

        if sub_ref:
            combined_text = f"Q1: {q1} | Q2: {q2}"
            new_data = pd.DataFrame(
                [
                    {
                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Step": "Page 12 - Reflection",
                        "Data": combined_text,
                    }
                ]
            )
            if conn:
                try:
                    existing_data = conn.read(worksheet="Responses", ttl=0)
                    updated_data = pd.concat(
                        [existing_data, new_data], ignore_index=True
                    )
                    conn.update(worksheet="Responses", data=updated_data)
                    st.success("บันทึก Reflection ลง Google Sheets สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกสำเร็จเรียบร้อย!")

# --- ปุ่มควบคุมด้านล่างหน้าจอ ---
st.markdown("---")
c_bot1, c_bot2 = st.columns([1, 1])
with c_bot1:
    if st.session_state.step > 4:
        if st.button("◀️ ย้อนกลับขั้นตอนก่อนหน้า"):
            st.session_state.step -= 1
            st.rerun()
with c_bot2:
    if st.session_state.step < 12:
        if st.button("ไปขั้นตอนถัดไป ➡️", type="primary"):
            st.session_state.step += 1
            st.rerun()