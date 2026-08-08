st.title("⚡ AI Panel Builder")

st.info("""
1. Select Electrical Parameters
2. Select Enclosure
3. Generate BOM & CAD
4. Run AI Analysis
5. Ask AI Questions
6. Download Reports
""")

import streamlit as st
import pandas as pd
import os

# =========================
# FILE MANAGEMENT
# =========================

os.makedirs("input data", exist_ok=True)
os.makedirs("blocks", exist_ok=True)
os.makedirs("datasheet", exist_ok=True)

st.sidebar.header("📂 Optional File Uploads")

uploaded_files = st.sidebar.file_uploader(
    "Upload Additional Files (Optional)",
    type=["csv", "dxf", "pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    for uploaded_file in uploaded_files:

        filename = uploaded_file.name

        if filename.lower().endswith(".csv"):
            save_path = os.path.join("input data", filename)

        elif filename.lower().endswith(".dxf"):
            save_path = os.path.join("blocks", filename)

        elif filename.lower().endswith(".pdf"):
            save_path = os.path.join("datasheet", filename)

        else:
            continue

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    st.sidebar.success("✅ Files uploaded successfully")

# =========================
# LOAD DEFAULT PROJECT FILES
# =========================

switchgear_path = "input data/Switchgear Data.csv"
enclosure_path = "input data/Enclosure Data.csv"

if not os.path.exists(switchgear_path):
    st.error("❌ Switchgear Data.csv not found")
    st.stop()

if not os.path.exists(enclosure_path):
    st.error("❌ Enclosure Data.csv not found")
    st.stop()

switchgear_df = pd.read_csv(switchgear_path)
enclosure_df = pd.read_csv(enclosure_path)

# =========================
# CLEAN DATA
# =========================

switchgear_df.columns = switchgear_df.columns.str.strip()
enclosure_df.columns = enclosure_df.columns.str.strip()

for col in switchgear_df.columns:
    if switchgear_df[col].dtype == "object":
        switchgear_df[col] = switchgear_df[col].str.strip()

for col in enclosure_df.columns:
    if enclosure_df[col].dtype == "object":
        enclosure_df[col] = enclosure_df[col].str.strip()

switchgear_df["HP"] = pd.to_numeric(
    switchgear_df["HP"],
    errors="coerce"
)

enclosure_df["Enclosure_H"] = pd.to_numeric(
    enclosure_df["Enclosure_H"],
    errors="coerce"
)

enclosure_df["Enclosure_W"] = pd.to_numeric(
    enclosure_df["Enclosure_W"],
    errors="coerce"
)

enclosure_df["Enclosure_D"] = pd.to_numeric(
    enclosure_df["Enclosure_D"],
    errors="coerce"
)

# =========================
# USER SELECTION
# =========================

import streamlit as st
import pandas as pd

# Load data
switchgear_df = pd.read_csv("input data/Switchgear Data.csv")
enclosure_df = pd.read_csv("input data/Enclosure Data.csv")

# Clean column names
switchgear_df.columns = switchgear_df.columns.str.strip()
enclosure_df.columns = enclosure_df.columns.str.strip()

# Clean string values
for col in switchgear_df.columns:
    if switchgear_df[col].dtype == "object":
        switchgear_df[col] = switchgear_df[col].str.strip()

for col in enclosure_df.columns:
    if enclosure_df[col].dtype == "object":
        enclosure_df[col] = enclosure_df[col].str.strip()

# =========================
# ELECTRICAL SELECTION
# =========================

st.subheader("⚡ Electrical Selection")

starter = st.selectbox(
    "Starter Type",
    sorted(switchgear_df["Starter"].dropna().unique())
)

filtered_mains = switchgear_df[
    switchgear_df["Starter"] == starter
]

mains = st.selectbox(
    "Mains Protection",
    sorted(filtered_mains["Mains_Protection"].dropna().unique())
)

filtered_hp = switchgear_df[
    (switchgear_df["Starter"] == starter)
    &
    (switchgear_df["Mains_Protection"] == mains)
]

hp = st.selectbox(
    "Motor Rating (HP)",
    sorted(filtered_hp["HP"].dropna().unique())
)

# =========================
# ENCLOSURE SELECTION
# =========================

st.subheader("📦 Enclosure Selection")

etype = st.selectbox(
    "Enclosure Type",
    sorted(enclosure_df["Enclosure_Type"].dropna().unique())
)

filtered_height = enclosure_df[
    enclosure_df["Enclosure_Type"] == etype
]

height = st.selectbox(
    "Height",
    sorted(filtered_height["Enclosure_H"].dropna().unique())
)

filtered_width = enclosure_df[
    (enclosure_df["Enclosure_Type"] == etype)
    &
    (enclosure_df["Enclosure_H"] == height)
]

width = st.selectbox(
    "Width",
    sorted(filtered_width["Enclosure_W"].dropna().unique())
)

filtered_depth = enclosure_df[
    (enclosure_df["Enclosure_Type"] == etype)
    &
    (enclosure_df["Enclosure_H"] == height)
    &
    (enclosure_df["Enclosure_W"] == width)
]

depth = st.selectbox(
    "Depth",
    sorted(filtered_depth["Enclosure_D"].dropna().unique())
)

# =========================
# CONFIRM BUTTON
# =========================

if st.button("✅ Confirm Selection"):

    st.success("Selection Confirmed")

    st.write("### Electrical Selection")
    st.write(f"Starter : {starter}")
    st.write(f"Mains : {mains}")
    st.write(f"HP : {hp}")

    st.write("### Enclosure Selection")
    st.write(f"Type : {etype}")
    st.write(f"Size : {height} x {width} x {depth}")

# =========================
# ✅ FILTER ELECTRICAL DATA
# =========================

filtered = switchgear_df[
    (switchgear_df['Starter'] == starter) &
    (switchgear_df['Mains_Protection'] == mains) &
    (switchgear_df['HP'] == hp)
]

if filtered.empty:
    st.error("❌ No matching data found")
    st.stop()

selected_row = filtered.iloc[0]

# =========================
# ✅ CLEAN RESULT
# =========================

clean_result = {
    k: v for k, v in selected_row.to_dict().items()
    if pd.notna(v) and str(v).strip().lower() != "nan"
}

# =========================
# ✅ BUILD BOM
# =========================

bom_dict = {}

component_mapping = {
    "Contactor_Main": "Contactor",
    "Contactor_Star": "Contactor",
    "Contactor_Delta": "Contactor",
    "Overload Relay": "Overload Relay",
    "Circuit_Breaker": "Circuit Breaker",
    "Fuse": "Fuse",
    "HRC_Fuse": "Fuse",
    "Fuse_Disconnector_Switch": "Switch",
    "Timer": "Timer"
}

for key, description in component_mapping.items():

    if key in clean_result:

        part_no = str(clean_result[key]).strip()

        if part_no in bom_dict:
            bom_dict[part_no]["Qty"] += 1
        else:
            bom_dict[part_no] = {
                "Description": description,
                "Part No": part_no,
                "Qty": 1
            }

# =========================
# ✅ ENCLOSURE
# =========================

filtered_enclosure = enclosure_df[
    (enclosure_df['Enclosure_Type'] == etype) &
    (enclosure_df['Enclosure_H'] == height) &
    (enclosure_df['Enclosure_W'] == width) &
    (enclosure_df['Enclosure_D'] == depth)
]

if not filtered_enclosure.empty:

    enclosure_result = filtered_enclosure.iloc[0].to_dict()

    part_no = enclosure_result["Enclosure"]

    bom_dict[part_no] = {
        "Description": "Enclosure",
        "Part No": part_no,
        "Qty": 1
    }

# =========================
# ✅ BOM TABLE
# =========================

bom_df = pd.DataFrame(bom_dict.values())

bom_df = bom_df.sort_values(by="Description").reset_index(drop=True)

bom_df.insert(0, "Sr. No", range(1, len(bom_df) + 1))

st.subheader("📦 BOM")

st.dataframe(bom_df)

# =========================
# ✅ EXCEL DOWNLOAD
# =========================

file_name = "Final_BOM.xlsx"

bom_df.to_excel(
    file_name,
    index=False,
    engine="openpyxl"
)

with open(file_name, "rb") as f:
    st.download_button(
        label="⬇ Download BOM Excel",
        data=f,
        file_name="Final_BOM.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
# ==================================================
# ✅ CAD GENERATION + VISUALIZATION + DOWNLOADS
# ==================================================

st.subheader("📐 CAD Layout")

try:

    # Generate DXF
    dxf_file = create_final_panel(
        bom_df,
        enclosure_result,
        file_name="FINAL_PANEL.dxf"
    )

    st.success("✅ CAD Layout Generated Successfully")

    # ------------------------------------------
    # VISUALIZE DXF
    # ------------------------------------------
    import ezdxf
    import matplotlib.pyplot as plt

    from ezdxf.addons.drawing import (
        RenderContext,
        Frontend,
        config,
    )

    from ezdxf.addons.drawing.matplotlib import (
        MatplotlibBackend,
    )

    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()

    ctx = RenderContext(doc)

    fig = plt.figure(figsize=(12, 16), dpi=150)

    ax = fig.add_axes([0, 0, 1, 1])

    out = MatplotlibBackend(ax)

    cfg = config.Configuration(
        background_policy=config.BackgroundPolicy.WHITE,
        color_policy=config.ColorPolicy.BLACK,
    )

    frontend = Frontend(
        ctx,
        out,
        config=cfg
    )

    frontend.draw_layout(
        msp,
        finalize=True
    )

    for patch in ax.patches:
        patch.set_facecolor("black")
        patch.set_edgecolor("black")

    ax.set_aspect("equal")

    ax.set_title(
        f"Panel Visualization: "
        f"{enclosure_result['Enclosure']} "
        f"({enclosure_result['Enclosure_H']} mm Height)"
    )

    # ✅ Show CAD inside Streamlit
    st.pyplot(fig)

    # ------------------------------------------
    # DXF DOWNLOAD
    # ------------------------------------------
    with open(dxf_file, "rb") as f:
        st.download_button(
            label="⬇ Download DXF Layout",
            data=f,
            file_name="FINAL_PANEL.dxf",
            mime="application/dxf"
        )

    # ------------------------------------------
    # CREATE PDF FROM VISUALIZATION
    # ------------------------------------------
    pdf_filename = "Electrical_Panel.pdf"

    plt.savefig(
        pdf_filename,
        bbox_inches="tight",
        pad_inches=0.1,
        dpi=300
    )

    # ------------------------------------------
    # PDF DOWNLOAD
    # ------------------------------------------
    with open(pdf_filename, "rb") as f:
        st.download_button(
            label="⬇ Download Layout PDF",
            data=f,
            file_name="Electrical_Panel.pdf",
            mime="application/pdf"
        )

except Exception as e:
    st.error(f"❌ CAD Generation Failed: {e}")
import json
import streamlit as st
import google.generativeai as genai

# =========================
# GEMINI CONFIG
# =========================

genai.configure(
    api_key=st.secrets["GOOGLE_API_KEY"]
)

model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# CONTEXT
# =========================

context = json.dumps(panel_data, indent=2)

# =========================
# AI ANALYSIS
# =========================

st.subheader("🤖 AI Design Analysis")

if st.button("Run AI Analysis"):

    prompt = f"""
You are an expert electrical design engineer.

Analyze the following motor starter panel configuration:

{context}

Provide:
- Technical explanation
- Safety considerations
- Risks
- Suggestions
- Rating (1-10)

Answer clearly in structured bullet points.
"""

    try:
        with st.spinner("AI is analysing..."):

            analysis = model.generate_content(prompt)

            ai_analysis_text = analysis.text

            st.session_state["ai_analysis_text"] = ai_analysis_text

            st.markdown(ai_analysis_text)

    except Exception as e:
        st.error(f"AI Analysis Failed: {e}")
st.subheader("💬 Ask AI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.text_input(
    "Ask about this panel design"
)

if st.button("Ask AI"):

    if question.strip():

        try:

            prompt = f"""
You are an expert electrical design engineer.

Panel Configuration:

{context}

Question:

{question}

Answer clearly and technically.
"""

            with st.spinner("AI is thinking..."):

                response = model.generate_content(prompt)

                answer = response.text

            st.session_state.chat_history.append(
                ("User", question)
            )

            st.session_state.chat_history.append(
                ("AI", answer)
            )

        except Exception as e:
            st.error(f"AI Error: {e}")

if st.session_state.chat_history:

    st.subheader("Conversation")

    for role, msg in st.session_state.chat_history:

        if role == "User":
            st.markdown(
                f"**🧑 User:** {msg}"
            )
        else:
            st.markdown(
                f"**🤖 AI:** {msg}"
            )

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

# =========================
# PDF CREATION FUNCTION
# =========================

def create_report():

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    doc = SimpleDocTemplate(temp_file.name)

    styles = getSampleStyleSheet()

    content = []

    # -------------------------
    # Title
    # -------------------------
    content.append(
        Paragraph(
            "AI Panel Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    # -------------------------
    # AI Analysis
    # -------------------------
    if "ai_analysis_text" in st.session_state:

        content.append(
            Paragraph(
                "AI Design Analysis",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                st.session_state["ai_analysis_text"].replace(
                    "\n",
                    "<br/>"
                ),
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 12))

    # -------------------------
    # Chat History
    # -------------------------
    content.append(
        Paragraph(
            "Chat History",
            styles["Heading2"]
        )
    )

    for role, msg in st.session_state.chat_history:

        content.append(
            Paragraph(
                f"<b>{role}</b>: {msg}",
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 5))

    doc.build(content)

    return temp_file.name

st.subheader("📄 Report")

if st.button("Generate PDF Report"):

    pdf_file = create_report()

    with open(pdf_file, "rb") as f:

        st.download_button(
            "⬇ Download Report",
            f,
            file_name="AI_Panel_Report.pdf",
            mime="application/pdf"
        )

st.session_state["ai_analysis_text"] = ai_text