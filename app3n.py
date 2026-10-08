from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 3: Professional Character & Virtues",
    page_icon="🛡️",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab3_page" not in st.session_state:
    st.session_state.lab3_page = 1

# --- Sidebar เมนูด้านซ้าย (18 หน้า) ---
st.sidebar.markdown("### 🛡️ LAB 3 Workflow")

pages_name = {
    1: "PAGE 1: Welcome",
    2: "PAGE 2: Connect (Lab 1-3)",
    3: "PAGE 3: Choose Your Professional",
    4: "PAGE 4: Group Virtue Analysis",
    5: "PAGE 5: Why It Matters",
    6: "PAGE 6: Observable Evidence",
    7: "PAGE 7: Strongest Evidence",
    8: "PAGE 8: Virtue vs Non-Virtue",
    9: "PAGE 9: Virtue Conflict Vote",
    10: "PAGE 10: Ethical Tension Map",
    11: "PAGE 11: Professional Dilemma",
    12: "PAGE 12: Reasoning (Support)",
    13: "PAGE 13: Challenge 1 (Severity)",
    14: "PAGE 14: Challenge 2 (Repeat)",
    15: "PAGE 15: Challenge 3 (Harm Done)",
    16: "PAGE 16: Virtue Map (Group)",
    17: "PAGE 17: Peer Challenge",
    18: "PAGE 18: Professional Identity",
}

current_index = list(pages_name.keys()).index(st.session_state.lab3_page)

selected_page_name = st.sidebar.radio(
    "เลือกหน้า LAB 3:",
    list(pages_name.values()),
    index=current_index,
    key="lab3_menu_selection",
)

for p_num, p_title in pages_name.items():
    if p_title == selected_page_name:
        st.session_state.lab3_page = p_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อด้านบนเพื่อเปลี่ยนหน้ากิจกรรม")


# ==========================================
# PAGE 1 — Welcome
# ==========================================
if st.session_state.lab3_page == 1:
    st.title("🛡️ LAB 3")
    st.subheader("คุณธรรมและจริยธรรมของผู้ประกอบวิชาชีพ")
    st.markdown("### What Kind of Professional Should I Become?")
    st.markdown("---")
    st.warning("### “ผู้ประกอบวิชาชีพที่ดีควรเป็นคนแบบไหน?”")


# ==========================================
# PAGE 2 — Connect
# ==========================================
elif st.session_state.lab3_page == 2:
    st.title("🌉 PAGE 2 — From Ethical Decision → Professional Character")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 📘 Lab 1\n**เราตัดสินว่าอะไรถูก/ผิดอย่างไร?**")
    with col2:
        st.warning("### 📗 Lab 2\n**เราตัดสินใจอย่างไรเมื่อคุณค่าขัดแย้งกัน?**")
    with col3:
        st.success("### 📙 Lab 3\n**คนที่ตัดสินใจอย่างมีจริยธรรมควรมีคุณธรรมอะไร?**")


