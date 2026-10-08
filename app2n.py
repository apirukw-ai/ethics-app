from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 2: Everyday Ethical Decision Making",
    page_icon="⚖️",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab2_page" not in st.session_state:
    st.session_state.lab2_page = 1

# --- Sidebar เมนูด้านซ้าย (12 หน้า) ---
st.sidebar.markdown("### ⚖️ LAB 2 Workflow")

pages_name = {
    1: "PAGE 1: Welcome",
    2: "PAGE 2: From Lab 1 → Lab 2",
    3: "PAGE 3: Scenario 1 (Quick Decision)",
    4: "PAGE 4: See the Room",
    5: "PAGE 5: Why? (เหตุผลเบื้องหลัง)",
    6: "PAGE 6: Scenario 2 (Ethical Dilemma)",
    7: "PAGE 7: Facts & Unknowns (Canvas)",
    8: "PAGE 8: Stakeholder Map (Challenges)",
    9: "PAGE 9: Ethical Tension Map",
    10: "PAGE 10: Decision Framework",
    11: "PAGE 11: Professional Bridge",
    12: "PAGE 12: Exit Reflection",
}

current_index = list(pages_name.keys()).index(st.session_state.lab2_page)

selected_page_name = st.sidebar.radio(
    "เลือกหน้า LAB 2:",
    list(pages_name.values()),
    index=current_index,
    key="lab2_menu_selection",
)

for p_num, p_title in pages_name.items():
    if p_title == selected_page_name:
        st.session_state.lab2_page = p_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อด้านบนเพื่อเปลี่ยนหน้ากิจกรรม")


# ==========================================
# PAGE 1 — Welcome
# ==========================================
if st.session_state.lab2_page == 1:
    st.title("⚖️ LAB 2")
    st.subheader("การคิดและตัดสินใจทางจริยธรรมในชีวิตประจำวัน")
    st.markdown("### “เมื่อไม่มีทางเลือกใดสมบูรณ์แบบ เราจะตัดสินใจอย่างไร?”")
    st.markdown("---")
    st.warning(
        """
        ### 📌 กติกาสำคัญวันนี้
        **“วันนี้ไม่มีคะแนนสำหรับการตอบเหมือนอาจารย์ คะแนนอยู่ที่คุณภาพของเหตุผล”**
        """
    )


# ==========================================
# PAGE 2 — Connect to Lab 1
# ==========================================
elif st.session_state.lab2_page == 2:
    st.title("🌉 PAGE 2 — จาก Lab 1 → Lab 2")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("### 📘 Lab 1\n**อะไรทำให้การกระทำหนึ่งถูก/ไม่ถูกต้อง?**")
    with col2:
        st.success("### 📗 Lab 2\n**เมื่อเจอสถานการณ์จริง เราจะตัดสินใจอย่างไร?**")

    st.markdown("---")
    st.markdown("### 🔄 กรอบความคิดต่อเนื่องของเรา:")
    st.markdown(
        """
        #### **FACTS → STAKEHOLDERS → ETHICAL ISSUE → VALUES → OPTIONS → CONSEQUENCES → DECISION → WHY**
        """
    )


# ==========================================
# PAGE 3 — Scenario 1: Quick Decision
# ==========================================
elif st.session_state.lab2_page == 3:
    st.title("👥 PAGE 3 — Scenario 1: Quick Decision")
    st.info(
        """
        **สถานการณ์:** คุณทำงานกลุ่มกับเพื่อน 5 คน เพื่อนคนหนึ่งแทบไม่ได้ช่วยทำงาน แต่เมื่อใกล้ส่งงาน เพื่อนขอให้ใส่ชื่อของเขาในรายงานด้วย
        """
    )
    st.markdown("### “คุณควรทำอย่างไร?”")

    with st.form("lab2_p3_form"):
        student_id = st.text_input("รหัสนิสิต:")
        s1_choice = st.radio(
            "เลือกการตัดสินใจ (Pre-Vote):",
            [
                "A. ใส่ชื่อให้ เพราะเป็นเพื่อนกัน",
                "B. ไม่ใส่ชื่อ เพราะไม่ได้ช่วยงาน",
                "C. ใส่ชื่อ แต่บอกเพื่อนว่าครั้งหน้าต้องรับผิดชอบมากกว่านี้",
                "D. คุยกับเพื่อนก่อน แล้วหาทางออกที่เหมาะสม",
                "E. อื่น ๆ"
            ]
        )
        sub_p3 = st.form_submit_button("ส่ง Pre-Vote Scenario 1")

        if sub_p3 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Page3 Scenario1 Vote",
                "Data": f"[{student_id}] Vote: {s1_choice[0]}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึก Pre-Vote สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p3:
            st.warning("กรุณากรอกรหัสนิสิต")


