# 🧭 AI Career Guidance Agent

An intelligent, single-agent career advisory web application built with **Python**, **Google Gemini API** (`google-genai` SDK), **JSON Schema / Pydantic**, and **Streamlit**.

The application collects a student's educational background, technical/soft skills, interests, practical experience, and career aspirations, then uses an autonomous AI agent to analyze their profile and return a strictly validated, structured career report.

---

## 🌟 Key Features & Innovative Capabilities

1. **Single Autonomous AI Agent**:
   - Evaluates profile strengths and readiness holistically in a single pass.
   - Constrained by a strict Pydantic JSON Schema (`CareerGuidanceReport`) using `response_schema` in the official `google-genai` SDK.
2. **Three Suitable Career Paths**:
   - Primary direct match, growth/adjacent match, and emerging specialization.
   - Quantified compatibility score (`match_percentage`) and transparent rationale (`why_it_fits`).
3. **🗺️ Visual Interactive Learning Roadmap (Mermaid.js Innovation)**:
   - Dynamic interactive flowcharts rendered directly inside the dashboard showing baseline skills, milestone checkpoints, capstone projects, and target roles.
   - Switchable layouts (Vertical Top-to-Bottom or Horizontal Left-to-Right) and 1-click exportable Mermaid code for GitHub/Notion.
4. **⚡ Interactive "What-If" Skill Simulator (Gamified Innovation)**:
   - Real-time interactive skill gap checkboxes that dynamically recalculate the student's career compatibility score and animate a live progress bar.
5. **🛠️ 1-Click Portfolio Project Architect & README Blueprint**:
   - Auto-generates complete, production-grade GitHub `README.md` blueprints, directory trees, system architecture diagrams, and download buttons for suggested projects.
6. **🎤 AI Mock Interview Coach & Roleplay**:
   - Curated technical, system design, and behavioral interview questions tailored to the candidate's exact profile and target job roles, with STAR methodology feedback and sample high-scoring answers.
7. **🕸️ Skill Competency Radar Analytics (Plotly)**:
   - Interactive radar / spider charts comparing student's current baseline vs Path 1, Path 2, and Path 3 requirements across 5 core dimensions.
8. **💼 Recruiter Outreach & Networking Toolkit**:
   - 1-click tailored LinkedIn connection pitches (<300 chars), cold emails to engineering managers, and 30-second elevator pitches for career fairs.
9. **📄 Dual Export Engine (JSON + Executive Markdown Dossier)**:
   - Export structured JSON for machine integration, or download a full Markdown dossier (`.md`) ready for printing and portfolio sharing.
10. **Pragmatic Industry Reality Check & Disclaimer**:
   - Grounded perspective on tech hiring market dynamics with clear ethical disclaimers.


---

## 📁 Folder Structure

```
ai-career-guidance-agent/
│
├── .env.example              # Template for environment variables (GEMINI_API_KEY)
├── .gitignore                # Git ignore rules for virtual env, cache, and secrets
├── requirements.txt          # Python library dependencies
├── README.md                 # Project documentation and setup guide
├── app.py                    # Streamlit web application frontend
│
└── src/
    ├── __init__.py           # Package marker
    ├── config.py             # Configuration and environment variable loader
    ├── schemas.py            # Pydantic schemas (JSON Schema definition)
    ├── agent.py              # Single AI Career Guidance Agent using google-genai SDK
    └── utils.py              # Helpers, JSON export, and sample demo profiles
```

---

## 📋 Prerequisites

- **Python**: Version 3.10 or higher.
- **Gemini API Key**: Free or paid API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
- **Code Editor**: Visual Studio Code (recommended) or any modern IDE.

---

## ⚙️ Installation & Setup (Step-by-Step)

### Step 1: Open the Project in VS Code
1. Launch **Visual Studio Code**.
2. Click **File** > **Open Folder...**
3. Navigate to and select the project directory:
   ```
   C:\Users\Admin\.gemini\antigravity\scratch\ai-career-guidance-agent
   ```
