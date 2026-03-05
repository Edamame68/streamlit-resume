# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

st.set_page_config(page_title="Chloe You | Interactive Resume", page_icon="📄", layout="wide")

# -----------------------------
# Data (from your resume PDF)
# -----------------------------
PROFILE = {
    "name": "Siyi (Chloe) You",
    "phone": "(778) 877-3029",
    "email": "siyi.you@rotman.utoronto.ca",
    "linkedin_text": "LinkedIn",
    # Put your actual LinkedIn URL here before deploying:
    "linkedin_url": "https://www.linkedin.com/",
    "headline": "Master of Management Analytics Candidate (Rotman, 2026) | Analytics + Strategy | Finance & Stats Background",
}

skills = [
    ("Python (NumPy, Pandas)", "Programming", 4),
    ("SQL (MySQL, PostgreSQL)", "Programming", 4),
    ("R (RStudio)", "Programming", 3),
    ("VBA", "Programming", 3),
    ("Power BI", "Analytics", 4),
    ("Microsoft Office (Excel/Word/PowerPoint)", "Tools", 5),
    ("Bloomberg Terminal", "Tools", 3),
    ("Adobe InDesign", "Tools", 3),
]
df_skills = pd.DataFrame(skills, columns=["Skill", "Category", "Proficiency (1-5)"])

education = [
    {
        "School": "Rotman School of Management, University of Toronto",
        "Location": "Toronto, ON",
        "Program": "Master of Management Analytics",
        "Year": "2026",
        "Highlights": [
            "MMA Entrance Award of $10,000 for Academic Excellence",
            "MCA naviGATE Case Competition Winner: 3-stage inclusive-investing strategy for LGBTQ+ ventures",
        ],
    },
    {
        "School": "Desautels Faculty of Management, McGill University",
        "Location": "Montreal, QC",
        "Program": "BCom, Finance major; Statistics minor",
        "Year": "2024",
        "Highlights": [
            "2x Tomlinson Engagement Award for Mentoring (2023, 2024): mentored 30+ first-year stats students",
            "Desautels Exchange Club Executive Director (2023): led 8-person team; hosted 6 events; grew participation by 20%",
        ],
    },
]
df_edu = pd.DataFrame(
    [{"School": e["School"], "Program": e["Program"], "Year": e["Year"], "Location": e["Location"]} for e in education]
)

experience = [
    {
        "Company": "DataSphere Lab, McGill University",
        "Location": "Montreal, Canada",
        "Role": "Grants Data Analyst",
        "Start": "2023-09-01",
        "End": "2025-06-30",
        "Bullets": [
            "Secured $25,000 in federal awards by building funding pipeline strategy; evaluated 50+ grants; supported call sourcing; created evaluation system",
            "Engineered data model + Power BI dashboard to standardize inputs, track deadlines/effort/value, segment by fit, rank via weighted rubric; produced go/no-go list",
            "Created a Proposal Copilot with prompt-engineered templates and an intake→draft→review workflow for faster first drafts",
            "Delivered 50% faster grant evaluation, sharper decision alignment, and higher throughput of submission-ready packages",
        ],
        "Tags": ["Analytics", "Power BI", "Strategy", "GenAI"],
    },
    {
        "Company": "Minsheng Securities",
        "Location": "Shanghai, China",
        "Role": "Research Analyst, Renewable Energy",
        "Start": "2024-05-01",
        "End": "2024-08-31",
        "Bullets": [
            "Researched eVTOL + renewable car sectors; identified trends and investment opportunities to support decisions",
            "Analyzed industry data, regulation, and technology to assess market potential and challenges; delivered insights to senior analysts",
        ],
        "Tags": ["Research", "Renewables", "eVTOL"],
    },
    {
        "Company": "Fosun Capital",
        "Location": "Shanghai, China",
        "Role": "Investment Analyst, Emerging Technology",
        "Start": "2023-05-01",
        "End": "2023-08-31",
        "Bullets": [
            "Performed diligence on shortlisted emerging-tech targets; produced valuation summaries for investment committee go/no-go decisions",
            "Used R to analyze company financial/operational data for M&A and financing; wrote 12+ research reports on trends and markets",
        ],
        "Tags": ["Finance", "Diligence", "R"],
    },
    {
        "Company": "Bank of East Asia",
        "Location": "Shanghai, China",
        "Role": "Credit Risk Analyst",
        "Start": "2021-05-01",
        "End": "2021-08-31",
        "Bullets": [
            "Processed 300+ KYC checks for mortgage applicants; assessed reputation and credit",
            "Flagged default risks to credit committee; supported decisions on approvals, limits, collateral, and pricing tiers",
        ],
        "Tags": ["Risk", "KYC", "Banking"],
    },
]
df_exp = pd.DataFrame(experience)

projects = [
    {
        "Project": "Integrated Management Student Fellowship (IMSF) – McGill Commute with Rideshare Optimization",
        "Theme": "Sustainable Transportation / UN SDGs",
        "Highlights": [
            "Selected as 1 of 65 fellows (2024 cohort) leading measurable-impact SDG projects",
            "Led initiative with McGill Office of Sustainability to improve carpool matching app usage",
            "Analyzed 200+ user profiles; engineered features (role, location/FSA, commute window) using R + Python; built geospatial heatmaps",
            "Designed a 3-stage pilot; projected 50% reduction in driver–passenger imbalance and +10 weekly matches upon rollout",
        ],
    }
]
df_projects = pd.DataFrame([{"Project": p["Project"], "Theme": p["Theme"]} for p in projects])

# -----------------------------
# Sidebar (interactive widgets)
# -----------------------------
st.sidebar.title("🎛️ Customize view")

section = st.sidebar.selectbox(
    "Jump to section",
    ["Overview", "Skills", "Experience", "Education", "Projects"],
)

