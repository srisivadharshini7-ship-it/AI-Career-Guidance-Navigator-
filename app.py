"""Streamlit Web Application for the AI Career Guidance Agent.
Features high-end UI styling, interactive Mermaid roadmaps, 'What-If' skill simulators,
competency radar analytics, mock interview coaching, and recruiter outreach toolkits.
"""

import os
import sys
import subprocess
from datetime import datetime

# Streamlit applications must be run via `streamlit run app.py`.
# If the user runs `python app.py`, auto-redirect to streamlit run:
from streamlit.runtime import exists

if not exists():
    print("\n" + "=" * 65)
    print("🧭 Notice: Streamlit applications should be launched via Streamlit.")
    print("🚀 Auto-launching: streamlit run app.py ...")
    print("=" * 65 + "\n")
    sys.exit(subprocess.call([sys.executable, "-m", "streamlit", "run", __file__] + sys.argv[1:]))

import streamlit as st
import streamlit.components.v1 as components

from src.schemas import StudentProfile, EducationInfo
from src.agent import CareerGuidanceAgent
from src.config import DEFAULT_MODEL, get_gemini_api_key, is_likely_valid_key
from src.utils import (
    SAMPLE_PROFILES,
    load_preset_profile,
    report_to_json_str,
    generate_mock_report,
    generate_mermaid_roadmap,
    render_mermaid_html,
    generate_project_scaffold_readme,
    generate_mock_interview_questions,
    generate_radar_chart_figure,
    generate_outreach_templates,
    report_to_markdown_dossier,
)