# ==========================================
# PAGE 4 — See the Room
# ==========================================
elif st.session_state.lab2_page == 4:
    st.title("📊 PAGE 4 — See the Room")
    st.markdown("### ผลโหวต Real-time ของทั้งห้อง (Scenario 1)")

    if conn:
        try:
            df = conn.read(worksheet="Lab2_Responses", ttl=5)
            p3_df = df[df["Step"] == "Lab2 - Page3 Scenario1 Vote"]
            if not p3_df.empty:
                votes = p3_df["Data"].apply(lambda x: x.split("Vote: ")[1].strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
            else:
                st.info("ยังไม่มีข้อมูลการโหวตในระบบ")
        except:
            pass

    st.markdown("---")
    st.warning("🤔 **คำถามชวนคิด:** “ทำไมคนในห้องจึงเลือกต่างกัน?”")


# ==========================================
# PAGE 5 — Why?
# ==========================================
elif st.session_state.lab2_page == 5:
    st.title("❓ PAGE 5 — Why? (เหตุผลเบื้องหลัง)")
    st.markdown("### เหตุผลที่สำคัญที่สุดของคุณคืออะไร? (เลือกได้สูงสุด 2 ข้อ)")

    why_options = [
        "ความยุติธรรม", "ความซื่อสัตย์", "ความรับผิดชอบ",
        "ความสัมพันธ์กับเพื่อน", "ผลกระทบต่อกลุ่ม", "กฎ/ระเบียบ",
        "การให้โอกาส", "เจตนาของเพื่อน", "ประโยชน์ของส่วนรวม", "อื่น ๆ"
    ]

    with st.form("lab2_p5_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        selected_whys = []
        for w in why_options:
            if st.checkbox(w, key=f"l2_w_{w}"):
                selected_whys.append(w)
                
        ethics_q = st.text_area("“ถ้าคนสองคนเลือกคำตอบต่างกัน แปลว่าคนหนึ่งมีจริยธรรม แต่อีกคนไม่มีหรือไม่? จงอธิบายสั้น ๆ”")
        
        sub_p5 = st.form_submit_button("ส่งคำตอบ Why")

        if sub_p5 and student_id:
            if len(selected_whys) <= 2 and len(selected_whys) > 0:
                joined_w = ", ".join(selected_whys)
                combined_why = f"Why: {joined_w} | Note: {ethics_q}"
                new_data = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Step": "Lab2 - Page5 Why",
                    "Data": f"[{student_id}] {combined_why}"
                }])
                if conn:
                    try:
                        existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                        updated = pd.concat([existing, new_data], ignore_index=True)
                        conn.update(worksheet="Lab2_Responses", data=updated)
                        st.success("บันทึกสำเร็จ!")
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
                else:
                    st.success("บันทึกจำลองสำเร็จ!")
            else:
                st.warning("กรุณาเลือกเหตุผล 1-2 ข้อเท่านั้น")
        elif sub_p5:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงความเห็นของนิสิต")
    if conn:
        try:
            df = conn.read(worksheet="Lab2_Responses", ttl=5)
            p5_df = df[df["Step"] == "Lab2 - Page5 Why"]
            if not p5_df.empty:
                st.dataframe(p5_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# PAGE 6 — Scenario 2: Ethical Dilemma
# ==========================================
elif st.session_state.lab2_page == 6:
    st.title("🧑‍🤝‍🧑 PAGE 6 — Scenario 2: Ethical Dilemma")
    st.info(
        """
        **Case: “เพื่อนที่มีเหตุผล”**  
        สถานการณ์: คุณทำงานกลุ่มกับเพื่อน 5 คน สมาชิกคนหนึ่งชื่อ “นนท์” แทบไม่ได้เข้าร่วมประชุมและไม่ได้ช่วยทำรายงานในช่วงที่ผ่านมา ก่อนส่งงาน 1 วัน นนท์มาบอกว่า *“ช่วงที่ผ่านมาแม่เราป่วยหนัก เราต้องดูแลแม่ เลยไม่มีเวลาช่วยงาน แต่เราก็อยากให้มีชื่อในงานด้วย”* สมาชิกคนอื่น ๆ ต้องตัดสินใจว่าจะทำอย่างไร
        """
    )
    st.markdown("### “คุณคิดว่ากลุ่มควรทำอย่างไร?”")

    with st.form("lab2_p6_form"):
        student_id = st.text_input("รหัสนิสิต:")
        s2_choice = st.radio(
            "เลือกการตัดสินใจ (Pre-Vote Scenario 2):",
            [
                "A. ใส่ชื่อ เพราะมีเหตุจำเป็น",
                "B. ไม่ใส่ชื่อ เพราะไม่ได้มีส่วนร่วมกับงาน",
                "C. ใส่ชื่อ แต่ต้องปรับวิธีประเมิน/แบ่งงานให้เหมาะสม",
                "D. คุยกันก่อน แล้วหาวิธีให้สมาชิกมีส่วนร่วมชดเชย",
                "E. อื่น ๆ"
            ]
        )
        sub_p6 = st.form_submit_button("ส่ง Pre-Vote Scenario 2")

        if sub_p6 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Page6 Scenario2 Vote",
                "Data": f"[{student_id}] Vote: {s2_choice[0]}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p6:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 ผลโหวต Scenario 2 ภาพรวมห้อง")
    if conn:
        try:
            df = conn.read(worksheet="Lab2_Responses", ttl=5)
            p6_df = df[df["Step"] == "Lab2 - Page6 Scenario2 Vote"]
            if not p6_df.empty:
                votes = p6_df["Data"].apply(lambda x: x.split("Vote: ")[1].strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
        except:
            pass


# ==========================================
# PAGE 7 — Facts & Unknowns (Group Discussion)
# ==========================================
elif st.session_state.lab2_page == 7:
    st.title("📋 PAGE 7 — Facts & Unknowns (Group Discussion)")
    st.markdown("ภารกิจกลุ่ม: ร่วมกันวิเคราะห์ 5 ประเด็นสำคัญจาก Scenario 2")

    with st.form("lab2_p7_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        c1 = st.text_input("1. FACTS: เรารู้อะไรแน่นอน?")
        c2 = st.text_input("2. UNKNOWN: เรายังไม่รู้อะไรที่อาจมีผลต่อการตัดสินใจ?")
        c3 = st.text_input("3. STAKEHOLDERS: ใครบ้างที่จะได้รับผลกระทบ?")
        c4 = st.text_input("4. ETHICAL ISSUE: จริง ๆ แล้ว “ปัญหาจริยธรรม” ของกรณีนี้คืออะไร?")
        c5 = st.text_input("5. VALUES IN CONFLICT: มีคุณค่า/หน้าที่อะไรบ้างที่กำลังขัดแย้งกัน?")
        
        sub_p7 = st.form_submit_button("ส่งผลวิเคราะห์กลุ่ม")

        if sub_p7 and group_name:
            combined_f = f"Facts:{c1}|Unknown:{c2}|Stakeholders:{c3}|Issue:{c4}|Values:{c5}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Page7 Canvas",
                "Data": f"[{group_name}] {combined_f}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึก Canvas สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p7:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.info("💡 **ข้อคิดสำคัญ:** “อย่าเพิ่งตัดสินใจจนกว่าจะตรวจสอบว่าเรามีข้อมูลเพียงพอหรือไม่”")


# ==========================================
# PAGE 8 — Stakeholder Map (CHANGE ONE FACTOR)
# ==========================================
elif st.session_state.lab2_page == 8:
    st.title("⚡ PAGE 8 — Change One Factor (Challenges)")
    st.markdown("ทดสอบเปลี่ยนข้อมูลในสถานการณ์ แล้วดูว่าการตัดสินใจเปลี่ยนหรือไม่")

    with st.form("lab2_p8_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        st.markdown("#### **Challenge 1:**")
        st.info("ข้อมูลใหม่: นนท์ไม่ได้เพียงดูแลแม่ แต่ต้องพาแม่เข้าโรงพยาบาลหลายครั้งในช่วงที่กลุ่มทำงาน")
        ch1_dec = st.radio("การตัดสินใจของกลุ่มเปลี่ยนหรือไม่ (Ch 1):", ["เปลี่ยน", "ไม่เปลี่ยน", "ยังตัดสินใจไม่ได้"], key="ch1_radio")
        ch1_reason = st.text_input("ข้อมูลใหม่นี้เปลี่ยนอะไรในเหตุผลของคุณ?")
        
        st.markdown("---")
        st.markdown("#### **Challenge 2:**")
        st.info("ข้อมูลเพิ่มเติม: “แต่สมาชิกคนอื่นต้องทำงานเพิ่มทั้งหมด และหากใส่ชื่อทุกคน คะแนนของสมาชิกที่ทำงานหนักกับสมาชิกที่ไม่ได้ทำงานจะเท่ากัน”")
        ch2_dec = st.radio("ตอนนี้คุณยังตัดสินใจเหมือนเดิมหรือไม่ (Ch 2):", ["เปลี่ยน", "ไม่เปลี่ยน", "ยังตัดสินใจไม่ได้"], key="ch2_radio")
        ch2_reason = st.text_input("เหตุผลประกอบ Challenge 2:")
        
        sub_p8 = st.form_submit_button("ส่งผล Challenges")

        if sub_p8 and group_name:
            combined_ch = f"Ch1: {ch1_dec} ({ch1_reason}) | Ch2: {ch2_dec} ({ch2_reason})"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Page8 Challenges",
                "Data": f"[{group_name}] {combined_ch}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p8:
            st.warning("กรุณากรอกชื่อกลุ่ม")


# ==========================================
# PAGE 9 — Ethical Tension Map
# ==========================================
elif st.session_state.lab2_page == 9:
    st.title("🗺️ PAGE 9 — Ethical Tension Map")
    st.markdown("เลือก 2 คุณค่าที่ขัดแย้งกันมากที่สุด แล้ววิเคราะห์ผลกระทบสองด้าน")

    with st.form("lab2_p9_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        tension_pair = st.text_input("คู่คุณค่าที่ขัดแย้งกัน (เช่น ความยุติธรรม ↔ ความเห็นอกเห็นใจ):")
        loss_a = st.text_area("1. “ถ้าคุณให้ความสำคัญกับ Value A มากขึ้น คุณจะเสียอะไร?”")
        loss_b = st.text_area("2. “ถ้าคุณให้ความสำคัญกับ Value B มากขึ้น คุณจะเสียอะไร?”")
        
        sub_p9 = st.form_submit_button("ส่งผล Tension Map")

        if sub_p9 and group_name and tension_pair:
            combined_t = f"Pair: {tension_pair} | Loss A: {loss_a} | Loss B: {loss_b}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Page9 Tension Map",
                "Data": f"[{group_name}] {combined_t}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p9:
            st.warning("กรุณากรอกชื่อกลุ่มและคู่คุณค่า")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Ethical Tension Map ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab2_Responses", ttl=5)
            p9_df = df[df["Step"] == "Lab2 - Page9 Tension Map"]
            if not p9_df.empty:
                st.dataframe(p9_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# PAGE 10 — Decision Framework (Card Sorting)
# ==========================================
elif st.session_state.lab2_page == 10:
    st.title("🛠️ PAGE 10 — Decision Framework (Card Sorting)")
    st.markdown("### “ถ้าคุณต้องตัดสินใจเรื่องจริยธรรมจริง ๆ คุณจะคิดตามลำดับใด?”")
    st.info("ขั้นตอน: STAKEHOLDERS, ETHICAL ISSUE, VALUES, RULES, OPTIONS, CONSEQUENCES, DECISION, JUSTIFICATION")

    with st.form("lab2_p10_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        sort_order = st.text_area("เรียงลำดับขั้นตอนของกลุ่มคุณ:")
        sub_p10 = st.form_submit_button("ส่ง Framework ของกลุ่ม")

        if sub_p10 and group_name and sort_order:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Page10 Framework",
                "Data": f"[{group_name}] {sort_order}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p10:
            st.warning("กรุณากรอกชื่อกลุ่มและลำดับขั้นตอน")

    st.markdown("---")
    st.subheader("📋 ตารางแสดง Framework ที่แต่ละกลุ่มออกแบบ")
    if conn:
        try:
            df = conn.read(worksheet="Lab2_Responses", ttl=5)
            p10_df = df[df["Step"] == "Lab2 - Page10 Framework"]
            if not p10_df.empty:
                st.dataframe(p10_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# PAGE 11 — Professional Bridge
# ==========================================
elif st.session_state.lab2_page == 11:
    st.title("🌉 PAGE 11 — Professional Bridge")
    st.markdown("### “ถ้าสถานการณ์เดียวกันเกิดขึ้นกับเภสัชกร จะมีอะไรเพิ่มเข้ามาจากการตัดสินใจในชีวิตประจำวัน?”")
    st.info("💡 เลือกสิ่งที่คิดว่าจะเพิ่มขึ้น (เลือกได้หลายข้อ)")

    bridge_options = [
        "ความรับผิดชอบต่อผู้ป่วย", "กฎหมาย", "จรรยาบรรณวิชาชีพ",
        "มาตรฐานวิชาชีพ", "ความปลอดภัย", "ความไว้วางใจของสังคม",
        "ผลกระทบต่อวิชาชีพ", "อื่น ๆ"
    ]

    with st.form("lab2_p11_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        selected_bridge = []
        for b in bridge_options:
            if st.checkbox(b, key=f"l2_b_{b}"):
                selected_bridge.append(b)
                
        sub_p11 = st.form_submit_button("ส่งข้อมูล Professional Bridge")

        if sub_p11 and student_id:
            if len(selected_bridge) > 0:
                joined_b = ", ".join(selected_bridge)
                new_data = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Step": "Lab2 - Page11 Bridge",
                    "Data": f"[{student_id}] Bridge: {joined_b}"
                }])
                if conn:
                    try:
                        existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                        updated = pd.concat([existing, new_data], ignore_index=True)
                        conn.update(worksheet="Lab2_Responses", data=updated)
                        st.success("บันทึกสำเร็จ!")
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
                else:
                    st.success("บันทึกจำลองสำเร็จ!")
            else:
                st.warning("กรุณาเลือกอย่างน้อย 1 ข้อ")
        elif sub_p11:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผลโหวตสิ่งที่เพิ่มขึ้นในมุมมองวิชาชีพ")
    if conn:
        try:
            df = conn.read(worksheet="Lab2_Responses", ttl=5)
            p11_df = df[df["Step"] == "Lab2 - Page11 Bridge"]
            if not p11_df.empty:
                all_b = []
                for item in p11_df["Data"]:
                    if "Bridge: " in item:
                        part = item.split("Bridge: ")[1]
                        all_b.extend([x.strip() for x in part.split(",")])
                if all_b:
                    st.bar_chart(pd.Series(all_b).value_counts())
        except:
            pass


# ==========================================
# PAGE 12 — Exit Reflection
# ==========================================
elif st.session_state.lab2_page == 12:
    st.title("🎯 PAGE 12 — Exit Reflection (Lab 2)")
    st.markdown("ตอบ 3 ข้อสั้น ๆ ท้ายคาบ")

    with st.form("lab2_p12_form"):
        student_id = st.text_input("รหัสนิสิต (ระบุหรือไม่ระบุก็ได้):")
        
        r1 = st.text_area("1. Before: ก่อน Lab วันนี้ ฉันคิดว่าการตัดสินใจทางจริยธรรมคือ...")
        r2 = st.text_area("2. Now: ตอนนี้ฉันคิดว่าการตัดสินใจทางจริยธรรมคือ...")
        r3 = st.text_area("3. Next: สิ่งหนึ่งที่ฉันจะนำไปใช้เมื่อต้องตัดสินใจเรื่องยาก ๆ คือ...")
        
        sub_ref = st.form_submit_button("ส่ง Exit Reflection Lab 2")

        if sub_ref and student_id:
            sid_val = "Anonymous" if not student_id else student_id
            combined_ref = f"Before: {r1} | Now: {r2} | Next: {r3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab2 - Exit Reflection",
                "Data": f"[{sid_val}] {combined_ref}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab2_Responses", data=updated)
                    st.success("บันทึก Exit Reflection สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_ref:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางรวบรวม Exit Reflection (Lab 2)")
    if conn:
        try:
            df = conn.read(worksheet="Lab2_Responses", ttl=5)
            ref_df = df[df["Step"] == "Lab2 - Exit Reflection"]
            if not ref_df.empty:
                st.dataframe(ref_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass