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

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "step" not in st.session_state:
    st.session_state.step = 4

# --- Sidebar เมนูด้านซ้ายแบบคลิกเลือกได้ ---
st.sidebar.markdown("### 🧭 LAB 1: ขั้นตอนกิจกรรม (Workflow)")

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

current_index = list(steps_name.keys()).index(st.session_state.step)

selected_step_name = st.sidebar.radio(
    "เลือกหน้ากิจกรรม:",
    list(steps_name.values()),
    index=current_index,
    key="menu_selection",
)

for s_num, s_title in steps_name.items():
    if s_title == selected_step_name:
        st.session_state.step = s_num

st.sidebar.markdown("---")
st.sidebar.info("💡 นิสิตสามารถคลิกเลือกหัวข้อกิจกรรมจากเมนูด้านบนได้เลยครับ")


# ==========================================
# PAGE 4 — Warm-up: What is Ethics?
# ==========================================
if st.session_state.step == 4:
    st.title("💬 PAGE 4 — Warm-up: What is Ethics?")
    st.write("### “เมื่อคุณได้ยินคำว่า Ethics คุณนึกถึงอะไรเป็นสิ่งแรก?”")

    with st.form("warmup_form"):
        student_id = st.text_input("รหัสนิสิต:")
        user_word = st.text_input(
            "พิมพ์คำตอบสั้น ๆ 1–3 คำ (เช่น หน้าศีลธรรม, ความถูกต้อง):"
        )
        submitted = st.form_submit_button("ส่งคำตอบ")

        if submitted and user_word and student_id:
            new_data = pd.DataFrame(
                [
                    {
                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Step": "Page 4 - Warmup",
                        "Data": f"[{student_id}] {user_word}",
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
                    st.success("บันทึกคำตอบลง Google Sheets เรียบร้อย!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาดในการบันทึก: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif submitted:
            st.warning("กรุณากรอกรหัสนิสิตและคำตอบให้ครบถ้วนครับ")

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
        "## “ถ้าการกระทำนั้นไม่ผิดกฎหมาย แสดงว่าการกระทำนั้นถูกต้องทางจริยธรรมหรือไม่”"
    )

    with st.form("dilemma1_form"):
        student_id = st.text_input("รหัสนิสิต:")
        choice = st.radio(
            "เลือกคำตอบของคุณ:",
            [
                "A. ถูกต้อง (ไม่ผิดกฎหมาย = ถูกต้องทางจริยธรรม)",
                "B. ไม่ถูกต้องเสมอไป (กฎหมายกับจริยธรรมอาจต่างกัน)",
                "C. ไม่แน่ใจ / ขึ้นอยู่กับบริบท",
            ],
        )
        sub_d1 = st.form_submit_button("ยืนยันคำตอบ")

        if sub_d1 and student_id:
            new_data = pd.DataFrame(
                [
                    {
                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Step": "Page 5 - Dilemma 1",
                        "Data": f"[{student_id}] {choice}",
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
                    st.success("บันทึกผลโหวตเรียบร้อย!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_d1:
            st.warning("กรุณากรอกรหัสนิสิตก่อนยืนยันคำตอบครับ")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผลการโหวต Dilemma 1")
    if conn:
        try:
            df = conn.read(worksheet="Responses", ttl=5)
            d1_data = df[df["Step"] == "Page 5 - Dilemma 1"]
            if not d1_data.empty:
                vote_counts = d1_data["Data"].value_counts()
                st.bar_chart(vote_counts)
            else:
                st.info("ยังไม่มีข้อมูลผลโหวต")
        except:
            st.info("กำลังรอข้อมูล...")


# ==========================================
# PAGE 6 — Why?
# ==========================================
elif st.session_state.step == 6:
    st.title("🧠 PAGE 6 — Why?")
    st.write("### “อะไรเป็นเหตุผลสำคัญที่สุดที่ทำให้คุณเลือกคำตอบนั้น?”")

    with st.form("reason_form"):
        student_id = st.text_input("รหัสนิสิต:")
        reason_text = st.text_area("อธิบายเหตุผลของคุณสั้น ๆ:")
        sub_reason = st.form_submit_button("ส่งเหตุผล")

        if sub_reason and reason_text and student_id:
            new_data = pd.DataFrame(
                [
                    {
                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Step": "Page 6 - Why",
                        "Data": f"[{student_id}] {reason_text}",
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
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_reason:
            st.warning("กรุณากรอกรหัสนิสิตและเหตุผลให้ครบถ้วนครับ")

    st.markdown("---")
    st.subheader("📋 คำตอบทั้งหมด (Page 6)")
    if conn:
        try:
            df = conn.read(worksheet="Responses", ttl=5)
            p6_data = df[df["Step"] == "Page 6 - Why"]
            if not p6_data.empty:
                st.dataframe(p6_data[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูลคำตอบ")
        except:
            st.info("ไม่สามารถโหลดข้อมูลได้")


# ==========================================
# PAGE 7 — Small Group Discussion
# ==========================================
elif st.session_state.step == 7:
    st.title("👥 PAGE 7 — Small Group Discussion")
    st.warning(
        "**โจทย์อภิปราย:** “การไม่ผิดกฎหมายเพียงอย่างเดียวเพียงพอที่จะบอกว่าการกระทำนั้นถูกต้องทางจริยธรรมหรือไม่”"
    )

    with st.form("group_discussion_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        discussion_summary = st.text_area("สรุปผลการอภิปรายของกลุ่มคุณ:")
        sub_disc = st.form_submit_button("ส่งสรุปผลการอภิปราย")

        if sub_disc and discussion_summary and group_name:
            new_data = pd.DataFrame(
                [
                    {
                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Step": "Page 7 - Group Discussion",
                        "Data": f"[{group_name}] {discussion_summary}",
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
                    st.success("บันทึกสรุปผลการอภิปรายลง Google Sheets สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_disc:
            st.warning("กรุณากรอกชื่อกลุ่มและสรุปผลการอภิปรายครับ")

    st.markdown("---")
    st.subheader("📋 สรุปผลการอภิปรายของแต่ละกลุ่ม (Page 7)")
    if conn:
        try:
            df = conn.read(worksheet="Responses", ttl=5)
            p7_data = df[df["Step"] == "Page 7 - Group Discussion"]
            if not p7_data.empty:
                st.dataframe(p7_data[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูลสรุปของกลุ่ม")
        except:
            st.info("ไม่สามารถโหลดข้อมูลได้")


# ==========================================
# PAGE 8 — Challenge
# ==========================================
elif st.session_state.step == 8:
    st.title("⚔️ PAGE 8 — Challenge")
    st.info(
        "“ถ้ามีคนแย้งกับความเห็นของกลุ่มคุณว่า\n*‘ถ้าไม่ผิดกฎหมาย ก็ไม่มีเหตุผลที่จะบอกว่าผิด’*\nคุณจะตอบอย่างไร?”"
    )

    with st.form("challenge_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        challenge_text = st.text_area("พิมพ์แนวทางการโต้แย้งของกลุ่ม:")
        sub_challenge = st.form_submit_button("ส่งคำตอบท้าทาย")

        if sub_challenge and challenge_text and group_name:
            new_data = pd.DataFrame(
                [
                    {
                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Step": "Page 8 - Challenge",
                        "Data": f"[{group_name}] {challenge_text}",
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
                    st.success("บันทึกคำตอบ Challenge ลง Google Sheets สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_challenge:
            st.warning("กรุณากรอกชื่อกลุ่มและแนวทางการโต้แย้งครับ")

    st.markdown("---")
    st.subheader("📋 แนวทางการโต้แย้งของแต่ละกลุ่ม (Page 8)")
    if conn:
        try:
            df = conn.read(worksheet="Responses", ttl=5)
            p8_data = df[df["Step"] == "Page 8 - Challenge"]
            if not p8_data.empty:
                st.dataframe(p8_data[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล Challenge")
        except:
            st.info("ไม่สามารถโหลดข้อมูลได้")


# ==========================================
# PAGE 9 — Dilemma 2: Pharmacy Context
# ==========================================
elif st.session_state.step == 9:
    st.title("💊 PAGE 9 — Dilemma 2: Pharmacy Context")
    st.error(
        "**สถานการณ์:** คุณเป็นเภสัชกรและพบว่าเพื่อนร่วมงานมีพฤติกรรมที่ไม่เหมาะสม แต่ในเหตุการณ์นั้นยังไม่มีผู้ป่วยได้รับอันตราย คุณจะทำอย่างไร?"
    )

    with st.form("dilemma2_form"):
        student_id = st.text_input("รหัสนิสิต:")
        choice_d2 = st.radio(
            "การตัดสินใจของคุณ:",
            [
                "1. ตักเตือนเพื่อนร่วมงานเป็นการส่วนตัวทันที",
                "2. รายงานผู้มีอำนาจหรือหัวหน้างานทันที",
                "3. รอดูสถานการณ์ไปก่อนเพราะยังไม่มีใครเสียหาย",
                "4. เพิกเฉยเพราะไม่ใช่เรื่องของเรา",
            ],
        )
        sub_d2 = st.form_submit_button("ยืนยันคำตอบ Dilemma 2")

        if sub_d2 and student_id:
            new_data = pd.DataFrame(
                [
                    {
                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Step": "Page 9 - Dilemma 2",
                        "Data": f"[{student_id}] {choice_d2}",
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
                    st.success("บันทึกผลโหวต Dilemma 2 เรียบร้อย!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_d2:
            st.warning("กรุณากรอกรหัสนิสิตก่อนยืนยันคำตอบครับ")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผลการโหวต Dilemma 2")
    if conn:
        try:
            df = conn.read(worksheet="Responses", ttl=5)
            d2_data = df[df["Step"] == "Page 9 - Dilemma 2"]
            if not d2_data.empty:
                vote_counts_d2 = d2_data["Data"].value_counts()
                st.bar_chart(vote_counts_d2)
            else:
                st.info("ยังไม่มีข้อมูลผลโหวต Dilemma 2")
        except:
            st.info("กำลังรอข้อมูล...")


# ==========================================
# PAGE 10 — Ethical Reasoning
# ==========================================
elif st.session_state.step == 10:
    st.title("📋 PAGE 10 — Ethical Reasoning Framework")
    st.write("### “วิเคราะห์สถานการณ์ตามกรอบการตัดสินใจทางจริยธรรม”")

    with st.form("framework_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        framework_text = st.text_area(
            "บันทึกผลการวิเคราะห์และแนวทางการตัดสินใจของกลุ่ม:"
        )
        sub_framework = st.form_submit_button("ส่งผลการวิเคราะห์")

        if sub_framework and framework_text and group_name:
            new_data = pd.DataFrame(
                [
                    {
                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Step": "Page 10 - Ethical Framework",
                        "Data": f"[{group_name}] {framework_text}",
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
                    st.success("บันทึกผลการวิเคราะห์ลง Google Sheets สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_framework:
            st.warning("กรุณากรอกชื่อกลุ่มและผลการวิเคราะห์ครับ")

    st.markdown("---")
    st.subheader("📋 ผลการวิเคราะห์ของแต่ละกลุ่ม (Page 10)")
    if conn:
        try:
            df = conn.read(worksheet="Responses", ttl=5)
            p10_data = df[df["Step"] == "Page 10 - Ethical Framework"]
            if not p10_data.empty:
                st.dataframe(p10_data[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูลการวิเคราะห์")
        except:
            st.info("ไม่สามารถโหลดข้อมูลได้")


# ==========================================
# PAGE 11 — Re-Vote
# ==========================================
elif st.session_state.step == 11:
    st.title("🔄 PAGE 11 — Re-Vote")
    st.info(
        "“หลังจากฟังเหตุผลของเพื่อนและอภิปรายในกลุ่มแล้ว คุณยังเลือกคำตอบเดิมหรือไม่?”"
    )

    with st.form("revote_form"):
        student_id = st.text_input("รหัสนิสิต:")
        revote_choice = st.radio(
            "การตัดสินใจใหม่ (Re-Vote):", ["เปลี่ยนใจ", "ยังคงเลือกคำตอบเดิม"]
        )
        sub_rv = st.form_submit_button("ยืนยัน Re-Vote")

        if sub_rv and student_id:
            new_data = pd.DataFrame(
                [
                    {
                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Step": "Page 11 - Re-Vote",
                        "Data": f"[{student_id}] {revote_choice}",
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
                    st.success("บันทึก Re-Vote เรียบร้อย!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_rv:
            st.warning("กรุณากรอกรหัสนิสิตก่อนยืนยัน Re-Vote ครับ")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผล Re-Vote")
    if conn:
        try:
            df = conn.read(worksheet="Responses", ttl=5)
            p11_data = df[df["Step"] == "Page 11 - Re-Vote"]
            if not p11_data.empty:
                vote_counts_rv = p11_data["Data"].value_counts()
                st.bar_chart(vote_counts_rv)
            else:
                st.info("ยังไม่มีข้อมูล Re-Vote")
        except:
            st.info("กำลังรอข้อมูล...")


# ==========================================
# PAGE 12 — Final Reflection
# ==========================================
elif st.session_state.step == 12:
    st.title("🎯 PAGE 12 — Final Reflection")

    with st.form("reflection_form"):
        student_id = st.text_input("รหัสนิสิต:")
        q1 = st.text_area(
            "1. หลังจากกิจกรรมวันนี้ คุณคิดว่า ‘จริยธรรม’ แตกต่างจาก ‘กฎหมาย’ หรือ ‘ความรู้สึกส่วนตัว’ อย่างไร?"
        )
        q2 = st.text_area(
            "2. สิ่งหนึ่งที่คุณจะนำไปใช้เมื่อเผชิญสถานการณ์ทางจริยธรรมในอนาคตคืออะไร?"
        )
        sub_ref = st.form_submit_button("ส่งแบบสะท้อนความคิด")

        if sub_ref and q1 and q2 and student_id:
            combined_text = f"Q1: {q1} | Q2: {q2}"
            new_data = pd.DataFrame(
                [
                    {
                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Step": "Page 12 - Reflection",
                        "Data": f"[{student_id}] {combined_text}",
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
        elif sub_ref:
            st.warning("กรุณากรอกรหัสนิสิตและตอบคำถามให้ครบถ้วนครับ")