# ==========================================
# PAGE 3 — Choose Your Professional
# ==========================================
elif st.session_state.lab3_page == 3:
    st.title("👥 PAGE 3 — Choose Your Professional")
    st.markdown("### “ถ้าคุณต้องเลือกเภสัชกรหนึ่งคนให้ดูแลคนในครอบครัว คุณจะเลือกคนแบบไหน?”")
    st.info("💡 เลือกคุณลักษณะที่สำคัญที่สุด **สูงสุด 5 ข้อ**")

    virtues_options = [
        "ซื่อสัตย์", "รับผิดชอบ", "มีเมตตา/เห็นอกเห็นใจ", "ยุติธรรม",
        "กล้าตัดสินใจ", "รอบคอบ", "เคารพผู้ป่วย", "มีความรู้",
        "มีวินัย", "กล้ายอมรับความผิด", "รักษาความลับ", "เสียสละ",
        "เคารพกฎหมาย", "เป็นมืออาชีพ", "อื่น ๆ"
    ]

    with st.form("lab3_p3_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        selected_virtues = []
        for v in virtues_options:
            if st.checkbox(v, key=f"l3_v_{v}"):
                selected_virtues.append(v)
                
        sub_p3 = st.form_submit_button("ส่งคุณลักษณะที่เลือก")

        if sub_p3 and student_id:
            if 0 < len(selected_virtues) <= 5:
                joined_v = ", ".join(selected_virtues)
                new_data = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Step": "Lab3 - Page3 ChooseProf",
                    "Data": f"[{student_id}] Virtues: {joined_v}"
                }])
                if conn:
                    try:
                        existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                        updated = pd.concat([existing, new_data], ignore_index=True)
                        conn.update(worksheet="Lab3_Responses", data=updated)
                        st.success("บันทึกสำเร็จ!")
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
                else:
                    st.success("บันทึกจำลองสำเร็จ!")
            else:
                st.warning("กรุณาเลือกคุณลักษณะ 1 ถึง 5 ข้อเท่านั้น")
        elif sub_p3:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 Top คุณลักษณะที่ห้องนี้เลือก (Top 10)")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_Responses", ttl=5)
            p3_df = df[df["Step"] == "Lab3 - Page3 ChooseProf"]
            if not p3_df.empty:
                all_v = []
                for item in p3_df["Data"]:
                    if "Virtues: " in item:
                        part = item.split("Virtues: ")[1]
                        all_v.extend([x.strip() for x in part.split(",")])
                if all_v:
                    s_series = pd.Series(all_v).value_counts().head(10)
                    st.bar_chart(s_series)
        except:
            pass


