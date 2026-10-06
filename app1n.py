from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 1: Foundations of Ethical Thinking",
    page_icon="🧭",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab1_page" not in st.session_state:
    st.session_state.lab1_page = 1

# --- Sidebar เมนูด้านซ้าย (14 หน้า) ---
st.sidebar.markdown("### 🧭 LAB 1 Workflow")

pages_name = {
    1: "PAGE 1: Welcome",
    2: "PAGE 2: Course Orientation",
    3: "PAGE 3: Ethics คืออะไร? (Word Cloud)",
    4: "PAGE 4: Dilemma 1 (Law vs Ethics)",
    5: "PAGE 5: See The Room",
    6: "PAGE 6: Group Discussion 1",
    7: "PAGE 7: Dilemma 2 (งานกลุ่มเพื่อน)",
    8: "PAGE 8: Why? (เหตุผลเบื้องหลัง)",
    9: "PAGE 9: Pharmacy Dilemma",
    10: "PAGE 10: Group Ethical Reasoning",
    11: "PAGE 11: Challenge (เพิ่มข้อมูลใหม่)",
    12: "PAGE 12: Re-Vote (Before → After)",
    13: "PAGE 13: Build the Framework",
    14: "PAGE 14: Exit Reflection",
}

current_index = list(pages_name.keys()).index(st.session_state.lab1_page)

selected_page_name = st.sidebar.radio(
    "เลือกหน้า LAB 1:",
    list(pages_name.values()),
    index=current_index,
    key="lab1_menu_selection",
)

for p_num, p_title in pages_name.items():
    if p_title == selected_page_name:
        st.session_state.lab1_page = p_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อด้านบนเพื่อเปลี่ยนหน้ากิจกรรม")


# ==========================================
# PAGE 1 — Welcome
# ==========================================
if st.session_state.lab1_page == 1:
    st.title("🧭 LAB 1")
    st.subheader("พื้นฐานการคิดเชิงจริยธรรม (Foundations of Ethical Thinking)")
    st.markdown("### เราตัดสินว่า “ถูกต้องทางจริยธรรม” จากอะไร?")
    st.markdown("---")
    st.info(
        """
        ### 💡 แนวคิดสำคัญของวันนี้
        วันนี้เราไม่ได้มาเรียนว่า **“คำตอบที่ถูกคืออะไร”**  
        แต่เราจะเรียนว่า...  
        **“เรามีเหตุผลอะไรที่ทำให้เลือกคำตอบนั้น?”**
        """
    )


# ==========================================
# PAGE 2 — Course Orientation
# ==========================================
elif st.session_state.lab1_page == 2:
    st.title("🗺️ PAGE 2 — Course Orientation")
    st.markdown("ใช้เวลาเพียง 8 นาทีทำความเข้าใจร่วมกัน")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔄 เราจะเรียนอย่างไร?")
        st.success("**THINK → VOTE → DISCUSS → CHALLENGE → RE-VOTE → REFLECT**")

        st.markdown("### 🎯 สิ่งที่คาดหวัง")
        st.markdown(
            """
            - แสดงความคิดเห็น
            - ฟังความคิดเห็นที่แตกต่าง
            - อธิบายเหตุผล
            - เปลี่ยนความคิดเห็นได้เมื่อมีเหตุผลหรือข้อมูลใหม่
            """
        )

    with col2:
        st.markdown("### 📜 กติกาการเรียนรู้")
        st.warning(
            """
            - เปลี่ยนคำตอบได้ **ไม่ใช่** เปลี่ยนเพราะเพื่อนส่วนใหญ่เลือก
            - ไม่จำเป็นต้องเห็นด้วยกับเพื่อน แต่ต้องอธิบายเหตุผลได้
            """
        )


