from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 4: Ethical Lens & Case Conference",
    page_icon="🎬",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab4_step" not in st.session_state:
    st.session_state.lab4_step = 1

# --- Sidebar เมนูด้านซ้าย (แบ่งเป็น LAB 4.1 และ LAB 4.2 ชัดเจน) ---
st.sidebar.markdown("### 🎬 LAB 4 Workflow")

st.sidebar.markdown("---")
st.sidebar.markdown("**-- LAB 4.1 --**")
step_1_btn = st.sidebar.button("Activity 1: Ethical Lens")
step_2_btn = st.sidebar.button("Activity 2: Watch the Case")

st.sidebar.markdown("---")
st.sidebar.markdown("**-- LAB 4.2 --**")
step_3_btn = st.sidebar.button("Activity 3: Case Conference")
step_4_btn = st.sidebar.button("Activity 4: Change Conditions")
step_5_btn = st.sidebar.button("Activity 5: Final Challenge")

# จัดการการเปลี่ยนหน้าผ่าน Sidebar Buttons
if step_1_btn:
    st.session_state.lab4_step = 1
elif step_2_btn:
    st.session_state.lab4_step = 2
elif step_3_btn:
    st.session_state.lab4_step = 3
elif step_4_btn:
    st.session_state.lab4_step = 4
elif step_5_btn:
    st.session_state.lab4_step = 5

st.sidebar.markdown("---")
st.sidebar.info(f"📍 กำลังแสดงผล: ช่วง LAB 4.{'1' if st.session_state.lab4_step in [1,2] else '2'}")


# ==========================================
# LAB 4.1: Activity 1 — Ethical Lens
# ==========================================
if st.session_state.lab4_step == 1:
    st.title("👓 LAB 4.1 — Activity 1: Ethical Lens")
    st.markdown("### “ถ้าคุณเห็นเหตุการณ์หนึ่งที่ดูเหมือนผิดจริยธรรม คุณจะดูอะไรเป็นอันดับแรก?”")
    st.info("💡 กรุณาเลือก **2 ข้อ** ที่คุณให้ความสำคัญที่สุด")

    lens_options = [
        "การกระทำ",
        "เจตนา",
        "ผลกระทบ",
        "ผู้ได้รับผลกระทบ",
        "กฎ/กฎหมาย",
        "คุณค่าที่เกี่ยวข้อง",
        "ความรับผิดชอบของผู้ประกอบวิชาชีพ"
    ]

    with st.form("lab4_1_act1_form"):
        student_id = st.text_input("รหัสนิสิต:")
        selected_choices = st.multiselect("เลือก 2 ข้อ:", lens_options, max_selections=2)
        sub_a1 = st.form_submit_button("ส่งคำตอบ Ethical Lens")

        if sub_a1 and student_id:
            if len(selected_choices) == 2:
                combined_choices = " + ".join(selected_choices)
                new_data = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Step": "Lab4.1 - Act 1 Ethical Lens",
                    "Data": f"[{student_id}] {combined_choices}"
                }])
                if conn:
                    try:
                        existing = conn.read(worksheet="Lab4_1_Responses", ttl=0)
                        updated = pd.concat([existing, new_data], ignore_index=True)
                        conn.update(worksheet="Lab4_1_Responses", data=updated)
                        st.success("บันทึกสำเร็จ!")
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
                else:
                    st.success("บันทึกจำลองสำเร็จ!")
            else:
                st.warning("กรุณาเลือกให้ครบถ้วนพอดี 2 ข้อ")
        elif sub_a1:
            st.warning("กรุณากรอกรหัสนิสิตและเลือกคำตอบ")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผล Vote (Ethical Lens)")
    if conn:
        try:
            df = conn.read(worksheet="Lab4_1_Responses", ttl=5)
            act1_df = df[df["Step"] == "Lab4.1 - Act 1 Ethical Lens"]
            if not act1_df.empty:
                all_selections = []
                for item in act1_df["Data"]:
                    if "]" in item:
                        choices_part = item.split("] ")[1]
                        all_selections.extend(choices_part.split(" + "))
                if all_selections:
                    st.bar_chart(pd.Series(all_selections).value_counts())
        except:
            pass