# Set Streamlit page configuration
st.set_page_config(
    page_title="AI Career Guidance Navigator",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Advanced CSS styling for premium look and feel
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .hero-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #3B82F6 100%);
        padding: 2.2rem 2.4rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 12px 28px -6px rgba(30, 58, 138, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.6px;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .hero-sub {
        font-size: 1.05rem;
        color: #E2E8F0;
        margin-top: 0.6rem;
        margin-bottom: 0;
        line-height: 1.55;
        max-width: 900px;
    }
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.1rem 1.4rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 0.2rem;
    }
    .card-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.3rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .card-box:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.06);
    }
    .badge {
        display: inline-block;
        padding: 0.28rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }
    .badge-blue { background-color: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; }
    .badge-green { background-color: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }
    .badge-purple { background-color: #F5F3FF; color: #6D28D9; border: 1px solid #DDD6FE; }
    .badge-orange { background-color: #FFF7ED; color: #C2410C; border: 1px solid #FED7AA; }
    .badge-red { background-color: #FEF2F2; color: #B91C1C; border: 1px solid #FECACA; }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_session_state():
    """Initialize default values in Streamlit session state."""
    if "report" not in st.session_state:
        st.session_state["report"] = None
    if "user_api_key" not in st.session_state:
        st.session_state["user_api_key"] = ""
    if "mode_used" not in st.session_state:
        st.session_state["mode_used"] = "built_in"
    if "profile_input" not in st.session_state:
        # Default to Aarav Sharma's preset
        default_preset = load_preset_profile("AI & Data Enthusiast (CS Undergrad)")
        st.session_state["profile_input"] = default_preset


init_session_state()

# ==============================================================================
# SIDEBAR: Configuration & Preset Selector
# ==============================================================================
with st.sidebar:
    st.image(
        "https://api.iconify.design/fluent-emoji-flat:compass.svg",
        width=55,
    )
    st.title("Settings & Engine")
    st.caption("Single Autonomous AI Agent • Google Gen AI SDK • JSON Schema")

    st.markdown("---")
    st.subheader("🔑 Gemini AI Configuration")

    env_key = get_gemini_api_key()
    env_is_valid = is_likely_valid_key(env_key)
    saved_custom_key = st.session_state.get("user_api_key", "").strip()

    if saved_custom_key and is_likely_valid_key(saved_custom_key):
        active_api_key = saved_custom_key
        masked_key = active_api_key[:4] + "..." + active_api_key[-4:]
        st.success(f"🟢 **Live Gemini API Active:** `{masked_key}`")
    elif env_key and env_is_valid:
        active_api_key = env_key
        masked_key = active_api_key[:4] + "..." + active_api_key[-4:]
        st.success(f"🟢 **Live Gemini API (.env):** `{masked_key}`")
    else:
        active_api_key = None
        st.info(
            "⚡ **Instant Advisory Mode Active**\n\n"
            "Runs immediately with zero configuration! To connect live Gemini AI models, enter your AI Studio key below."
        )

    user_key_override = st.text_input(
        "Gemini API Key (Optional)",
        value=saved_custom_key,
        type="password",
        placeholder="AIzaSy... (leave blank to run free)",
        help="Get a free key from https://aistudio.google.com/app/apikey to use live Gemini API.",
    )

    if user_key_override.strip():
        st.session_state["user_api_key"] = user_key_override.strip()
        active_api_key = user_key_override.strip()

    # Model selection
    selected_model = st.selectbox(
        "Gemini Model",
        options=["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"],
        index=0,
        help="Recommended: gemini-2.5-flash for fastest speed and strict schema validation.",
    )

    st.markdown("---")
    st.subheader("⚡ Quick Load Demo Profiles")
    preset_choice = st.selectbox(
        "Select candidate background:",
        options=["Select a sample profile..."] + list(SAMPLE_PROFILES.keys()),
    )

    if st.button("Load Preset", use_container_width=True):
        if preset_choice != "Select a sample profile...":
            st.session_state["profile_input"] = load_preset_profile(preset_choice)
            st.session_state["report"] = None
            st.rerun()

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.83rem; color: #64748B; line-height: 1.4;">
        <strong>🛡️ Ethical Advisory Notice</strong><br>
        This tool uses an autonomous AI agent to evaluate profiles objectively. It provides educational roadmaps and skill gap analyses. It does <em>not</em> guarantee employment or interviews.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==============================================================================
# MAIN PAGE HERO HEADER
# ==============================================================================
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-title">
            <span>🧭</span> AI Career Guidance Navigator
        </div>
        <p class="hero-sub">
            Personalized career diagnostics, interactive skill gap simulations, visual Mermaid roadmaps,
            competency radar analytics, and recruiter outreach toolkits powered by Google Gemini and Structured JSON Schema.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

current_p = st.session_state["profile_input"]

# ==============================================================================
# PROFILE COLLECTION FORM
# ==============================================================================
with st.expander("📝 Candidate Profile Input (Click to Expand / Edit)", expanded=(st.session_state["report"] is None)):
    with st.form("student_profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🎓 Education & Background")
            full_name = st.text_input(
                "Full Name",
                value=current_p.full_name,
                placeholder="e.g. Alex Morgan",
            )
            degree = st.text_input(
                "Degree or Education Level *",
                value=current_p.education.level_or_degree,
                placeholder="e.g. B.Tech Computer Science, B.Sc Mathematics, High School Diploma",
            )
            field_of_study = st.text_input(
                "Field of Study / Specialization *",
                value=current_p.education.field_of_study,
                placeholder="e.g. Information Technology, Electronics, Business",
            )
            institution = st.text_input(
                "College or University (Optional)",
                value=current_p.education.institution or "",
                placeholder="e.g. State University",
            )
            grad_status = st.text_input(
                "Graduation Year or Status *",
                value=current_p.education.graduation_year_or_status,
                placeholder="e.g. 3rd Year (Graduating 2026), Recent Graduate (2025)",
            )

            experience_level_options = [
                "Complete Beginner (No coding experience yet)",
                "Student Projects & Coursework",
                "Self-Taught / Personal Projects",
                "1 Internship Completed",
                "1-2 Years Junior / Work Experience",
                "Career Switcher (Transitioning from non-tech domain)",
            ]
            default_exp_idx = 1
            for idx, opt in enumerate(experience_level_options):
                if current_p.experience_level.lower() in opt.lower():
                    default_exp_idx = idx
                    break

            experience_level = st.selectbox(
                "Experience Level *",
                options=experience_level_options,
                index=default_exp_idx,
            )

        with col2:
            st.markdown("#### 💡 Skills, Interests & Career Goals")
            tech_skills_str = st.text_area(
                "Technical Skills (comma-separated) *",
                value=", ".join(current_p.technical_skills),
                placeholder="e.g. Python, SQL, JavaScript, Git, Docker, Linux",
                help="Enter languages, libraries, tools, and technical concepts you are familiar with.",
                height=95,
            )

            soft_skills_str = st.text_input(
                "Soft Skills (comma-separated) *",
                value=", ".join(current_p.soft_skills),
                placeholder="e.g. Problem Solving, Communication, Fast Learner, Teamwork",
            )

            interests_str = st.text_input(
                "Areas of Interest / Passions (comma-separated) *",
                value=", ".join(current_p.interests),
                placeholder="e.g. Artificial Intelligence, Cloud Computing, Cybersecurity, Web Development",
            )

            experience_summary = st.text_area(
                "Experience & Project Summary *",
                value=current_p.experience_summary,
                placeholder="Describe academic projects, open-source work, internships, hackathons, or personal coding experiments...",
                height=100,
            )

            career_goals = st.text_area(
                "Career Aspirations & Target Goals *",
                value=current_p.career_goals,
                placeholder="e.g. Seeking an entry-level AI/ML engineer role in a product company; interested in hybrid work; want to build impactful AI systems.",
                height=100,
            )

        submitted = st.form_submit_button("🚀 Run AI Career Guidance Agent", use_container_width=True, type="primary")

        if submitted:
            # Form validation
            if not degree.strip() or not field_of_study.strip():
                st.error("Please fill in both Degree and Field of Study.")
            elif not tech_skills_str.strip():
                st.error("Please provide at least one technical skill or tool.")
            elif not interests_str.strip():
                st.error("Please provide at least one area of interest.")
            else:
                # Update session state with submitted inputs
                parsed_profile = StudentProfile(
                    full_name=full_name.strip() or "Student",
                    education=EducationInfo(
                        level_or_degree=degree.strip(),
                        field_of_study=field_of_study.strip(),
                        institution=institution.strip(),
                        graduation_year_or_status=grad_status.strip() or "Undergrad",
                    ),
                    technical_skills=[s.strip() for s in tech_skills_str.split(",") if s.strip()],
                    soft_skills=[s.strip() for s in soft_skills_str.split(",") if s.strip()] or ["Adaptability"],
                    interests=[s.strip() for s in interests_str.split(",") if s.strip()],
                    experience_level=experience_level,
                    experience_summary=experience_summary.strip() or "Undergraduate academic projects and self-study.",
                    career_goals=career_goals.strip() or "Looking for an entry-level software or tech role.",
                )
                st.session_state["profile_input"] = parsed_profile

                # If a valid AI Studio key is provided, run live Gemini API
                if active_api_key and is_likely_valid_key(active_api_key):
                    with st.spinner("🤖 Calling Google Gemini API with JSON Schema constraint..."):
                        try:
                            agent = CareerGuidanceAgent(api_key=active_api_key, model_name=selected_model)
                            report = agent.analyze_profile(parsed_profile)
                            st.session_state["report"] = report
                            st.session_state["mode_used"] = "live_gemini"
                            st.success("✅ Analysis complete via Google Gemini API! Scroll down to view your report.")
                            st.rerun()
                        except Exception as err:
                            st.warning(f"⚠️ Live Gemini API Notice: {str(err)}\n\nGenerating your report using the Intelligent Career Guidance Engine...")
                            report = generate_mock_report(parsed_profile)
                            st.session_state["report"] = report
                            st.session_state["mode_used"] = "built_in"
                            st.rerun()
                else:
                    # Run instantly with built-in intelligent engine!
                    with st.spinner("🤖 The AI Career Guidance Agent is analyzing your profile, evaluating skill gaps, and generating roadmaps..."):
                        report = generate_mock_report(parsed_profile)
                        st.session_state["report"] = report
                        st.session_state["mode_used"] = "built_in"
                        st.success("✅ Analysis complete! Scroll down to explore your customized Career Guidance Report.")
                        st.rerun()

# ==============================================================================
# REPORT DISPLAY SECTION
# ==============================================================================
report = st.session_state["report"]

if report is not None:
    st.markdown("---")

    # Header Strip with Dual Download Buttons (JSON + Markdown Dossier)
    header_col1, header_col2, header_col3 = st.columns([2.5, 1, 1])
    with header_col1:
        st.subheader(f"📊 Career Strategy Report: {report.student_name}")
        mode_desc = "Live Google Gemini Model" if st.session_state.get("mode_used") == "live_gemini" else "Intelligent Career Advisory Engine"
        st.caption(f"Generated on {report.generated_at} • Evaluated by Single AI Career Guidance Agent ({mode_desc})")
    with header_col2:
        json_data = report_to_json_str(report)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"career_guidance_{report.student_name.lower().replace(' ', '_')}.json",
            mime="application/json",
            use_container_width=True,
        )
    with header_col3:
        md_dossier = report_to_markdown_dossier(report)
        st.download_button(
            label="📄 Download Dossier (.md)",
            data=md_dossier,
            file_name=f"career_dossier_{report.student_name.lower().replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    # Top KPI Metrics Strip
    top_match = max([p.match_percentage for p in report.career_paths])
    total_roles = sum([len(p.relevant_job_roles) for p in report.career_paths])

    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <span class="kpi-label">Peak Compatibility</span>
                <span class="kpi-value" style="color: #2563EB;">{top_match}%</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with kpi2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <span class="kpi-label">Analyzed Trajectories</span>
                <span class="kpi-value" style="color: #7C3AED;">3 Paths</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with kpi3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <span class="kpi-label">Searchable Roles</span>
                <span class="kpi-value" style="color: #059669;">{total_roles}+ Roles</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # 1. Executive Summary Card
    with st.container():
        st.markdown(
            f"""
            <div class="card-box" style="border-left: 5px solid #2563EB;">
                <h4 style="margin-top:0; color: #1E3A8A;">📌 Executive Profile Assessment</h4>
                <p style="color: #334155; font-size: 1.05rem; line-height: 1.6;">{report.profile_summary.overall_assessment}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_sum1, col_sum2 = st.columns(2)
        with col_sum1:
            st.markdown("##### 🌟 Key Profile Strengths")
            for strength in report.profile_summary.key_strengths:
                st.markdown(f"- **{strength}**")

        with col_sum2:
            st.markdown("##### 🎯 High-Leverage Actions (This Week)")
            for step in report.profile_summary.immediate_next_steps:
                st.markdown(f"- 🚀 {step}")

    st.markdown("---")

    # SPECIAL FEATURE: Overview Matrix & Competency Radar Tab Group
    main_view_tabs = st.tabs([
        "🎯 In-Depth Career Paths & Roadmaps",
        "📊 Competency Radar & Path Matrix",
    ])

    # TAB 1: In-Depth Career Paths
    with main_view_tabs[0]:
        st.markdown("### 🎯 Recommended Career Trajectories (Top 3)")
        st.caption("Each path includes compatibility rating, what-if skill simulators, visual Mermaid roadmaps, portfolio scaffolds, and mock interview coaching.")

        path_tab_titles = [
            f"Path 1: {report.career_paths[0].career_title} ({report.career_paths[0].match_percentage}% Match)",
            f"Path 2: {report.career_paths[1].career_title} ({report.career_paths[1].match_percentage}% Match)",
            f"Path 3: {report.career_paths[2].career_title} ({report.career_paths[2].match_percentage}% Match)",
        ]
        path_tabs = st.tabs(path_tab_titles)

        for i, tab in enumerate(path_tabs):
            path = report.career_paths[i]
            with tab:
                # Top metrics & Fit
                metric_col, fit_col = st.columns([1, 3])
                with metric_col:
                    st.metric(label="Baseline Compatibility", value=f"{path.match_percentage}%")
                with fit_col:
                    st.markdown("##### 🔍 Why This Career Fits You")
                    st.write(path.why_it_fits)

                # Job Roles & Responsibilities
                r_col1, r_col2 = st.columns(2)
                with r_col1:
                    st.markdown("##### 💼 Searchable Entry-Level Job Roles")
                    roles_html = "".join([f'<span class="badge badge-blue">{r}</span>' for r in path.relevant_job_roles])
                    st.markdown(roles_html, unsafe_allow_html=True)
                with r_col2:
                    st.markdown("##### 📋 Core Day-to-Day Responsibilities")
                    for resp in path.primary_responsibilities:
                        st.markdown(f"- {resp}")

                st.markdown("---")

                # SPECIAL FEATURE 1: Interactive What-If Skill Simulator
                with st.container():
                    st.markdown("##### ⚡ Interactive 'What-If' Skill Simulator")
                    st.caption("Check off skills you plan to learn or have recently acquired to simulate your upgraded match score in real time!")
                    sim_cols = st.columns(len(path.skill_gaps) if path.skill_gaps else 1)
                    gaps_learned = 0
                    for g_idx, gap in enumerate(path.skill_gaps):
                        with sim_cols[g_idx % len(sim_cols)]:
                            is_checked = st.checkbox(
                                f"Acquired: **{gap.missing_skill}**",
                                key=f"skill_sim_{i}_{g_idx}",
                                help=f"Priority: {gap.importance}. Reason: {gap.reason}",
                            )
                            if is_checked:
                                gaps_learned += 1

                    # Calculate boosted score
                    max_boost = 100 - path.match_percentage
                    boost_per_skill = max_boost / len(path.skill_gaps) if path.skill_gaps else 0
                    simulated_score = min(100, int(path.match_percentage + (gaps_learned * boost_per_skill)))

                    p_col1, p_col2 = st.columns([3, 1])
                    with p_col1:
                        st.progress(simulated_score / 100)
                    with p_col2:
                        if gaps_learned > 0:
                            st.markdown(f"**Simulated Match:** :green[**{simulated_score}%**] *(+{simulated_score - path.match_percentage}%)*")
                        else:
                            st.markdown(f"**Current Match:** **{path.match_percentage}%**")

                st.markdown("---")

                # Detailed Skill Gaps Cards
                st.markdown("##### ⚠️ Detailed Skill Gaps to Bridge")
                gap_cols = st.columns(len(path.skill_gaps) if path.skill_gaps else 1)
                for g_idx, gap in enumerate(path.skill_gaps):
                    with gap_cols[g_idx % len(gap_cols)]:
                        badge_color = "badge-red" if gap.importance == "High" else "badge-orange"
                        st.markdown(
                            f"""
                            <div class="card-box" style="min-height: 160px;">
                                <span class="badge {badge_color}">{gap.importance} Priority</span>
                                <span class="badge badge-purple">{gap.category}</span>
                                <h5 style="margin: 0.5rem 0 0.3rem 0; color: #0F172A;">{gap.missing_skill}</h5>
                                <p style="font-size: 0.88rem; color: #475569; margin: 0;">{gap.reason}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                st.markdown("---")

                # SPECIAL FEATURE 2: Visual Learning Roadmap with Mermaid.js & Step Cards
                st.markdown("##### 🗺️ Personalized Learning Roadmap")
                roadmap_view = st.radio(
                    "Select Roadmap View Mode:",
                    options=["🗺️ Visual Interactive Flowchart (Mermaid.js)", "📋 Step-by-Step Phase Cards"],
                    horizontal=True,
                    key=f"roadmap_view_{i}",
                )

                if roadmap_view == "🗺️ Visual Interactive Flowchart (Mermaid.js)":
                    orient_choice = st.radio(
                        "Diagram Layout:",
                        options=["Top-to-Bottom (Vertical)", "Left-to-Right (Horizontal)"],
                        horizontal=True,
                        key=f"orient_{i}",
                    )
                    orient_code = "TD" if "Vertical" in orient_choice else "LR"
                    mermaid_code = generate_mermaid_roadmap(
                        path=path,
                        current_skills=report.profile_summary.key_strengths,
                        orientation=orient_code,
                    )

                    diagram_height = 560 if orient_code == "TD" else 380
                    components.html(render_mermaid_html(mermaid_code), height=diagram_height, scrolling=True)

                    with st.expander("📋 View & Export Mermaid Diagram Code (for GitHub / Notion)"):
                        st.code(mermaid_code, language="mermaid")
                else:
                    for milestone in path.learning_roadmap:
                        with st.expander(f"📍 {milestone.phase_title} ({milestone.estimated_timeline})", expanded=True):
                            m_col1, m_col2 = st.columns(2)
                            with m_col1:
                                st.markdown("**Topics to Master:**")
                                for topic in milestone.key_topics:
                                    st.markdown(f"- {topic}")
                                st.markdown(f"**🎯 Checkpoint Goal:** *{milestone.milestone_checkpoint}*")
                            with m_col2:
                                st.markdown("**Recommended Resources & Certifications:**")
                                for res in milestone.recommended_resources:
                                    st.markdown(f"- {res}")

                st.markdown("---")

                # SPECIAL FEATURE 3: Portfolio Projects + 1-Click README Blueprint Generator
                st.markdown("##### 💻 Suggested Portfolio-Building Projects")
                proj_cols = st.columns(len(path.practical_projects) if path.practical_projects else 1)
                for p_idx, proj in enumerate(path.practical_projects):
                    with proj_cols[p_idx % len(proj_cols)]:
                        diff_badge = "badge-green" if proj.difficulty == "Beginner" else "badge-orange" if proj.difficulty == "Intermediate" else "badge-purple"
                        tools_html = "".join([f'<span class="badge badge-blue">{t}</span>' for t in proj.tech_stack])
                        st.markdown(
                            f"""
                            <div class="card-box" style="min-height: 250px;">
                                <span class="badge {diff_badge}">{proj.difficulty}</span>
                                <h4 style="margin: 0.5rem 0 0.3rem 0; color: #0F172A;">{proj.title}</h4>
                                <p style="font-size: 0.9rem; color: #334155;">{proj.description}</p>
                                <div style="margin-bottom: 0.5rem;"><strong>Tech Stack:</strong><br>{tools_html}</div>
                                <p style="font-size: 0.85rem; color: #15803D;"><strong>Portfolio Showcase Tip:</strong> {proj.portfolio_showcase_tip}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        with st.expander(f"🛠️ View & Download GitHub README Blueprint"):
                            readme_content = generate_project_scaffold_readme(proj, student_name=report.student_name)
                            st.markdown(readme_content)
                            st.download_button(
                                label="📥 Download README.md Blueprint",
                                data=readme_content,
                                file_name=f"README_{proj.title.lower().replace(' ', '_')[:20]}.md",
                                mime="text/markdown",
                                key=f"dl_readme_{i}_{p_idx}",
                                use_container_width=True,
                            )

                st.markdown("---")

                # SPECIAL FEATURE 4: Recruiter Outreach & Networking Toolkit
                with st.expander(f"💼 Recruiter Outreach & Networking Toolkit for {path.career_title}", expanded=False):
                    st.caption("Custom-crafted cold emails, LinkedIn connection pitches, and 30-second elevator pitches tailored to your background.")
                    templates = generate_outreach_templates(st.session_state["profile_input"], path)
                    
                    pitch_tab1, pitch_tab2, pitch_tab3 = st.tabs([
                        "💬 LinkedIn Connection Note (<300 chars)",
                        "📧 Cold Email to Hiring Manager",
                        "🎤 30-Second Elevator Pitch",
                    ])
                    with pitch_tab1:
                        st.code(templates["linkedin_pitch"], language="text")
                    with pitch_tab2:
                        st.code(templates["cold_email"], language="text")
                    with pitch_tab3:
                        st.info(templates["elevator_pitch"])

                st.markdown("---")

                # SPECIAL FEATURE 5: AI Mock Interview Coach & Roleplay
                with st.expander(f"🎤 AI Mock Interview Coach for {path.career_title} (Roleplay & Practice)", expanded=False):
                    st.markdown(
                        "Practice high-frequency technical and behavioral interview questions customized for this career path. "
                        "Draft your response and inspect evaluation criteria and high-scoring sample answers."
                    )
                    interview_qs = generate_mock_interview_questions(path.career_title)
                    for q_idx, q_data in enumerate(interview_qs, 1):
                        st.markdown(f"**Question {q_idx} [{q_data['category']}]:** {q_data['question']}")
                        st.text_area(
                            f"Your Answer (Question {q_idx})",
                            placeholder="Type your response here using the STAR method (Situation, Task, Action, Result)...",
                            key=f"interview_ans_{i}_{q_idx}",
                            height=85,
                        )
                        with st.expander(f"🔍 Show Evaluation Criteria & Sample Answer (Q{q_idx})"):
                            st.markdown("**Key Hiring Criteria:**")
                            for crit in q_data["key_criteria"]:
                                st.markdown(f"- ✅ {crit}")
                            st.markdown(f"**High-Scoring Sample Response:**\n> {q_data['sample_answer']}")

    # TAB 2: Competency Radar & Path Matrix
    with main_view_tabs[1]:
        st.markdown("### 📊 Skill Competency Radar & Career Matrix")
        st.caption("Multi-dimensional comparison of your current skillset versus the industry requirements for all three trajectories.")

        radar_col, matrix_col = st.columns([1.1, 1.2])

        with radar_col:
            st.markdown("##### 🕸️ Competency Radar Analysis")
            radar_fig = generate_radar_chart_figure(st.session_state["profile_input"], report.career_paths)
            if radar_fig is not None:
                st.plotly_chart(radar_fig, use_container_width=True)
            else:
                st.info("Competency Radar will render when Plotly is installed.")

        with matrix_col:
            st.markdown("##### 📋 Trajectory Comparison Matrix")
            for idx, p_item in enumerate(report.career_paths, 1):
                badge_bg = "badge-blue" if idx == 1 else "badge-purple" if idx == 2 else "badge-green"
                time_est = p_item.learning_roadmap[-1].estimated_timeline if p_item.learning_roadmap else "3-4 Months"
                st.markdown(
                    f"""
                    <div class="card-box" style="margin-bottom: 0.8rem; padding: 1rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                            <strong style="font-size: 1.05rem; color: #0F172A;">{p_item.career_title}</strong>
                            <span class="badge {badge_bg}">{p_item.match_percentage}% Match</span>
                        </div>
                        <p style="font-size: 0.88rem; color: #475569; margin-bottom: 0.4rem;">
                            <strong>Searchable Roles:</strong> {', '.join(p_item.relevant_job_roles[:2])}
                        </p>
                        <p style="font-size: 0.85rem; color: #64748B; margin: 0;">
                            ⏱️ <strong>Estimated Timeline:</strong> ~{time_est} | ⚠️ <strong>Gaps:</strong> {len(p_item.skill_gaps)} identified
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("---")

    # 3. Industry Reality Check & Disclaimer
    disc_col1, disc_col2 = st.columns(2)
    with disc_col1:
        st.markdown(
            f"""
            <div class="card-box" style="border-left: 5px solid #F59E0B;">
                <h4 style="margin-top:0; color: #B45309;">📈 Industry Reality Check</h4>
                <p style="font-size: 0.95rem; color: #475569; line-height: 1.55;">{report.industry_reality_check}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with disc_col2:
        st.markdown(
            f"""
            <div class="card-box" style="border-left: 5px solid #64748B;">
                <h4 style="margin-top:0; color: #1E293B;">⚖️ Employment & Advisory Disclaimer</h4>
                <p style="font-size: 0.95rem; color: #475569; line-height: 1.55;">{report.employment_disclaimer}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    # Helpful introductory guide when no report is generated yet
    st.info("👆 Review the candidate profile details above (or choose one from the sidebar presets), then click **Run AI Career Guidance Agent** to generate your customized career strategy.")