4. Open the integrated terminal in VS Code:
   - Shortcut: `` Ctrl + ` `` (Control + Backtick)
   - Or click menu: **Terminal** > **New Terminal**.

---

### Step 2: Create and Activate a Virtual Environment (Recommended)

In your VS Code terminal (PowerShell or Bash), run:

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If PowerShell restricts script execution, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once, then activate again).*

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3: Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

This installs:
- `google-genai` (Official Google Gen AI SDK)
- `streamlit` (Web application framework)
- `pydantic` (Data validation and JSON Schema enforcement)
- `python-dotenv` (Environment variable management)

---

### Step 4: Configure Your Gemini API Key

You have two simple ways to configure your API key:

#### Option A: Using a `.env` file (Recommended for development)
1. In the project root, copy `.env.example` to create a `.env` file:
   ```powershell
   # Windows PowerShell:
   Copy-Item .env.example .env
   ```
2. Open the `.env` file in VS Code and paste your Gemini API key:
   ```ini
   GEMINI_API_KEY=AIzaSyYourActualKeyHere
   GEMINI_MODEL=gemini-2.5-flash
   ```

#### Option B: Setting a System / Session Environment Variable
**On Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="AIzaSyYourActualKeyHere"
```

**On Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=AIzaSyYourActualKeyHere
```

**On macOS / Linux:**
```bash
export GEMINI_API_KEY="AIzaSyYourActualKeyHere"
```

#### Option C: Directly via the Web Interface
You can also launch the app and paste your API key into the secure password field in the sidebar!

---

## 🚀 Running the Application

Launch the Streamlit web app by executing:

```bash
streamlit run app.py
```
*(Or `python -m streamlit run app.py` if streamlit is not in your global system PATH).*

Streamlit will print the local URL and automatically open it in your browser:
```
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## 💡 How to Use the Application

1. **Quick Test with a Demo Profile**:
   - In the left sidebar, open the **⚡ Quick Load Demo Profiles** dropdown.
   - Choose a profile (e.g., *"AI & Data Enthusiast (CS Undergrad)"* or *"Self-Taught Web Developer"*).
   - Click **Load Preset**. The form automatically populates with realistic student data!
2. **Or Enter Your Own Profile**:
   - Fill in your degree, major, university, graduation year, technical skills, soft skills, interests, and career goals.
3. **Run the AI Agent**:
   - Click **🚀 Run AI Career Guidance Agent**.
   - The autonomous agent calls the Gemini API with structured JSON Schema enforcement.
4. **Explore the Structured Output**:
   - **Executive Assessment**: Strengths and immediate 7-day action items.
   - **Career Tabs**: Switch between 3 tailored career paths. Review match scores, relevant job titles, skill gaps, learning roadmaps, and practical portfolio projects.
   - **Industry Reality Check & Employment Disclaimer**: Grounded advice and explicit notification that guidance does not guarantee job placement.
5. **Download the JSON Report**:
   - Click **📥 Download Report (JSON)** in the upper right to save the full report to your computer.

---

## 🏗️ Architecture & Single-Agent Design

```
+-----------------------------------------------------------+
|                      Streamlit UI                         |
|   (Profile Form, Demo Presets, Tabbed Dashboard, JSON DL) |
+-----------------------------+-----------------------------+
                              | StudentProfile (Pydantic)
                              v
+-----------------------------------------------------------+
|                 CareerGuidanceAgent (agent.py)            |
|   - Single autonomous AI advisory agent                   |
|   - Evaluates readiness, gaps, and milestones             |
+-----------------------------+-----------------------------+
                              | System Prompt + Schema
                              v
+-----------------------------------------------------------+
|              Google Gen AI SDK (google-genai)             |
|   - Client: genai.Client(api_key=...)                     |
|   - Model: gemini-2.5-flash                               |
|   - Config: response_schema=CareerGuidanceReport          |
|             response_mime_type="application/json"         |
+-----------------------------+-----------------------------+
                              | JSON output matching schema
                              v
+-----------------------------------------------------------+
|          CareerGuidanceReport Validation (schemas.py)     |
|   - Pydantic model validation                             |
|   - Renders interactive UI & exportable JSON payload      |
+-----------------------------------------------------------+
```

---

## ⚖️ Ethical Advisory & Employment Disclaimer

This tool is designed purely for **educational guidance, skill benchmarking, and strategic learning planning**. 

- **No Employment Guarantee**: Completion of recommended roadmaps, projects, or acquisition of skills does not guarantee employment, interviews, offers, or specific compensation levels.
- **Market Dynamics**: Hiring criteria vary widely across employers, geographical locations, economic cycles, and specific job openings.
- **Actionable Effort**: Success in technology careers requires consistent individual effort, hands-on coding, networking, continuous learning, and adapting to industry shifts.