# ==========================================
# PAGE 3 — QUESTION: “Ethics คืออะไร?”
# ==========================================
elif st.session_state.lab1_page == 3:
    st.title("💭 PAGE 3 — Question: “Ethics คืออะไร?”")
    st.markdown("### เมื่อได้ยินคำว่า “จริยธรรม” คุณนึกถึงอะไรเป็นอันดับแรก?")
    st.markdown("💡 กรุณาพิมพ์คำสั้น ๆ 1–3 คำ (เช่น ความดี, ถูก/ผิด, ศีลธรรม, กฎหมาย, ความรับผิดชอบ ฯลฯ)")

    with st.form("lab1_p3_form"):
        student_id = st.text_input("รหัสนิสิต:")
        word_input = st.text_input("คำที่นึกถึง (1-3 คำ):")
        sub_p3 = st.form_submit_button("ส่งคำตอบ")

        if sub_p3 and student_id and word_input:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab1 - Page3 Ethics Word",
                "Data": f"[{student_id}] Word: {word_input}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab1_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab1_Responses", data=updated)
                    st.success("บันทึกคำตอบสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p3:
            st.warning("กรุณากรอกรหัสนิสิตและคำตอบ")

    st.markdown("---")
    st.subheader("☁️ รายการคำตอบทั้งหมดในห้อง (สรุปแบบความถี่)")
    if conn:
        try:
            df = conn.read(worksheet="Lab1_Responses", ttl=5)
            p3_df = df[df["Step"] == "Lab1_Responses"] if not df.empty else pd.DataFrame()
            # กรองเฉพาะ Step ที่ถูกต้อง
            p3_df = df[df["Step"] == "Lab1 - Page3 Ethics Word"]
            if not p3_df.empty:
                words = p3_df["Data"].apply(lambda x: x.split("Word: ")[1].strip() if "Word: " in x else x)
                word_counts = words.value_counts().reset_index()
                word_counts.columns = ["คำตอบ", "ความถี่"]
                st.dataframe(word_counts, use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูลคำตอบในระบบ")
        except:
            pass
    st.info("📌 **คำถามชวนคิดสำหรับอาจารย์:** จากคำตอบที่เห็น มีอะไรที่น่าสนใจบ้าง?")


# ==========================================
# PAGE 4 — DILEMMA 1: LAW ≠ ETHICS
# ==========================================
elif st.session_state.lab1_page == 4:
    st.title("⚖️ PAGE 4 — Dilemma 1: Law ≠ Ethics")
    st.markdown("### (Anonymous Vote)")
    st.info(
        "**สถานการณ์:** การกระทำหนึ่งไม่ผิดกฎหมาย แต่คุณคิดว่าไม่ถูกต้องทางจริยธรรม คุณคิดว่าเป็นไปได้หรือไม่?"
    )

    with st.form("lab1_p4_form"):
        vote_choice = st.radio(
            "เลือกตัวเลือกของคุณ (ไม่ระบุตัวตน):",
            [
                "A. เป็นไปไม่ได้ (ถ้าไม่ผิดกฎหมาย ก็ไม่ควรถือว่าผิดจริยธรรม)",
                "B. เป็นไปได้ (กฎหมายกับจริยธรรมเป็นคนละเรื่องกัน)",
                "C. ขึ้นอยู่กับสถานการณ์",
                "D. ยังไม่แน่ใจ"
            ]
        )
        sub_p4 = st.form_submit_button("ส่งเสียงโหวต (Anonymous)")

        if sub_p4:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab1 - Page4 Dilemma1 Vote",
                "Data": f"[Anonymous] Vote: {vote_choice[0]}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab1_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab1_Responses", data=updated)
                    st.success("บันทึกเสียงโหวตแบบไม่ระบุตัวตนสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")


# ==========================================
# PAGE 5 — SEE THE ROOM
# ==========================================
elif st.session_state.lab1_page == 5:
    st.title("📊 PAGE 5 — See The Room")
    st.markdown("### ผลโหวตภาพรวมของห้อง (ไม่แสดงชื่อ)")

    if conn:
        try:
            df = conn.read(worksheet="Lab1_Responses", ttl=5)
            p4_df = df[df["Step"] == "Lab1 - Page4 Dilemma1 Vote"]
            if not p4_df.empty:
                votes = p4_df["Data"].apply(lambda x: x.split("Vote: ")[1].strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
            else:
                st.info("ยังไม่มีข้อมูลการโหวตในระบบ")
        except:
            pass

    st.markdown("---")
    st.warning("🤔 **คำถามชวนคิด:** ทำไมคนในห้องจึงคิดต่างกัน? (ให้เวลาคิด 1 นาที ก่อนอภิปรายร่วมกัน)")


# ==========================================
# PAGE 6 — GROUP DISCUSSION 1
# ==========================================
elif st.session_state.lab1_page == 6:
    st.title("💬 PAGE 6 — Group Discussion 1")
    st.markdown("### “อะไรทำให้การกระทำหนึ่ง ‘ถูกต้อง’ หรือ ‘ไม่ถูกต้อง’?”")

    reasons_list = [
        "กฎหมาย", "สิทธิของผู้อื่น", "ผลกระทบ", "ความรับผิดชอบ",
        "ความซื่อสัตย์", "ความเป็นธรรม", "เจตนา", "คุณค่าหรือความเชื่อ",
        "กฎของวิชาชีพ", "อื่น ๆ"
    ]

    with st.form("lab1_p6_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        st.markdown("เลือกเหตุผลที่สำคัญที่สุด **3 ข้อ**:")
        selected_reasons = []
        for r in reasons_list:
            if st.checkbox(r, key=f"r_{r}"):
                selected_reasons.append(r)
                
        conflict_ans = st.text_area("“ถ้าเหตุผล 2 ข้อขัดแย้งกัน คุณจะให้น้ำหนักกับอะไร เพราะเหตุใด?”")
        
        sub_p6 = st.form_submit_button("ส่งผล Group Discussion 1")

        if sub_p6 and group_name:
            if len(selected_reasons) == 3:
                joined_r = ", ".join(selected_reasons)
                combined_d1 = f"Reasons: {joined_r} | Conflict: {conflict_ans}"
                new_data = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Step": "Lab1 - Page6 Group Disc1",
                    "Data": f"[{group_name}] {combined_d1}"
                }])
                if conn:
                    try:
                        existing = conn.read(worksheet="Lab1_Responses", ttl=0)
                        updated = pd.concat([existing, new_data], ignore_index=True)
                        conn.update(worksheet="Lab1_Responses", data=updated)
                        st.success("บันทึกสำเร็จ!")
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
                else:
                    st.success("บันทึกจำลองสำเร็จ!")
            else:
                st.warning("กรุณาเลือกเหตุผลให้ครบถ้วนพอดี 3 ข้อ")
        elif sub_p6:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Discussion ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab1_Responses", ttl=5)
            p6_df = df[df["Step"] == "Lab1 - Page6 Group Disc1"]
            if not p6_df.empty:
                st.dataframe(p6_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# PAGE 7 — DILEMMA 2: “ทำเพื่อประโยชน์ของตัวเอง”
# ==========================================
elif st.session_state.lab1_page == 7:
    st.title("🧑‍🤝‍🧑 PAGE 7 — Dilemma 2: “ทำเพื่อประโยชน์ของตัวเอง”")
    st.info(
        """
        **สถานการณ์:** คุณทำงานกลุ่มกับเพื่อน 5 คน เพื่อนคนหนึ่งแทบไม่ได้ช่วยงานกลุ่ม แต่ก่อนส่งงานเขาขอให้ใส่ชื่อเขาด้วย เพราะถ้าไม่มีชื่อ เขาอาจมีปัญหากับผลการเรียน คุณเป็นคนที่มีสิทธิ์ตัดสินใจว่าจะใส่ชื่อเขาหรือไม่
        """
    )
    st.markdown("### คุณจะทำอย่างไร?")

    with st.form("lab1_p7_form"):
        student_id = st.text_input("รหัสนิสิต:")
        d2_choice = st.radio(
            "เลือกการตัดสินใจของคุณ:",
            [
                "A. ใส่ชื่อ",
                "B. ไม่ใส่ชื่อ",
                "C. ใส่ชื่อ แต่บอกให้เขารับผิดชอบบางส่วนก่อน",
                "D. หาทางอื่น"
            ]
        )
        sub_p7 = st.form_submit_button("ส่งคำตอบ Dilemma 2")

        if sub_p7 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab1 - Page7 Dilemma2 Vote",
                "Data": f"[{student_id}] Choice: {d2_choice[0]}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab1_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab1_Responses", data=updated)
                    st.success("บันทึกคำตอบสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p7:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 ผลโหวตภาพรวม Dilemma 2")
    if conn:
        try:
            df = conn.read(worksheet="Lab1_Responses", ttl=5)
            p7_df = df[df["Step"] == "Lab1 - Page7 Dilemma2 Vote"]
            if not p7_df.empty:
                votes = p7_df["Data"].apply(lambda x: x.split("Choice: ")[1].strip() if "Choice: " in x else x)
                st.bar_chart(votes.value_counts())
        except:
            pass


