import pandas as pd
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics & Decision-Making Workshop",
    page_icon="🧭",
    layout="wide",
)

# --- 1. กำหนดค่าเริ่มต้นใน Session State ---
if "step" not in st.session_state:
    st.session_state.step = 4  # เริ่มที่ Page 4 ตามโจทย์ (ปรับเปลี่ยนได้)

if "word_cloud_data" not in st.session_state:
    st.session_state.word_cloud_data = [
        "ถูกต้อง",
        "ศีลธรรม",
        "หน้าที่",
        "ความถูกต้อง",
        "กฎหมาย",
        "คุณธรรม",
    ]

if "reasons" not in st.session_state:
    st.session_state.reasons = []

if "reflections" not in st.session_state:
    st.session_state.reflections = []


# ฟังก์ชันเปลี่ยนหน้า
def next_step():
    st.session_state.step += 1


def prev_step():
    st.session_state.step -= 1


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
# ปุ่มควบคุมข้ามหน้าด่วนสำหรับอาจารย์
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
            st.session_state.word_cloud_data.append(user_word)
            st.success("บันทึกคำตอบของคุณแล้ว!")

    st.markdown("---")
    st.markdown("### ☁️ Word Cloud (จำลองการแสดงผล)")
    # แสดงคำแบบแท็กคลาวด์ง่าย ๆ ด้วยการวนลูป
    st.info(" ".join([f"` {w} `" for w in st.session_state.word_cloud_data]))
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
    st.caption(
        "เป้าหมายของหน้านี้คือให้นักศึกษาเห็นว่า คนสองคนอาจเลือกคำตอบเดียวกัน แต่ใช้เหตุผลคนละแบบ"
    )

    with st.form("reason_form"):
        reason_text = st.text_area("อธิบายเหตุผลของคุณสั้น ๆ:")
        sub_reason = st.form_submit_button("ส่งเหตุผล")
        if sub_reason and reason_text:
            st.session_state.reasons.append(reason_text)
            st.success("ส่งเหตุผลสำเร็จ!")

    if st.session_state.reasons:
        st.markdown("### 📢 เหตุผลจากเพื่อนร่วมชั้น (บางส่วน):")
        for r in st.session_state.reasons[-3:]:
            st.markdown(f"- *\"{r}\"*")


# ==========================================
# PAGE 7 — Small Group Discussion
# ==========================================
elif st.session_state.step == 7:
    st.title("👥 PAGE 7 — Small Group Discussion")
    st.write("แบ่งนักศึกษาเป็นกลุ่มย่อย และร่วมกันอภิปรายโจทย์นี้:")
    st.warning(
        "**โจทย์อภิปราย:** “การไม่ผิดกฎหมายเพียงอย่างเดียวเพียงพอที่จะบอกว่าการกระทำนั้นถูกต้องทางจริยธรรมหรือไม่”"
    )
    st.write(
        "ให้แต่ละกลุ่มร่วมกันหาข้อสรุปและเตรียมตัวสะท้อนความคิดเห็นต่อหน้าห้อง"
    )


# ==========================================
# PAGE 8 — Challenge
# ==========================================
elif st.session_state.step == 8:
    st.title("⚔️ PAGE 8 — Challenge")
    st.write("### สถานการณ์ท้าทายความคิดเห็นกลุ่ม:")
    st.info(
        "“ถ้ามีคนแย้งกับความเห็นของกลุ่มคุณว่า\n*‘ถ้าไม่ผิดกฎหมาย ก็ไม่มีเหตุผลที่จะบอกว่าผิด’*\nคุณจะตอบอย่างไร?”"
    )

    st.text_area("พิมพ์แนวทางการโต้แย้งหรือคำตอบของกลุ่มคุณ:")
    if st.button("บันทึกคำตอบกลุ่ม"):
        st.success("บันทึกเรียบร้อย!")


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
    if st.button("ส่งคำตอบสถานการณ์นี้"):
        st.success("บันทึกคำตอบแล้ว!")


# ==========================================
# PAGE 10 — Ethical Reasoning
# ==========================================
elif st.session_state.step == 10:
    st.title("📋 PAGE 10 — Ethical Reasoning Framework")
    st.write(
        "ให้แต่ละกลุ่มวิเคราะห์สถานการณ์ Pharmacy Context โดยใช้กรอบการคิดเชิงจริยธรรมด้านล่าง:"
    )

    st.markdown(
        """
    - **1. ระบุประเด็นปัญหาจริยธรรม (Ethical Issue):** อะไรคือแก่นของปัญหา?
    - **2. ผู้มีส่วนได้ส่วนเสีย (Stakeholders):** ใครบ้างที่จะได้รับผลกระทบ?
    - **3. ทางเลือกที่เป็นไปได้ (Alternative Actions):** มีแนวทางปฏิบัติอะไรบ้าง?
    - **4. ผลกระทบและหลักการ (Consequences & Principles):** ใช้หลักจริยธรรมใดมาตัดสิน?
    """
    )
    st.text_area("บันทึกผลการวิเคราะห์ของกลุ่ม:")


# ==========================================
# PAGE 11 — Re-Vote
# ==========================================
elif st.session_state.step == 11:
    st.title("🔄 PAGE 11 — Re-Vote")
    st.write("นำคำถามจาก Dilemma 2 กลับมาอีกครั้ง:")
    st.info(
        "“หลังจากฟังเหตุผลของเพื่อนและอภิปรายในกลุ่มแล้ว คุณยังเลือกคำตอบเดิมหรือไม่?”"
    )

    st.radio(
        "การตัดสินใจใหม่ของคุณ (Re-Vote):",
        [
            "เปลี่ยนใจ (จากเดิม)",
            "ยังคงเลือกคำตอบเดิม",
        ],
    )
    if st.button("ยืนยันผล Re-Vote"):
        st.success("บันทึกผลการโหวตรอบสองเรียบร้อย!")


# ==========================================
# PAGE 12 — Final Reflection
# ==========================================
elif st.session_state.step == 12:
    st.title("🎯 PAGE 12 — Final Reflection")
    st.write("### สรุปการเรียนรู้ท้ายกิจกรรม")

    with st.form("reflection_form"):
        q1 = st.text_area(
            "1. หลังจากกิจกรรมวันนี้ คุณคิดว่า ‘จริยธรรม’ แตกต่างจาก ‘กฎหมาย’ หรือ ‘ความรู้สึกส่วนตัว’ อย่างไร?"
        )
        q2 = st.text_area(
            "2. สิ่งหนึ่งที่คุณจะนำไปใช้เมื่อเผชิญสถานการณ์ทางจริยธรรมในอนาคตคืออะไร?"
        )
        sub_ref = st.form_submit_button("ส่งแบบสะท้อนความคิด")
        if sub_ref:
            st.success(
                "ขอบคุณสำหรับการเข้าร่วมกิจกรรม! บันทึกข้อมูลเรียบร้อยแล้วครับ 🎉"
            )

# --- ปุ่มควบคุมด้านล่างหน้าจอสำหรับเลื่อนสเตป ---
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