# ==========================================
# PAGE 4 — Group Virtue
# ==========================================
elif st.session_state.lab3_page == 4:
    st.title("📋 PAGE 4 — Group Virtue Analysis")
    st.markdown("### แต่ละกลุ่มเลือก 1 คุณธรรม (จาก Top ของห้อง) มาวิเคราะห์เชิงลึก")

    with st.form("lab3_p4_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        chosen_virtue = st.text_input("คุณธรรมที่กลุ่มเลือก:")
        
        q1 = st.text_area("1. ความหมาย: “สำหรับกลุ่มเรา คุณธรรมนี้หมายถึงอะไร?”")
        q2 = st.text_area("2. ทำไมจึงสำคัญ?: “ถ้าเภสัชกรขาดคุณธรรมนี้ จะเกิดอะไรขึ้น?”")
        
        st.markdown("3. เกี่ยวข้องกับใครบ้าง? (เลือกได้หลายข้อ)")
        stake_list = ["ผู้ป่วย", "ครอบครัว", "เพื่อนร่วมงาน", "องค์กร", "วิชาชีพ", "สังคม"]
        selected_stakes = []
        for s in stake_list:
            if st.checkbox(s, key=f"l3_s_{s}"):
                selected_stakes.append(s)
                
        q3 = st.text_area("4. ความเข้าใจผิด: “อะไรคือสิ่งที่ดูเหมือนเป็นคุณธรรมนี้ แต่จริง ๆ แล้วอาจไม่ใช่?” (เช่น รับผิดชอบ ≠ ทำทุกอย่างเอง)")
        
        sub_p4 = st.form_submit_button("ส่งผลวิเคราะห์กลุ่ม")

        if sub_p4 and group_name and chosen_virtue:
            joined_s = ", ".join(selected_stakes)
            combined_gv = f"Virtue: {chosen_virtue} | Meaning: {q1} | Why: {q2} | Stakes: {joined_s} | Misconception: {q3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3 - Page4 GroupVirtue",
                "Data": f"[{group_name}] {combined_gv}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p4:
            st.warning("กรุณากรอกชื่อกลุ่มและคุณธรรมที่เลือก")

    st.markdown("---")
    st.subheader("📋 ตารางสรุปการวิเคราะห์คุณธรรมของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_Responses", ttl=5)
            p4_df = df[df["Step"] == "Lab3 - Page4 GroupVirtue"]
            if not p4_df.empty:
                st.dataframe(p4_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# PAGE 5 — Why It Matters
# ==========================================
elif st.session_state.lab3_page == 5:
    st.title("❓ PAGE 5 — Why It Matters")
    st.markdown("### ถ้าเภสัชกรขาดคุณธรรมที่กลุ่มเลือก จะเกิดผลกระทบอย่างไร?")

    impact_options = [
        "Patient harm", "Loss of trust", "Professional misconduct",
        "Unfairness", "Team problems", "Social impact", "Other"
    ]

    with st.form("lab3_p5_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        selected_impacts = []
        for imp in impact_options:
            if st.checkbox(imp, key=f"l3_imp_{imp}"):
                selected_impacts.append(imp)
                
        reason_imp = st.text_area("อธิบายเหตุผลสั้น ๆ เพิ่มเติม:")
        
        sub_p5 = st.form_submit_button("ส่งผล Why It Matters")

        if sub_p5 and group_name:
            joined_imp = ", ".join(selected_impacts)
            combined_m = f"Impacts: {joined_imp} | Reason: {reason_imp}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3 - Page5 WhyMatters",
                "Data": f"[{group_name}] {combined_m}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p5:
            st.warning("กรุณากรอกชื่อกลุ่ม")


# ==========================================
# PAGE 6 — Evidence
# ==========================================
elif st.session_state.lab3_page == 6:
    st.title("🔍 PAGE 6 — Observable Evidence")
    st.markdown("### เราจะรู้ได้อย่างไรว่า “เขามีคุณธรรมนี้”?")
    st.info("ระบุพฤติกรรมที่สังเกตได้อย่างน้อย 3 ข้อ (เช่น 1. ตรวจสอบข้อมูลก่อนจ่ายยา 2. ติดตามปัญหา 3. ยอมรับผิด)")

    with st.form("lab3_p6_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        b1 = st.text_input("พฤติกรรมที่ 1:")
        b2 = st.text_input("พฤติกรรมที่ 2:")
        b3 = st.text_input("พฤติกรรมที่ 3:")
        
        sub_p6 = st.form_submit_button("ส่งพฤติกรรมที่สังเกตได้")

        if sub_p6 and group_name and b1 and b2 and b3:
            combined_b = f"1: {b1} | 2: {b2} | 3: {b3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3 - Page6 Evidence",
                "Data": f"[{group_name}] {combined_b}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p6:
            st.warning("กรุณากรอกชื่อกลุ่มและพฤติกรรมให้ครบ 3 ข้อ")


# ==========================================
# PAGE 7 — Strongest Evidence
# ==========================================
elif st.session_state.lab3_page == 7:
    st.title("⭐ PAGE 7 — Strongest Evidence")
    st.markdown("### พฤติกรรมใดจาก 3 ข้อที่กลุ่มเสนอ เป็นหลักฐานที่ชัด/แข็งแรงที่สุด?")

    with st.form("lab3_p7_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        strongest_b = st.selectbox("เลือกพฤติกรรมที่แข็งแรงที่สุด:", ["พฤติกรรมที่ 1", "พฤติกรรมที่ 2", "พฤติกรรมที่ 3"])
        why_strong = st.text_area("“เพราะอะไรพฤติกรรมนี้จึงสะท้อนคุณธรรมได้ชัดเจนที่สุด?”")
        
        sub_p7 = st.form_submit_button("ส่งพฤติกรรมที่แข็งแรงที่สุด")

        if sub_p7 and group_name:
            combined_str = f"Strongest: {strongest_b} | Reason: {why_strong}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3 - Page7 Strongest",
                "Data": f"[{group_name}] {combined_str}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p7:
            st.warning("กรุณากรอกชื่อกลุ่ม")


# ==========================================
# PAGE 8 — Virtue ≠ Virtue?
# ==========================================
elif st.session_state.lab3_page == 8:
    st.title("⚠️ PAGE 8 — Virtue ≠ Virtue?")
    st.markdown("### สิ่งใด “ดูเหมือน” เป็นคุณธรรมนี้ แต่จริง ๆ อาจไม่ใช่?")

    with st.form("lab3_p8_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        fake_virtue = st.text_area("สร้างตัวอย่างความเข้าใจผิดหรือพฤติกรรมที่สวมรอยเป็นคุณธรรมนี้ (เช่น การเสียสละ → ยอมทำผิดเพื่อช่วยเพื่อน):")
        
        sub_p8 = st.form_submit_button("ส่งตัวอย่างความเข้าใจผิด")

        if sub_p8 and group_name and fake_virtue:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3 - Page8 FakeVirtue",
                "Data": f"[{group_name}] {fake_virtue}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p8:
            st.warning("กรุณากรอกชื่อกลุ่มและคำตอบ")


# ==========================================
# PAGE 9 — Virtue Conflict
# ==========================================
elif st.session_state.lab3_page == 9:
    st.title("⚔️ PAGE 9 — Virtue Conflict")
    st.markdown("### “คุณธรรมที่ดีสองอย่างสามารถขัดแย้งกันได้หรือไม่?”")

    with st.form("lab3_p9_form"):
        student_id = st.text_input("รหัสนิสิต:")
        vc_vote = st.radio("เลือกคำตอบ:", ["ได้", "ไม่ได้", "ไม่แน่ใจ"])
        sub_p9 = st.form_submit_button("ส่งโหวต Virtue Conflict")

        if sub_p9 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3 - Page9 ConflictVote",
                "Data": f"[{student_id}] Vote: {vc_vote}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p9:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 ผลโหวตภาพรวมห้อง")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_Responses", ttl=5)
            p9_df = df[df["Step"] == "Lab3 - Page9 ConflictVote"]
            if not p9_df.empty:
                votes = p9_df["Data"].apply(lambda x: x.split("Vote: ")[1].strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
        except:
            pass


# ==========================================
# PAGE 10 — Ethical Tension
# ==========================================
elif st.session_state.lab3_page == 10:
    st.title("🗺️ PAGE 10 — Ethical Tension Map")
    st.markdown("เลือกคู่คุณธรรมที่ขัดแย้งกัน แล้ววิเคราะห์ผลกระทบเมื่อน้ำหนักเอียงไปข้างใดข้างหนึ่ง")

    with st.form("lab3_p10_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        pair_choice = st.selectbox(
            "เลือกคู่คุณธรรมที่ขัดแย้งกัน:",
            [
                "ความซื่อสัตย์ ↔ ความเมตตา",
                "ความยุติธรรม ↔ การให้โอกาส",
                "ความรับผิดชอบ ↔ ความสัมพันธ์",
                "การเคารพผู้ป่วย ↔ ความปลอดภัย",
                "ความเสียสละ ↔ การดูแลตนเอง",
                "อื่น ๆ"
            ]
        )
        
        loss_a = st.text_area("1. “ถ้าคุณให้ความสำคัญกับคุณธรรม A มากขึ้น คุณอาจเสียอะไร?”")
        loss_b = st.text_area("2. “ถ้าให้คุณธรรม B มากขึ้น คุณอาจเสียอะไร?”")
        
        sub_p10 = st.form_submit_button("ส่งผล Tension Map")

        if sub_p10 and group_name:
            combined_tm = f"Pair: {pair_choice} | Loss A: {loss_a} | Loss B: {loss_b}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3 - Page10 TensionMap",
                "Data": f"[{group_name}] {combined_tm}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p10:
            st.warning("กรุณากรอกชื่อกลุ่ม")


# ==========================================
# PAGE 11 — Professional Dilemma
# ==========================================
elif st.session_state.lab3_page == 11:
    st.title("💼 PAGE 11 — Professional Dilemma")
    st.markdown("### ความรับผิดชอบ vs ความเห็นอกเห็นใจ")
    st.info(
        """
        **Case: “เพื่อนร่วมงานทำงานผิดพลาด”**  
        เภสัชกรคนหนึ่งพบว่าเพื่อนร่วมงานทำงานผิดพลาดหลายครั้ง ความผิดพลาดครั้งล่าสุดอาจส่งผลต่อความปลอดภัยของผู้ป่วย เพื่อนร่วมงานยอมรับว่าเกิดจากปัญหาส่วนตัวและขอร้องว่า *“อย่าเพิ่งบอกหัวหน้าได้ไหม เรากำลังมีปัญหาครอบครัว”*
        """
    )
    st.markdown("### “คุณจะทำอย่างไร?”")

    with st.form("lab3_p11_form"):
        student_id = st.text_input("รหัสนิสิต:")
        d_choice = st.radio(
            "เลือกการตัดสินใจของคุณ:",
            [
                "A. ไม่รายงาน",
                "B. รายงานทันที",
                "C. พูดคุยกับเพื่อนก่อน",
                "D. ประเมินความเสี่ยงและดำเนินการตามความเหมาะสม",
                "E. อื่นๆ"
            ]
        )
        sub_p11 = st.form_submit_button("ส่งคำตอบ Dilemma")

        if sub_p11 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3 - Page11 Dilemma",
                "Data": f"[{student_id}] Vote: {d_choice[0]}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p11:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 ผลโหวต Professional Dilemma ทั้งห้อง")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_Responses", ttl=5)
            p11_df = df[df["Step"] == "Lab3 - Page11 Dilemma"]
            if not p11_df.empty:
                votes = p11_df["Data"].apply(lambda x: x.split("Vote: ")[1].strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
        except:
            pass


# ==========================================
# PAGE 12 — Reasoning
# ==========================================
elif st.session_state.lab3_page == 12:
    st.title("❓ PAGE 12 — Reasoning (เหตุผลเบื้องหลัง)")
    st.markdown("### เลือกคุณธรรม/หลักคิดที่สนับสนุนคำตอบของคุณ (เลือกได้หลายข้อ)")

    reas_options = [
        "Patient safety", "Responsibility", "Compassion", "Honesty",
        "Fairness", "Professional duty", "Trust", "Other"
    ]

    with st.form("lab3_p12_form"):
        student_id = st.text_input("รหัสนิสิต:")
        
        selected_reas = []
        for reas in reas_options:
            if st.checkbox(reas, key=f"l3_r_{reas}"):
                selected_reas.append(reas)
                
        reason_note = st.text_area("อธิบายเหตุผลสั้น ๆ เพิ่มเติม:")
        sub_p12 = st.form_submit_button("ส่งคำตอบ Reasoning")

        if sub_p12 and student_id:
            if len(selected_reas) > 0:
                joined_r = ", ".join(selected_reas)
                combined_re = f"Values: {joined_r} | Note: {reason_note}"
                new_data = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Step": "Lab3 - Page12 Reasoning",
                    "Data": f"[{student_id}] {combined_re}"
                }])
                if conn:
                    try:
                        existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                        updated = pd.concat([existing, new_data], ignore_index=True)
                        conn.update(worksheet="Lab3_Responses", data=updated)
                        st.success("บันทึกสำเร็จ!")
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
                else:
                    st.success("บันทึกจำลองสำเร็จ!")
            else:
                st.warning("กรุณาเลือกคุณธรรม/หลักคิดอย่างน้อย 1 ข้อ")
        elif sub_p12:
            st.warning("กรุณากรอกรหัสนิสิต")


# ==========================================
# PAGE 13 — Challenge 1
# ==========================================
elif st.session_state.lab3_page == 13:
    st.title("⚡ PAGE 13 — Challenge 1 (Severity)")
    st.info("“ความผิดพลาดยังไม่ส่งผลต่อผู้ป่วย และสามารถแก้ไขได้ทันที”")

    with st.form("lab3_p13_form"):
        student_id = st.text_input("รหัสนิสิต:")
        ch1_ans = st.radio("การตัดสินใจของคุณเปลี่ยนหรือไม่?", ["YES (เปลี่ยน)", "NO (ไม่เปลี่ยน)", "NOT SURE (ไม่แน่ใจ)"])
        ch1_why = st.text_area("เพราะอะไร:")
        sub_p13 = st.form_submit_button("ส่งผล Challenge 1")

        if sub_p13 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3 - Page13 Challenge1",
                "Data": f"[{student_id}] Ch1: {ch1_ans} | Note: {ch1_why}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p13:
            st.warning("กรุณากรอกรหัสนิสิต")


# ==========================================
# PAGE 14 — Challenge 2
# ==========================================
elif st.session_state.lab3_page == 14:
    st.title("⚡ PAGE 14 — Challenge 2 (Repeat)")
    st.info("“ความผิดพลาดเกิดขึ้นเป็นครั้งที่ 3”")

    with st.form("lab3_p14_form"):
        student_id = st.text_input("รหัสนิสิต:")
        ch2_ans = st.radio("การตัดสินใจของคุณเปลี่ยนหรือไม่?", ["YES (เปลี่ยน)", "NO (ไม่เปลี่ยน)", "NOT SURE (ไม่แน่ใจ)"])
        ch2_why = st.text_area("เพราะอะไร:")
        sub_p14 = st.form_submit_button("ส่งผล Challenge 2")

        if sub_p14 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3 - Page14 Challenge2",
                "Data": f"[{student_id}] Ch2: {ch2_ans} | Note: {ch2_why}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p14:
            st.warning("กรุณากรอกรหัสนิสิต")


# ==========================================
# PAGE 15 — Challenge 3
# ==========================================
elif st.session_state.lab3_page == 15:
    st.title("⚡ PAGE 15 — Challenge 3 (Harm Done)")
    st.info("“ผู้ป่วยได้รับอันตรายแล้ว”")
    st.markdown("### ตอนนี้คุณธรรมใดควรได้รับน้ำหนักมากที่สุด?")

    with st.form("lab3_p15_form"):
        student_id = st.text_input("รหัสนิสิต:")
        ch3_choice = st.radio(
            "เลือกคุณธรรมหลัก:",
            [
                "Patient safety",
                "Responsibility",
                "Compassion",
                "Honesty",
                "Fairness",
                "Professional duty",
                "Other"
            ]
        )
        sub_p15 = st.form_submit_button("ส่งผล Challenge 3")

        if sub_p15 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3 - Page15 Challenge3",
                "Data": f"[{student_id}] TopValue: {ch3_choice}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p15:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผลคุณธรรมที่ได้รับน้ำหนักสูงสุดเมื่อเกิดอันตราย")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_Responses", ttl=5)
            p15_df = df[df["Step"] == "Lab3 - Page15 Challenge3"]
            if not p15_df.empty:
                votes = p15_df["Data"].apply(lambda x: x.split("TopValue: ")[1].strip() if "TopValue: " in x else x)
                st.bar_chart(votes.value_counts())
        except:
            pass


# ==========================================
# PAGE 16 — Virtue Map
# ==========================================
elif st.session_state.lab3_page == 16:
    st.title("🗺️ PAGE 16 — MY PROFESSIONAL VIRTUE MAP")
    st.markdown("แต่ละกลุ่มร่วมกันสรุปแผนผังคุณธรรมทางวิชาชีพ")

    with st.form("lab3_p16_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        m_virtue = st.text_input("1. คุณธรรมหลักของกลุ่ม:")
        m_why = st.text_input("2. ทำไมสำคัญ?:")
        m_beh = st.text_input("3. พฤติกรรมที่เห็นได้:")
        m_who = st.text_input("4. ใครได้รับประโยชน์?:")
        m_conf = st.text_input("5. ถ้าขัดแย้งกับคุณธรรมอื่น จะทำอย่างไร?:")
        m_dev = st.text_input("6. ฉันต้องพัฒนาตัวเองอย่างไร?:")
        
        sub_p16 = st.form_submit_button("ส่ง Virtue Map ของกลุ่ม")

        if sub_p16 and group_name:
            combined_vm = f"Virtue:{m_virtue}|Why:{m_why}|Beh:{m_beh}|Who:{m_who}|Conf:{m_conf}|Dev:{m_dev}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3 - Page16 VirtueMap",
                "Data": f"[{group_name}] {combined_vm}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p16:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดง Virtue Map ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_Responses", ttl=5)
            p16_df = df[df["Step"] == "Lab3 - Page16 VirtueMap"]
            if not p16_df.empty:
                st.dataframe(p16_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# PAGE 17 — Peer Challenge
# ==========================================
elif st.session_state.lab3_page == 17:
    st.title("⚔️ PAGE 17 — Peer Challenge")
    st.markdown("ดู Virtue Map ของกลุ่มอื่น ๆ แล้วร่วมสะท้อนมุมมอง")

    with st.form("lab3_p17_form"):
        group_name = st.text_input("ชื่อกลุ่มของคุณ:")
        target_group = st.text_input("กลุ่มที่คุณเลือกดูและต้องการคอมเมนต์:")
        
        diff_ans = st.text_area("1. “อะไรในคำตอบของกลุ่มนี้ที่ทำให้คุณคิดต่างหรือคิดเพิ่ม?”")
        quest_ans = st.text_area("2. “คุณมีคำถามอะไรกับกลุ่มนี้?”")
        
        sub_p17 = st.form_submit_button("ส่ง Peer Challenge")

        if sub_p17 and group_name and target_group:
            combined_pc = f"Target: {target_group} | ThinkDiff: {diff_ans} | Question: {quest_ans}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3 - Page17 PeerChallenge",
                "Data": f"[{group_name}] {combined_pc}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p17:
            st.warning("กรุณากรอกชื่อกลุ่มและกลุ่มเป้าหมาย")

    st.markdown("---")
    st.subheader("📋 ตารางรายการ Peer Challenge ทั้งหมด")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_Responses", ttl=5)
            p17_df = df[df["Step"] == "Lab3 - Page17 PeerChallenge"]
            if not p17_df.empty:
                st.dataframe(p17_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# PAGE 18 — Professional Identity
# ==========================================
elif st.session_state.lab3_page == 18:
    st.title("🎯 PAGE 18 — Professional Identity (Exit Reflection)")
    st.markdown("### Final Question")
    st.info(
        "“ถ้าวันหนึ่งคุณเป็นเภสัชกร และคนไข้/เพื่อนร่วมงาน/สังคมต้องอธิบายว่าคุณเป็นเภสัชกรแบบไหน คุณอยากให้เขาพูดถึงคุณว่าอย่างไร?”"
    )

    with st.form("lab3_p18_form"):
        student_id = st.text_input("รหัสนิสิต (ระบุหรือไม่ระบุก็ได้):")
        
        id_statement = st.text_input("“ฉันอยากเป็นเภสัชกรที่...”")
        virtue_dev = st.text_input("“และคุณธรรมหนึ่งอย่างที่ฉันต้องพัฒนาต่อคือ...”")
        dev_reason = st.text_area("เพราะอะไร:")
        
        sub_p18 = st.form_submit_button("ส่ง Professional Identity")

        if sub_p18 and student_id:
            sid_val = "Anonymous" if not student_id else student_id
            combined_pi = f"Statement: {id_statement} | NeedDev: {virtue_dev} | Reason: {dev_reason}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab3 - Exit Professional Identity",
                "Data": f"[{sid_val}] {combined_pi}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab3_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab3_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p18:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📋 ตารางรวบรวม Professional Identity ของนิสิต")
    if conn:
        try:
            df = conn.read(worksheet="Lab3_Responses", ttl=5)
            p18_df = df[df["Step"] == "Lab3 - Exit Professional Identity"]
            if not p18_df.empty:
                st.dataframe(p18_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass