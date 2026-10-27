from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Ethics Lab 4: Ethical Courage & Authority",
    page_icon="🛡️",
    layout="wide",
)

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# --- กำหนดค่าเริ่มต้นใน Session State ---
if "lab4_page" not in st.session_state:
    st.session_state.lab4_page = 1

# --- Sidebar เมนูด้านซ้าย (14 หน้า) ---
st.sidebar.markdown("### 🛡️ LAB 4 Workflow")

pages_name = {
    1: "Page 1 — Welcome",
    2: "Page 2 — Connect",
    3: "Page 3 — Initial Vote",
    4: "Page 4 — Watch the Clip",
    5: "Page 5 — Ethical Turning Point",
    6: "Page 6 — Stakeholder Map",
    7: "Page 7 — Ethical Tension Map",
    8: "Page 8 — Evaluate the Options",
    9: "Page 9 — Group Decision",
    10: "Page 10 — Challenge (New Info)",
    11: "Page 11 — Re-vote (Before vs After)",
    12: "Page 12 — Whole-class Debrief",
    13: "Page 13 — Transfer to Pharmacy",
    14: "Page 14 — Exit Reflection",
}

current_index = list(pages_name.keys()).index(st.session_state.lab4_page)

selected_page_name = st.sidebar.radio(
    "เลือกหน้า LAB 4:",
    list(pages_name.values()),
    index=current_index,
    key="lab4_menu_selection",
)

for p_num, p_title in pages_name.items():
    if p_title == selected_page_name:
        st.session_state.lab4_page = p_num

st.sidebar.markdown("---")
st.sidebar.info("💡 เลือกหัวข้อด้านบนเพื่อเปลี่ยนหน้ากิจกรรม")


# ==========================================
# Page 1 — Welcome
# ==========================================
if st.session_state.lab4_page == 1:
    st.title("🛡️ Lab 4: ความกล้าหาญในการยืนหยัดในสิ่งที่ถูกต้อง")
    st.markdown("### Ethical Courage & Authority Dilemma")
    st.markdown("---")
    st.info(
        """
        ### 📌 ข้อความนำ:
        “วันนี้เราไม่ได้ฝึกเพียงการแยกแยะถูก–ผิด แต่ฝึกคิดว่าจะทำอย่างไรเมื่อการทำสิ่งที่ถูกต้องไม่ใช่เรื่องง่าย”
        """
    )


# ==========================================
# Page 2 — Connect
# ==========================================
elif st.session_state.lab4_page == 2:
    st.title("🌉 Page 2 — Connect")
    st.markdown("### ชวนคิดก่อนเข้าสู่บทเรียน")
    st.warning("“ถ้าคุณพบว่าผู้มีอำนาจกำลังทำสิ่งที่ไม่ถูกต้อง คุณคิดว่าการทักท้วงเป็นสิ่งที่ควรทำเสมอหรือไม่?”")

    with st.form("lab4_p2_form"):
        student_id = st.text_input("รหัสนิสิต:")
        connect_choice = st.radio(
            "เลือกมุมมองของคุณ:",
            [
                "ควรทักท้วงทันที",
                "ควรตรวจสอบข้อเท็จจริงก่อน",
                "ขึ้นอยู่กับสถานการณ์",
                "ยังไม่แน่ใจ"
            ]
        )
        sub_p2 = st.form_submit_button("ส่งคำตอบ Connect")

        if sub_p2 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab4 - Page2 Connect",
                "Data": f"[{student_id}] Choice: {connect_choice}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab4_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab4_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p2:
            st.warning("กรุณากรอกรหัสนิสิต")


# ==========================================
# Page 3 — Initial Vote
# ==========================================
elif st.session_state.lab4_page == 3:
    st.title("🗳️ Page 3 — Initial Vote")
    st.info(
        """
        **สถานการณ์สมมติ:**  
        “คุณพบพฤติกรรมที่อาจไม่ถูกต้องของผู้บังคับบัญชา แต่ยังไม่แน่ใจในข้อเท็จจริงทั้งหมด คุณจะทำอย่างไรเป็นอันดับแรก?”
        """
    )

    with st.form("lab4_p3_form"):
        student_id = st.text_input("รหัสนิสิต:")
        init_vote = st.radio(
            "เลือกแนวทาง (Initial Vote - ไม่ระบุตัวบุคคลบนจอรวม):",
            [
                "A. ทักท้วงทันทีต่อหน้าผู้อื่น",
                "B. ตรวจสอบข้อเท็จจริงเพิ่มเติมก่อน",
                "C. พูดคุยกับผู้เกี่ยวข้องเป็นการส่วนตัว",
                "D. ขอคำปรึกษาจากบุคคลหรือช่องทางที่เหมาะสม",
                "E. ยังไม่ดำเนินการ เพราะกังวลผลกระทบต่อตนเอง",
                "F. อื่น ๆ"
            ]
        )
        reason_f = st.text_input("ระบุเหตุผลเพิ่มเติม (กรณีเลือก F หรืออื่น ๆ):")
        
        sub_p3 = st.form_submit_button("ส่ง Initial Vote")

        if sub_p3 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab4 - Page3 InitialVote",
                "Data": f"[{student_id}] Vote: {init_vote[0]} | Note: {reason_f}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab4_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab4_Responses", data=updated)
                    st.success("บันทึก Initial Vote สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p3:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 ผลโหวต Initial Vote ภาพรวมห้อง")
    if conn:
        try:
            df = conn.read(worksheet="Lab4_Responses", ttl=5)
            p3_df = df[df["Step"] == "Lab4 - Page3 InitialVote"]
            if not p3_df.empty:
                votes = p3_df["Data"].apply(lambda x: x.split("Vote: ")[1].split(" |")[0].strip() if "Vote: " in x else x)
                st.bar_chart(votes.value_counts())
        except:
            pass


# ==========================================
# Page 4 — Watch the Clip
# ==========================================
elif st.session_state.lab4_page == 4:
    st.title("🎬 Page 4 — Watch the Clip")
    st.markdown("### 🎥 กรณีศึกษา / คลิปวิดีโอสถานการณ์ปัญหา")
    st.markdown("[🔗 คลิกที่นี่เพื่อเปิดลิงก์คลิปวิดีโอในแท็บใหม่](https://youtu.be/HdDrMe52xxs?utm_source=chatgpt.com)", unsafe_allow_html=True)
    
    st.info(
        """
        **คำแนะนำระหว่างรับชม:**  
        “ระหว่างดู ให้สังเกตเหตุการณ์สำคัญ ผู้มีส่วนได้เสีย และจุดที่ตัวละครต้องตัดสินใจ”  
        - เกิดอะไรขึ้น?  
        - ใครได้รับผลกระทบ?  
        - ตัวละครต้องตัดสินใจเรื่องใด?  
        - มีแรงกดดันหรือความเสี่ยงอะไรบ้าง?
        """
    )


# ==========================================
# Page 5 — Ethical Turning Point
# ==========================================
elif st.session_state.lab4_page == 5:
    st.title("🔍 Page 5 — Ethical Turning Point")
    st.markdown("ระบุเหตุการณ์จุดเปลี่ยนสำคัญ แยกข้อเท็จจริงออกจากการตีความ")

    with st.form("lab4_p5_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม (เช่น กลุ่ม 1):")
        
        tp1 = st.text_area("1. เหตุการณ์ใดคือจุดเปลี่ยนสำคัญในคลิป?")
        tp2 = st.text_area("2. ข้อเท็จจริงที่ปรากฏชัดเจนคืออะไร?")
        tp3 = st.text_area("3. มีข้อมูลหรือข้อสงสัยใดที่ยังไม่ทราบและต้องตรวจสอบเพิ่ม?")
        
        sub_p5 = st.form_submit_button("ส่งผล Turning Point")

        if sub_p5 and group_name:
            combined_tp = f"TurningPoint: {tp1} | Facts: {tp2} | Unknowns: {tp3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab4 - Page5 TurningPoint",
                "Data": f"[{group_name}] {combined_tp}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab4_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab4_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p5:
            st.warning("กรุณากรอกชื่อกลุ่ม")