# ==========================================
# PAGE 8 — WHY?
# ==========================================
elif st.session_state.lab1_page == 8:
    st.title("❓ PAGE 8 — Why? (เหตุผลเบื้องหลัง)")
    st.markdown("### หลังเห็นผลโหวต “เหตุผลหลักของคุณคืออะไร?”")

    why_options = [
        "ความยุติธรรม", "ความซื่อสัตย์", "ความสัมพันธ์กับเพื่อน",
        "ผลกระทบต่อเพื่อน", "ความรับผิดชอบ", "กฎของรายวิชา",
        "ผลประโยชน์ของกลุ่ม", "อื่น ๆ"
    ]

    with st.form("lab1_p8_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        st.markdown("เลือกเหตุผลหลัก (ไม่เกิน 2 ข้อ):")
        selected_whys = []
        for w in why_options:
            if st.checkbox(w, key=f"w_{w}"):
                selected_whys.append(w)
                
        expl_text = st.text_area("“ถ้าเหตุผลของคุณขัดกับเหตุผลของเพื่อน คุณจะอธิบายการตัดสินใจของคุณอย่างไร?”")
        
        sub_p8 = st.form_submit_button("ส่งคำตอบ Why")

        if sub_p8 and student_id:
            if len(selected_whys) <= 2 and len(selected_whys) > 0:
                joined_w = ", ".join(selected_whys)
                combined_why = f"Why: {joined_w} | Expl: {expl_text}"
                new_data = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Step": "Lab1 - Page8 Why",
                    "Data": f"[{student_id}] {combined_why}"
                }])
                if conn:
                    try:
                        existing = conn.read(worksheet="Lab1_Responses", ttl=0)
                        updated = pd.concat([existing, new_data], ignore_index=True)
                        conn.update(worksheet="Lab1_Responses", data=updated)
                        st.success("บันทึกสำเร็จ!")
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
                else:
                    st.success("บันทึกจำลองสำเร็จ!")
            else:
                st.warning("กรุณาเลือกเหตุผล 1-2 ข้อเท่านั้น")
        elif sub_p8:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.info("💡 **Key Learning:** คำตอบเดียวกัน $\neq$ เหตุผลเดียวกัน และ คำตอบต่างกัน $\neq$ คนหนึ่งต้องผิดเสมอไป")