min_prof = st.sidebar.slider("Minimum skill proficiency to show", 1, 5, 3)  # Widget #1
selected_cats = st.sidebar.multiselect(
    "Skill categories",
    sorted(df_skills["Category"].unique().tolist()),
    default=sorted(df_skills["Category"].unique().tolist()),
)  # Widget #2

show_details = st.sidebar.checkbox("Show detailed bullet points", value=True)  # Widget #3

tag_filter = st.sidebar.multiselect(
    "Filter experience by tag",
    sorted({t for tags in df_exp["Tags"] for t in tags}),
    default=[],
)  # Widget #4 (extra)

# -----------------------------
# Header
# -----------------------------
left, right = st.columns([0.72, 0.28])
with left:
    st.title(PROFILE["name"])
    st.caption(PROFILE["headline"])
    st.write(f"📞 {PROFILE['phone']}  |  ✉️ {PROFILE['email']}  |  🔗 [{PROFILE['linkedin_text']}]({PROFILE['linkedin_url']})")

with right:
    # Optional headshot if you add assets/headshot.png
    try:
        st.image("assets/headshot.png", caption="Chloe You", use_container_width=True)
    except Exception:
        st.info("Tip: add `assets/headshot.png` to show a headshot.")

st.divider()

# -----------------------------
# Helpers
# -----------------------------
def render_bullets(items):
    for b in items:
        st.write(f"• {b}")

def experience_timeline_chart(df):
    tmp = df.copy()
    tmp["Start_dt"] = pd.to_datetime(tmp["Start"])
    tmp["End_dt"] = pd.to_datetime(tmp["End"])
    tmp["Duration_months"] = (tmp["End_dt"].dt.year - tmp["Start_dt"].dt.year) * 12 + (tmp["End_dt"].dt.month - tmp["Start_dt"].dt.month)
    tmp["Label"] = tmp["Role"] + " @ " + tmp["Company"]

    base = alt.Chart(tmp).mark_bar().encode(
        y=alt.Y("Label:N", sort="-x"),
        x=alt.X("Start_dt:T", title="Start"),
        x2=alt.X2("End_dt:T", title="End"),
        tooltip=["Company", "Role", "Location", "Start_dt:T", "End_dt:T"]
    ).properties(height=220)

    return base

def skills_chart(df):
    return (
        alt.Chart(df)
        .mark_bar()
        .encode(
            y=alt.Y("Skill:N", sort="-x"),
            x=alt.X("Proficiency (1-5):Q", scale=alt.Scale(domain=[0, 5])),
            tooltip=["Skill", "Category", "Proficiency (1-5)"],
        )
        .properties(height=260)
    )

# -----------------------------
# Section rendering
# -----------------------------
if section == "Overview":
    st.subheader("Summary")
    st.write(
        "I’m an analytics-focused candidate with experience across grants analytics, finance, and research. "
        "I build structured decision systems (dashboards, rubrics, workflows) and translate messy program or market information into clear go/no-go recommendations."
    )

    st.subheader("Highlights")
    cols = st.columns(3)
    with cols[0]:
        st.metric("Federal awards secured", "$25,000")
    with cols[1]:
        st.metric("Grant opportunities evaluated", "50+")
    with cols[2]:
        st.metric("KYC checks processed", "300+")

    st.subheader("Quick view")
    st.write("Skills (filtered by your sidebar settings) + experience timeline preview:")
    filtered_skills = df_skills[
        (df_skills["Proficiency (1-5)"] >= min_prof) & (df_skills["Category"].isin(selected_cats))
    ]
    st.altair_chart(skills_chart(filtered_skills), use_container_width=True)
    st.altair_chart(experience_timeline_chart(df_exp), use_container_width=True)

elif section == "Skills":
    st.subheader("Skills table")
    filtered = df_skills[
        (df_skills["Proficiency (1-5)"] >= min_prof) & (df_skills["Category"].isin(selected_cats))
    ].sort_values(["Category", "Proficiency (1-5)"], ascending=[True, False])

    st.dataframe(filtered, use_container_width=True, hide_index=True)  # Table requirement ✅

    st.subheader("Skills proficiency chart")
    st.altair_chart(skills_chart(filtered), use_container_width=True)  # Chart requirement ✅

elif section == "Experience":
    st.subheader("Experience timeline")
    st.altair_chart(experience_timeline_chart(df_exp), use_container_width=True)

    st.subheader("Experience details")

    shown = df_exp.copy()
    if tag_filter:
        shown = shown[shown["Tags"].apply(lambda tags: any(t in tags for t in tag_filter))]

    for _, row in shown.iterrows():
        st.markdown(f"### {row['Role']} — {row['Company']}")
        st.caption(f"{row['Location']} | {row['Start']} → {row['End']} | Tags: {', '.join(row['Tags'])}")
        if show_details:
            render_bullets(row["Bullets"])
        st.divider()

elif section == "Education":
    st.subheader("Education table")
    st.dataframe(df_edu, use_container_width=True, hide_index=True)

    st.subheader("Details")
    for e in education:
        st.markdown(f"### {e['Program']} — {e['School']}")
        st.caption(f"{e['Location']} | {e['Year']}")
        if show_details:
            render_bullets(e["Highlights"])
        st.divider()

elif section == "Projects":
    st.subheader("Projects table")
    st.dataframe(df_projects, use_container_width=True, hide_index=True)

    st.subheader("Details")
    for p in projects:
        st.markdown(f"### {p['Project']}")
        st.caption(p["Theme"])
        if show_details:
            render_bullets(p["Highlights"])
        st.divider()

st.caption("Built with Streamlit • Interactive widgets: section jump, skill slider, category multiselect, details toggle, tag filter")