# ==========================================
# LAB 4.1: Activity 2 — Watch the Case
# ==========================================
elif st.session_state.lab4_step == 2:
    st.title("🎬 LAB 4.1 — Activity 2: Watch the Case (Ethical Case Card)")
    st.markdown("ระหว่างดูหนัง/คลิป ให้แต่ละกลุ่มร่วมกันวิเคราะห์ตามประเด็นด้านล่างนี้")

    with st.form("lab4_1_act2_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        c_a = st.text_area("A. What happened? (เกิดอะไรขึ้น?)")
        c_b = st.text_area("B. Who is affected? (ใครได้รับผลกระทบ?)")
        c_c = st.text_area("C. What is the ethical issue? (ปัญหาจริยธรรมคืออะไร?)")
        c_d = st.text_area("D. What values are involved? (มีคุณค่าหรือหลักจริยธรรมอะไรเกี่ยวข้อง?)")
        c_e = st.text_area("E. What should the person do? (ควรทำอย่างไร?)")
        sub_a2 = st.form_submit_button("ส่งคำตอบ Case Card")

        if sub_a2 and group_name:
            combined_case = f"A: {c_a} | B: {c_b} | C: {c_c} | D: {c_d} | E: {c_e}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab4.1 - Act 2 Case Card",
                "Data": f"[{group_name}] {combined_case}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab4_1_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab4_1_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a2:
            st.warning("กรุณาระบุชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Case Card ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab4_1_Responses", ttl=5)
            p2_df = df[df["Step"] == "Lab4.1 - Act 2 Case Card"]
            if not p2_df.empty:
                st.dataframe(p2_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# LAB 4.2: Activity 3 — Ethical Case Conference
# ==========================================
elif st.session_state.lab4_step == 3:
    st.title("🏛️ LAB 4.2 — Ethical Case Conference")
    st.markdown("เลือก 1 Ethical Turning Point (ช่วงเวลาที่ต้องตัดสินใจ) แล้ววิเคราะห์ด้วยกรอบ Lab 2")

    with st.form("lab4_2_act3_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        s1 = st.text_area("1. Situation: เกิดอะไรขึ้นในจุดเปลี่ยนนี้?")
        s2 = st.text_area("2. Stakeholders: ใครเกี่ยวข้องบ้าง?")
        s3 = st.text_area("3. Ethical tension: คุณค่าอะไรกำลังขัดแย้งกัน?")
        s4 = st.text_area("4. Options: มีทางเลือกอะไรบ้าง?")
        s5 = st.text_area("5. Consequences: แต่ละทางเลือกมีผลอย่างไร?")
        s6 = st.text_area("6. Decision: กลุ่มเลือกทางไหน?")
        s7 = st.text_area("7. Justification: ทำไมจึงเลือกทางนั้น?")
        
        sub_a3 = st.form_submit_button("ส่งผล Case Conference")

        if sub_a3 and group_name:
            combined_conf = f"Sit: {s1} | Stake: {s2} | Tension: {s3} | Opt: {s4} | Cons: {s5} | Dec: {s6} | Just: {s7}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab4.2 - Act 3 Conference",
                "Data": f"[{group_name}] {combined_conf}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab4_2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab4_2_Responses", data=updated)
                    st.success("บันทึก Case Conference สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a3:
            st.warning("กรุณาระบุชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางสรุป Ethical Case Conference ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab4_2_Responses", ttl=5)
            p3_df = df[df["Step"] == "Lab4.2 - Act 3 Conference"]
            if not p3_df.empty:
                st.dataframe(p3_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# LAB 4.2: Activity 4 — Change Conditions
# ==========================================
elif st.session_state.lab4_step == 4:
    st.title("🔄 LAB 4.2 — Activity 4: Change Conditions")
    st.markdown("ทดสอบเปลี่ยนเงื่อนไขสถานการณ์ แล้วดูว่าการตัดสินใจจะเปลี่ยนไปหรือไม่")

    with st.form("lab4_2_act4_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        condition_type = st.selectbox(
            "เลือกเงื่อนไขที่เปลี่ยน:",
            [
                "เงื่อนไขที่ 1: ถ้าการตัดสินใจนั้นไม่ส่งผลเสียต่อผู้ป่วย แต่ส่งผลต่อเพื่อนร่วมงาน",
                "เงื่อนไขที่ 2: ถ้าคนที่กระทำผิดเป็นหัวหน้าของคุณ",
                "เงื่อนไขที่ 3: ถ้าการรายงานเหตุการณ์ทำให้เพื่อนร่วมงานเสียโอกาสทางอาชีพ"
            ]
        )
        vote_change = st.radio("คำตอบของกลุ่มยังเหมือนเดิมหรือไม่?", ["เหมือนเดิม", "ไม่เหมือนเดิม", "ไม่แน่ใจ"])
        reason_text = st.text_area("เพราะอะไร (โปรดอธิบายเหตุผล):")
        
        sub_a4 = st.form_submit_button("ส่งคำตอบ Change Conditions")

        if sub_a4 and group_name:
            cond_tag = condition_type.split(":")[0]
            combined_cond = f"Cond: {cond_tag} | Vote: {vote_change} | Reason: {reason_text}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab4.2 - Act 4 Change Conditions",
                "Data": f"[{group_name}] {combined_cond}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab4_2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab4_2_Responses", data=updated)
                    st.success("บันทึกข้อมูลสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a4:
            st.warning("กรุณาระบุชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Change Conditions ของกลุ่มต่างๆ")
    if conn:
        try:
            df = conn.read(worksheet="Lab4_2_Responses", ttl=5)
            p4_df = df[df["Step"] == "Lab4.2 - Act 4 Change Conditions"]
            if not p4_df.empty:
                st.dataframe(p4_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# LAB 4.2: Activity 5 — Final Challenge
# ==========================================
elif st.session_state.lab4_step == 5:
    st.title("🎯 LAB 4.2 — Final Challenge")
    st.markdown("### “การทำสิ่งที่ถูกต้องทางจริยธรรม ทำไมบางครั้งจึงทำได้ยาก?”")

    obstacle_options = [
        "ความสัมพันธ์กับคนอื่น",
        "อำนาจ/ลำดับชั้น",
        "ผลประโยชน์",
        "ความกลัว",
        "ความไม่แน่ใจ",
        "กฎที่ไม่ชัดเจน",
        "ความแตกต่างของค่านิยม"
    ]

    with st.form("lab4_2_act5_form"):
        student_id = st.text_input("รหัสนิสิต:")
        selected_obstacle = st.selectbox("เลือกอุปสรรคสำคัญที่สุด:", obstacle_options)
        discussion_comment = st.text_area("ความเห็นเพิ่มเติม (Discussion):")
        
        sub_a5 = st.form_submit_button("ส่งโหวต Final Challenge")

        if sub_a5 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab4.2 - Act 5 Final Challenge",
                "Data": f"[{student_id}] Obstacle: {selected_obstacle} | Comment: {discussion_comment}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab4_2_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab4_2_Responses", data=updated)
                    st.success("บันทึกโหวตสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_a5:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 กราฟแสดงผล Vote อุปสรรคทางจริยธรรม (Final Challenge)")
    if conn:
        try:
            df = conn.read(worksheet="Lab4_2_Responses", ttl=5)
            act5_df = df[df["Step"] == "Lab4.2 - Act 5 Final Challenge"]
            if not act5_df.empty:
                obstacles = act5_df["Data"].apply(lambda x: x.split("|")[0].replace("Obstacle: ", "").strip() if "Obstacle: " in x else x)
                st.bar_chart(obstacles.value_counts())
        except:
            pass