# ==========================================
# Page 6 — Stakeholder Map
# ==========================================
elif st.session_state.lab4_page == 6:
    st.title("👥 Page 6 — Stakeholder Map")
    st.markdown("ระบุผู้มีส่วนได้เสียและผลกระทบที่อาจเกิดขึ้น")

    with st.form("lab4_p6_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        sh1 = st.text_input("ผู้ที่พบพฤติกรรมไม่เหมาะสม:")
        sh2 = st.text_input("ผู้มีอำนาจตัดสินใจ / ผู้ถูกพาดพิง:")
        sh3 = st.text_input("ผู้ได้รับผลกระทบโดยตรง:")
        sh4 = st.text_input("องค์กรหรือสังคม:")
        sh_other = st.text_area("ผู้มีส่วนได้เสียอื่น ๆ เพิ่มเติม (ถ้ามี):")
        
        sub_p6 = st.form_submit_button("ส่ง Stakeholder Map")

        if sub_p6 and group_name:
            combined_sh = f"Observer: {sh1} | Authority: {sh2} | DirectVictim: {sh3} | Org: {sh4} | Other: {sh_other}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab4 - Page6 Stakeholders",
                "Data": f"[{group_name}] {combined_sh}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab4_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab4_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p6:
            st.warning("กรุณากรอกชื่อกลุ่ม")


# ==========================================
# Page 7 — Ethical Tension Map
# ==========================================
elif st.session_state.lab4_page == 7:
    st.title("🗺️ Page 7 — Ethical Tension Map")
    st.markdown("เลือกคุณค่าหรือหน้าที่ที่เกี่ยวข้อง และวิเคราะห์ความขัดแย้ง")

    values_list = [
        "ความซื่อสัตย์", "ความรับผิดชอบ", "ความเป็นธรรม",
        "ประโยชน์ส่วนรวม", "ความสัมพันธ์ในองค์กร", "ความปลอดภัย",
        "การเคารพข้อกำหนดและมาตรฐาน"
    ]

    with st.form("lab4_p7_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        selected_vals = []
        st.markdown("เลือกคุณค่าที่เกี่ยวข้อง (เลือกได้หลายข้อ):")
        for v in values_list:
            if st.checkbox(v, key=f"l4_v_{v}"):
                selected_vals.append(v)
                
        tension_q = st.text_area("“คุณค่าใดขัดแย้งกัน และเหตุใดจึงขัดแย้งกันในสถานการณ์นี้?”")
        
        sub_p7 = st.form_submit_button("ส่ง Ethical Tension Map")

        if sub_p7 and group_name:
            if len(selected_vals) > 0:
                joined_v = ", ".join(selected_vals)
                combined_tm = f"Values: {joined_v} | Tension: {tension_q}"
                new_data = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Step": "Lab4 - Page7 TensionMap",
                    "Data": f"[{group_name}] {combined_tm}"
                }])
                if conn:
                    try:
                        existing = conn.read(worksheet="Lab4_Responses", ttl=0)
                        updated = pd.concat([existing, new_data], ignore_index=True)
                        conn.update(worksheet="Lab4_Responses", data=updated)
                        st.success("บันทึกสำเร็จ!")
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
                else:
                    st.success("บันทึกจำลองสำเร็จ!")
            else:
                st.warning("กรุณาเลือกคุณค่าอย่างน้อย 1 ข้อ")
        elif sub_p7:
            st.warning("กรุณากรอกชื่อกลุ่ม")