# ==========================================
# PAGE 9 — PHARMACY DILEMMA
# ==========================================
elif st.session_state.lab1_page == 9:
    st.title("💊 PAGE 9 — Pharmacy Dilemma")
    st.markdown("### เข้าสู่บริบททางวิชาชีพเภสัชกรรม")
    st.info(
        """
        **สถานการณ์:** ผู้ป่วยมาขอคำแนะนำเกี่ยวกับผลิตภัณฑ์สุขภาพชนิดหนึ่ง เภสัชกรพบว่าผลิตภัณฑ์ดังกล่าวถูกกฎหมายและสามารถจำหน่ายได้ แต่หลักฐานเกี่ยวกับประโยชน์ของผลิตภัณฑ์ยังมีข้อจำกัด ผู้ป่วยเชื่อว่าผลิตภัณฑ์นี้จะช่วยตนเองได้ และต้องการซื้อ เภสัชกรควรทำอย่างไร?
        """
    )

    with st.form("lab1_p9_form"):
        student_id = st.text_input("รหัสนิสิต:")
        p_choice = st.radio(
            "เลือกแนวทางของเภสัชกร:",
            [
                "A. จำหน่าย เพราะถูกกฎหมาย",
                "B. ไม่จำหน่าย เพราะหลักฐานยังไม่เพียงพอ",
                "C. ให้ข้อมูลข้อดี–ข้อจำกัด แล้วให้ผู้ป่วยตัดสินใจ",
                "D. ซักถามข้อมูลเพิ่มเติมก่อนตัดสินใจ",
                "E. อื่น ๆ"
            ]
        )
        sub_p9 = st.form_submit_button("ส่งคำตอบ Pharmacy Dilemma")

        if sub_p9 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab1 - Page9 Pharm Vote",
                "Data": f"[{student_id}] Vote: {p_choice[0]}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab1_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab1_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p9:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 ผลโหวต Pharmacy Dilemma ทั้งห้อง")
    if conn:
        try:
            df = conn.read(worksheet="Lab1_Responses", ttl=5)
            p9_df = df[df["Step"] == "Lab1 - Page9 Pharm Vote"]
            if not p9_df.empty:
                votes = p9_df["Data"].apply(lambda x: x.split("Vote: ")[1].strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
        except:
            pass


# ==========================================
# PAGE 10 — GROUP ETHICAL REASONING
# ==========================================
elif st.session_state.lab1_page == 10:
    st.title("📋 PAGE 10 — Group Ethical Reasoning Canvas")
    st.markdown("ทุกกลุ่มร่วมกันวิเคราะห์ Case เดียวกันผ่าน Ethical Reasoning Canvas 9 ขั้นตอน")

    with st.form("lab1_p10_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        c1 = st.text_input("1. FACTS: เรารู้อะไร?")
        c2 = st.text_input("2. UNKNOWN: เรายังไม่รู้อะไร?")
        c3 = st.text_input("3. STAKEHOLDERS: ใครได้รับผลกระทบ?")
        c4 = st.text_input("4. ETHICAL ISSUE: ประเด็นจริยธรรมคืออะไร?")
        c5 = st.text_input("5. VALUES: มีคุณค่าอะไรที่เกี่ยวข้อง?")
        c6 = st.text_input("6. RULES: มีกฎหมาย/กฎ/มาตรฐานวิชาชีพอะไรเกี่ยวข้อง?")
        c7 = st.text_input("7. OPTIONS: มีทางเลือกอะไรบ้าง?")
        c8 = st.text_input("8. DECISION: กลุ่มเลือกอะไร?")
        c9 = st.text_area("9. WHY?: เพราะอะไร?")
        
        sub_p10 = st.form_submit_button("ส่ง Ethical Canvas ของกลุ่ม")

        if sub_p10 and group_name:
            combined_canvas = f"F:{c1}|U:{c2}|S:{c3}|I:{c4}|V:{c5}|R:{c6}|O:{c7}|D:{c8}|W:{c9}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab1 - Page10 Canvas",
                "Data": f"[{group_name}] {combined_canvas}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab1_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab1_Responses", data=updated)
                    st.success("บันทึก Canvas สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p10:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางเปรียบเทียบคำตอบแต่ละกลุ่ม (สำหรับให้อาจารย์สุ่มอภิปรายจุดต่าง)")
    if conn:
        try:
            df = conn.read(worksheet="Lab1_Responses", ttl=5)
            p10_df = df[df["Step"] == "Lab1 - Page10 Canvas"]
            if not p10_df.empty:
                st.dataframe(p10_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# PAGE 11 — CHALLENGE
# ==========================================
elif st.session_state.lab1_page == 11:
    st.title("⚡ PAGE 11 — Challenge (เพิ่มข้อมูลใหม่)")
    st.markdown("หลังจากกลุ่มตัดสินใจแล้ว ระบบเพิ่มข้อมูลใหม่เข้ามาท้าทายการตัดสินใจ")

    with st.form("lab1_p11_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        challenge_type = st.selectbox(
            "เลือก Challenge:",
            [
                "Challenge 1: ผู้ป่วยมีรายได้น้อยและบอกว่า หากไม่ได้ซื้อผลิตภัณฑ์นี้ เขาอาจไม่สามารถหาทางเลือกอื่นได้",
                "Challenge 2: เภสัชกรพบว่าผลิตภัณฑ์มีทางเลือกอื่นที่มีหลักฐานสนับสนุนมากกว่า แต่มีราคาสูงกว่า",
                "Challenge 3: ผู้ป่วยยืนยันว่าได้รับข้อมูลจากแหล่งอื่นมาแล้ว และต้องการซื้อโดยไม่ต้องการคำแนะนำเพิ่มเติม"
            ]
        )
        
        still_same = st.radio("“คุณยังตัดสินใจเหมือนเดิมหรือไม่?”", ["เหมือนเดิม", "เปลี่ยนการตัดสินใจ", "ปรับเปลี่ยนบางส่วน"])
        ch_reason = st.text_area("อธิบายเหตุผลประกอบข้อมูลใหม่:")
        
        sub_p11 = st.form_submit_button("ส่งผล Challenge")

        if sub_p11 and group_name:
            tag = challenge_type.split(":")[0]
            combined_ch = f"Ch: {tag} | Decision: {still_same} | Reason: {ch_reason}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab1 - Page11 Challenge",
                "Data": f"[{group_name}] {combined_ch}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab1_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab1_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p11:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Challenge ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab1_Responses", ttl=5)
            p11_df = df[df["Step"] == "Lab1 - Page11 Challenge"]
            if not p11_df.empty:
                st.dataframe(p11_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# PAGE 12 — RE-VOTE
# ==========================================
elif st.session_state.lab1_page == 12:
    st.title("🔄 PAGE 12 — Re-Vote (Before → After)")
    st.markdown("### ขึ้นคำถามเดิม: “เภสัชกรควรทำอย่างไร?” ให้โหวตอีกครั้ง")

    with st.form("lab1_p12_form"):
        student_id = st.text_input("รหัสนิสิต:")
        revote_choice = st.radio(
            "เลือกคำตอบใหม่อีกครั้ง:",
            [
                "A. จำหน่าย เพราะถูกกฎหมาย",
                "B. ไม่จำหน่าย เพราะหลักฐานยังไม่เพียงพอ",
                "C. ให้ข้อมูลข้อดี–ข้อจำกัด แล้วให้ผู้ป่วยตัดสินใจ",
                "D. ซักถามข้อมูลเพิ่มเติมก่อนตัดสินใจ",
                "E. อื่น ๆ"
            ]
        )
        sub_p12 = st.form_submit_button("ส่ง Re-Vote")

        if sub_p12 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab1 - Page12 ReVote",
                "Data": f"[{student_id}] After: {revote_choice[0]}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab1_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab1_Responses", data=updated)
                    st.success("บันทึก Re-Vote สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p12:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 เปรียบเทียบผลโหวต Before (Page 9) vs After (Page 12)")
    if conn:
        try:
            df = conn.read(worksheet="Lab1_Responses", ttl=5)
            
            c_b, c_a = st.columns(2)
            with c_b:
                st.markdown("**Before (Page 9)**")
                b_df = df[df["Step"] == "Lab1 - Page9 Pharm Vote"]
                if not b_df.empty:
                    vb = b_df["Data"].apply(lambda x: x.split("Vote: ")[1].strip() if "Vote: " in x else x)
                    st.bar_chart(vb.value_counts())
                else:
                    st.info("ยังไม่มีข้อมูล Before")
            
            with c_a:
                st.markdown("**After (Page 12)**")
                a_df = df[df["Step"] == "Lab1 - Page12 ReVote"]
                if not a_df.empty:
                    va = a_df["Data"].apply(lambda x: x.split("After: ")[1].strip() if "After: " in x else x)
                    st.bar_chart(va.value_counts())
                else:
                    st.info("ยังไม่มีข้อมูล After")
        except:
            pass
    st.info("💡 **Key Concept:** Ethical reasoning is revisable when relevant information changes.")


# ==========================================
# PAGE 13 — BUILD THE FRAMEWORK
# ==========================================
elif st.session_state.lab1_page == 13:
    st.title("🛠️ PAGE 13 — Build the Framework")
    st.markdown("### “ถ้าคุณต้องสร้างขั้นตอนในการตัดสินใจทางจริยธรรมด้วยตัวเอง คุณจะเรียงขั้นตอนอย่างไร?”")
    st.info("การ์ดขั้นตอน: FACTS, STAKEHOLDERS, ETHICAL ISSUE, VALUES, RULES, OPTIONS, CONSEQUENCES, DECISION, JUSTIFICATION")

    with st.form("lab1_p13_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        framework_order = st.text_area("เรียงลำดับขั้นตอนและอธิบายสั้น ๆ:")
        sub_p13 = st.form_submit_button("ส่ง Framework ของกลุ่ม")

        if sub_p13 and group_name and framework_order:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab1 - Page13 Framework",
                "Data": f"[{group_name}] {framework_order}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab1_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab1_Responses", data=updated)
                    st.success("บันทึก Framework สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p13:
            st.warning("กรุณากรอกชื่อกลุ่มและลำดับขั้นตอน")

    st.markdown("---")
    st.subheader("📋 ตารางแสดง Framework ที่แต่ละกลุ่มออกแบบ")
    if conn:
        try:
            df = conn.read(worksheet="Lab1_Responses", ttl=5)
            p13_df = df[df["Step"] == "Lab1 - Page13 Framework"]
            if not p13_df.empty:
                st.dataframe(p13_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass


# ==========================================
# PAGE 14 — EXIT REFLECTION
# ==========================================
elif st.session_state.lab1_page == 14:
    st.title("🎯 PAGE 14 — Exit Reflection")
    st.markdown("ตอบคนเดียว 4 นาทีสุดท้าย (ไม่ต้องอภิปราย)")

    with st.form("lab1_p14_form"):
        student_id = st.text_input("รหัสนิสิต (ระบุหรือไม่ระบุก็ได้):")
        
        q1 = st.text_area("Q1: วันนี้มีอะไรที่ทำให้คุณเปลี่ยนความคิด?")
        q2 = st.text_area("Q2: เมื่อคุณตัดสินใจทางจริยธรรม สิ่งที่คุณให้ความสำคัญมากที่สุดคืออะไร?")
        q3 = st.text_area("Q3: สิ่งหนึ่งที่คุณอยากฝึกเกี่ยวกับการตัดสินใจทางจริยธรรมคืออะไร?")
        
        sub_p14 = st.form_submit_button("ส่ง Exit Reflection")

        if sub_p14 and student_id:
            sid_val = "Anonymous" if not student_id else student_id
            combined_ref = f"Q1: {q1} | Q2: {q2} | Q3: {q3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab1 - Exit Reflection",
                "Data": f"[{sid_val}] {combined_ref}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab1_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab1_Responses", data=updated)
                    st.success("บันทึก Exit Reflection สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p14:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางรวบรวม Exit Reflection ทั้งหมด")
    if conn:
        try:
            df = conn.read(worksheet="Lab1_Responses", ttl=5)
            p14_df = df[df["Step"] == "Lab1 - Exit Reflection"]
            if not p14_df.empty:
                st.dataframe(p14_df[["Timestamp", "Data"]], use_container_width=True)
            else:
                st.info("ยังไม่มีข้อมูล")
        except:
            pass