# ==========================================
# Page 8 — Evaluate the Options
# ==========================================
elif st.session_state.lab4_page == 8:
    st.title("⚖️ Page 8 — Evaluate the Options")
    st.markdown("นำเสนอทางเลือกอย่างน้อย 2 ทางเลือก (ไม่จำกัดว่าต้องเผชิญหน้าตรง ๆ)")

    with st.form("lab4_p8_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        st.markdown("#### **ทางเลือกที่ 1:**")
        opt1_act = st.text_input("การดำเนินการ (Opt 1):")
        opt1_pros = st.text_input("ผลดี (Opt 1):")
        opt1_cons = st.text_input("ผลเสียหรือความเสี่ยง (Opt 1):")
        opt1_mit = st.text_input("วิธีลดความเสี่ยง (Opt 1):")
        
        st.markdown("---")
        st.markdown("#### **ทางเลือกที่ 2:**")
        opt2_act = st.text_input("การดำเนินการ (Opt 2):")
        opt2_pros = st.text_input("ผลดี (Opt 2):")
        opt2_cons = st.text_input("ผลเสียหรือความเสี่ยง (Opt 2):")
        opt2_mit = st.text_input("วิธีลดความเสี่ยง (Opt 2):")
        
        sub_p8 = st.form_submit_button("ส่งทางเลือกทั้งหมด")

        if sub_p8 and group_name:
            combined_opts = f"Opt1: {opt1_act} (+{opt1_pros}/-{opt1_cons}/Mit:{opt1_mit}) || Opt2: {opt2_act} (+{opt2_pros}/-{opt2_cons}/Mit:{opt2_mit})"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab4 - Page8 Options",
                "Data": f"[{group_name}] {combined_opts}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab4_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab4_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p8:
            st.warning("กรุณากรอกชื่อกลุ่ม")


# ==========================================
# Page 9 — Group Decision
# ==========================================
elif st.session_state.lab4_page == 9:
    st.title("🎯 Page 9 — Group Decision")
    st.markdown("### “จากข้อมูลที่มีอยู่ กลุ่มของคุณเลือกแนวทางใด และเพราะเหตุใด?”")

    with st.form("lab4_p9_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        decision_summary = st.text_area("ข้อสรุปการตัดสินใจและเหตุผลสนับสนุน:")
        sub_p9 = st.form_submit_button("ส่งการตัดสินใจของกลุ่ม")

        if sub_p9 and group_name and decision_summary:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab4 - Page9 Decision",
                "Data": f"[{group_name}] {decision_summary}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab4_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab4_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p9:
            st.warning("กรุณากรอกชื่อกลุ่มและคำตอบ")

    st.markdown("---")
    st.subheader("📋 ตารางสรุปการตัดสินใจของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab4_Responses", ttl=5)
            p9_df = df[df["Step"] == "Lab4 - Page9 Decision"]
            if not p9_df.empty:
                st.dataframe(p9_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# Page 10 — Challenge: New Information
# ==========================================
elif st.session_state.lab4_page == 10:
    st.title("⚡ Page 10 — Challenge: New Information")
    st.info(
        """
        **ข้อมูลใหม่ / แรงกดดันเพิ่มเติม:**  
        - *“หากคุณเป็นผู้ใต้บังคับบัญชาที่พบพฤติกรรมดังกล่าว และผู้บังคับบัญชามีอำนาจประเมินผลงานของคุณ คุณจะดำเนินการอย่างไร?”*  
        - *“หากคุณยังไม่มีหลักฐานเพียงพอที่จะสรุปว่ามีการกระทำผิด คุณจะทำอย่างไรเพื่อรักษาความถูกต้องและลดความเสี่ยงต่อผู้เกี่ยวข้อง?”*
        """
    )

    with st.form("lab4_p10_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        ch_shift = st.radio("ข้อมูลใหม่นี้ทำให้กลุ่มเปลี่ยนแนวทางหรือไม่?", ["เปลี่ยนแนวทาง", "ไม่เปลี่ยนแนวทาง", "ปรับเปลี่ยนวิธีการดำเนินการ"])
        ch_why = st.text_area("เพราะเหตุใด (อธิบายผลกระทบของข้อมูลใหม่):")
        
        sub_p10 = st.form_submit_button("ส่งผล Challenge")

        if sub_p10 and group_name:
            combined_ch = f"Shift: {ch_shift} | Reason: {ch_why}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab4 - Page10 Challenge",
                "Data": f"[{group_name}] {combined_ch}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab4_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab4_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p10:
            st.warning("กรุณากรอกชื่อกลุ่ม")


# ==========================================
# Page 11 — Re-vote
# ==========================================
elif st.session_state.lab4_page == 11:
    st.title("🔄 Page 11 — Re-vote (Before vs After)")
    st.markdown("### โหวตอีกครั้งเพื่อเปรียบเทียบการเปลี่ยนแปลงหลังผ่านกระบวนการวิเคราะห์และ Challenge")

    with st.form("lab4_p11_form"):
        student_id = st.text_input("รหัสนิสิต:")
        revote_choice = st.radio(
            "เลือกแนวทางอีกครั้ง:",
            [
                "A. ทักท้วงทันทีต่อหน้าผู้อื่น",
                "B. ตรวจสอบข้อเท็จจริงเพิ่มเติมก่อน",
                "C. พูดคุยกับผู้เกี่ยวข้องเป็นการส่วนตัว",
                "D. ขอคำปรึกษาจากบุคคลหรือช่องทางที่เหมาะสม",
                "E. ยังไม่ดำเนินการ เพราะกังวลผลกระทบต่อตนเอง",
                "F. อื่น ๆ"
            ]
        )
        revote_note = st.text_area("เหตุผลประกอบการตัดสินใจ (หากมีการเปลี่ยนใจ หรือเหตุผลที่ยืนยันคำเดิม):")
        
        sub_p11 = st.form_submit_button("ส่ง Re-vote")

        if sub_p11 and student_id:
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab4 - Page11 ReVote",
                "Data": f"[{student_id}] After: {revote_choice[0]} | Note: {revote_note}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab4_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab4_Responses", data=updated)
                    st.success("บันทึก Re-vote สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p11:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.subheader("📊 เปรียบเทียบผลโหวต Before (Page 3) vs After (Page 11)")
    if conn:
        try:
            df = conn.read(worksheet="Lab4_Responses", ttl=5)
            
            c_b, c_a = st.columns(2)
            with c_b:
                st.markdown("**Initial Vote (Page 3)**")
                b_df = df[df["Step"] == "Lab4 - Page3 InitialVote"]
                if not b_df.empty:
                    vb = b_df["Data"].apply(lambda x: x.split("Vote: ")[1].split(" |")[0].strip() if "Vote: " in x else x)
                    st.bar_chart(vb.value_counts())
                else:
                    st.info("ยังไม่มีข้อมูล Initial")
            
            with c_a:
                st.markdown("**Re-vote (Page 11)**")
                a_df = df[df["Step"] == "Lab4 - Page11 ReVote"]
                if not a_df.empty:
                    va = a_df["Data"].apply(lambda x: x.split("After: ")[1].split(" |")[0].strip() if "After: " in x else x)
                    st.bar_chart(va.value_counts())
                else:
                    st.info("ยังไม่มีข้อมูล Re-vote")
        except:
            pass


# ==========================================
# Page 12 — Whole-class Debrief
# ==========================================
elif st.session_state.lab4_page == 12:
    st.title("🗣️ Page 12 — Whole-class Debrief")
    st.markdown("อภิปรายร่วมกันทั้งห้องโดยเน้นประเด็นสำคัญ:")

    st.markdown(
        """
        - **เหตุผลใดมีน้ำหนักมากที่สุดในการตัดสินใจ?**  
        - **มีข้อจำกัดอะไรในแต่ละทางเลือก?**  
        - **ข้อมูลใดที่ควรตรวจสอบก่อนดำเนินการจริง?**  
        """
    )
    st.info("📌 ผู้สอนเลือกกลุ่มที่มีความเห็นต่างหรือน่าสนใจมานำเสนอร่วมกันในขั้นตอนนี้")


# ==========================================
# Page 13 — Transfer to Pharmacy
# ==========================================
elif st.session_state.lab4_page == 13:
    st.title("💊 Page 13 — Transfer to Pharmacy")
    st.info(
        """
        **สถานการณ์ประยุกต์:**  
        “คุณเป็นเภสัชกรในโรงพยาบาล และพบว่าผู้บังคับบัญชาขอให้ดำเนินการบางอย่างที่คุณเห็นว่าอาจไม่เหมาะสมกับความปลอดภัยของผู้ป่วยหรือมาตรฐานวิชาชีพ แต่คุณยังต้องตรวจสอบข้อเท็จจริงและข้อกำหนดที่เกี่ยวข้อง”
        """
    )
    st.markdown("ตอบตามกรอบมาตรฐาน:")

    with st.form("lab4_p13_form"):
        group_name = st.text_input("ชื่อกลุ่ม / เลขที่กลุ่ม:")
        
        t1 = st.text_input("1. FACTS (ต้องตรวจสอบข้อเท็จจริงอะไรบ้าง):")
        t2 = st.text_input("2. STAKEHOLDERS (ใครได้รับผลกระทบ):")
        t3 = st.text_input("3. ETHICAL ISSUE / DUTIES (มีหน้าที่/ความรับผิดชอบใดขัดแย้งกัน):")
        t4 = st.text_input("4. OPTIONS (มีทางเลือกใดบ้าง):")
        t5 = st.text_input("5. CONSEQUENCES (ผลดี-ผลเสียแต่ละทางเลือก):")
        t6 = st.text_input("6. DECISION (คุณจะดำเนินการอย่างไร):")
        t7 = st.text_area("7. JUSTIFICATION (เหตุผลสนับสนุน):")
        
        sub_p13 = st.form_submit_button("ส่งผล Transfer to Pharmacy")

        if sub_p13 and group_name:
            combined_tr = f"Facts:{t1}|Stake:{t2}|Issue:{t3}|Opt:{t4}|Cons:{t5}|Dec:{t6}|Just:{t7}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab4 - Page13 Transfer",
                "Data": f"[{group_name}] {combined_tr}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab4_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab4_Responses", data=updated)
                    st.success("บันทึกสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_p13:
            st.warning("กรุณากรอกชื่อกลุ่ม")

    st.markdown("---")
    st.subheader("📋 ตารางแสดงผล Transfer to Pharmacy ของแต่ละกลุ่ม")
    if conn:
        try:
            df = conn.read(worksheet="Lab4_Responses", ttl=5)
            p13_df = df[df["Step"] == "Lab4 - Page13 Transfer"]
            if not p13_df.empty:
                st.dataframe(p13_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass


# ==========================================
# Page 14 — Exit Reflection
# ==========================================
elif st.session_state.lab4_page == 14:
    st.title("🎯 Page 14 — Exit Reflection")
    st.markdown("ตอบรายบุคคล (ส่งท้าย Lab 4)")

    with st.form("lab4_p14_form"):
        student_id = st.text_input("รหัสนิสิต (ระบุหรือไม่ระบุก็ได้):")
        
        r1 = st.text_area("1. วันนี้ฉันได้เรียนรู้อะไรเกี่ยวกับการตัดสินใจทางจริยธรรม?")
        r2 = st.text_area("2. มีเหตุผลหรือข้อมูลใดที่ทำให้ฉันทบทวนความคิดเดิม?")
        r3 = st.text_area("3. หากพบสถานการณ์คล้ายกันในวิชาชีพ ฉันจะเตรียมตัวอย่างไร?")
        
        sub_ref = st.form_submit_button("ส่ง Exit Reflection Lab 4")

        if sub_ref and student_id:
            sid_val = "Anonymous" if not student_id else student_id
            combined_ref = f"Learned: {r1} | Reviewed: {r2} | Prepare: {r3}"
            new_data = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Step": "Lab4 - Exit Reflection",
                "Data": f"[{sid_val}] {combined_ref}"
            }])
            if conn:
                try:
                    existing = conn.read(worksheet="Lab4_Responses", ttl=0)
                    updated = pd.concat([existing, new_data], ignore_index=True)
                    conn.update(worksheet="Lab4_Responses", data=updated)
                    st.success("บันทึก Exit Reflection สำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
            else:
                st.success("บันทึกจำลองสำเร็จ!")
        elif sub_ref:
            st.warning("กรุณากรอกรหัสนิสิต")

    st.markdown("---")
    st.info(
        """
        ### 🌟 ข้อความปิดท้าย:
        “ความกล้าหาญทางจริยธรรมไม่ใช่เพียงการกล้าโต้แย้ง แต่คือการเลือกดำเนินการอย่างมีเหตุผล รอบคอบ และรับผิดชอบต่อผู้ที่ได้รับผลกระทบ”
        """
    )
    
    st.subheader("📋 ตารางรวบรวม Exit Reflection (Lab 4)")
    if conn:
        try:
            df = conn.read(worksheet="Lab4_Responses", ttl=5)
            ref_df = df[df["Step"] == "Lab4 - Exit Reflection"]
            if not ref_df.empty:
                st.dataframe(ref_df[["Timestamp", "Data"]], use_container_width=True)
        except:
            pass
