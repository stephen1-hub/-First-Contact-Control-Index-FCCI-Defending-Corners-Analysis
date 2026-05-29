# ---------------------------------------------------
# ⚽ FCCI DASHBOARD — INTERACTIVE VERSION
# ---------------------------------------------------

import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="FCCI Interactive Dashboard",
    layout="wide"
)

st.title("⚽ First Contact Control Index (FCCI)")
st.markdown("Interactive league-wide set-piece first-contact analysis")

# ---------------------------------------------------
# SEASON SELECTOR
# ---------------------------------------------------
SEASONS = {
    "La Liga 2020/21": {
        "competition_id": 11,
        "season_id": 90
    }
}

season_name = st.sidebar.selectbox(
    "Select Season",
    list(SEASONS.keys())
)

competition_id = SEASONS[season_name]["competition_id"]
season_id = SEASONS[season_name]["season_id"]

# ---------------------------------------------------
# LOAD MATCHES
# ---------------------------------------------------
@st.cache_data
def load_matches(competition_id, season_id):

    url = f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/{competition_id}/{season_id}.json"
    data = requests.get(url).json()

    return pd.json_normalize(data)

matches = load_matches(competition_id, season_id)

match_ids = matches["match_id"].tolist()

# ---------------------------------------------------
# FIRST CONTACT ENGINE
# ---------------------------------------------------
priority = {
    "Shot": 3,
    "Clearance": 2,
    "Block": 2,
    "Interception": 2,
    "Duel": 1,
    "Ball Receipt*": 1,
    "Miscontrol": 1
}

def load_events(match_id):

    url = f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json"
    data = requests.get(url).json()

    return pd.json_normalize(data)

def get_first_contact(df, idx):

    best_event = None
    best_score = 0

    max_index = min(idx + 10, len(df))

    for i in range(idx + 1, max_index):

        event = df.iloc[i]
        etype = event.get("type.name", None)
        team = event.get("team.name", None)

        if etype in priority and team is not None:

            if priority[etype] > best_score:
                best_event = (etype, team)
                best_score = priority[etype]

    return best_event if best_event else (None, None)

def classify(event):

    if event in ["Clearance", "Block", "Interception"]:
        return "Win"
    elif event == "Shot":
        return "Danger"
    elif event in ["Duel", "Ball Receipt*", "Miscontrol"]:
        return "Contested"
    return "Other"

# ---------------------------------------------------
# BUILD DATASET (CACHED)
# ---------------------------------------------------
@st.cache_data
def build_fc_dataset(match_ids):

    results = []

    for match_id in match_ids:

        df = load_events(match_id)

        corners = df[
            (df["type.name"] == "Pass") &
            (df["pass.type.name"] == "Corner")
        ]

        for idx in corners.index:

            event, team = get_first_contact(df, idx)

            if event is None or team is None:
                continue

            results.append({
                "match_id": match_id,
                "team": team,
                "event": event,
                "outcome": classify(event)
            })

    return pd.DataFrame(results)

fc_df = build_fc_dataset(match_ids)

# ---------------------------------------------------
# FILTERS
# ---------------------------------------------------
st.sidebar.header("Filters")

min_corners = st.sidebar.slider("Minimum Corners", 0, 50, 3)

team_list = sorted(fc_df["team"].unique())

selected_teams = st.sidebar.multiselect(
    "Select Teams",
    team_list,
    default=team_list
)

filtered_df = fc_df[
    fc_df["team"].isin(selected_teams)
]

# ---------------------------------------------------
# TEAM METRICS
# ---------------------------------------------------
comparison = filtered_df.groupby("team").agg(
    Total_Corners=("outcome", "count"),
    Wins=("outcome", lambda x: (x == "Win").sum()),
    Danger=("outcome", lambda x: (x == "Danger").sum())
).reset_index()

comparison["Win Rate"] = comparison["Wins"] / comparison["Total_Corners"] * 100
comparison["Danger Rate"] = comparison["Danger"] / comparison["Total_Corners"] * 100
comparison["FCCI"] = comparison["Win Rate"] - comparison["Danger Rate"]

# Apply filter
comparison = comparison[comparison["Total_Corners"] >= min_corners]

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
st.subheader("📊 Season Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Teams", len(comparison))
col2.metric("Total Corners_Faced", int(comparison["Total_Corners"].sum()))
col3.metric("Avg FCCI", f"{comparison['FCCI'].mean():.2f}")

# ---------------------------------------------------
# FCCI RANKING
# ---------------------------------------------------
st.subheader("🏆 FCCI League Rankings")

ranking = comparison.sort_values("FCCI", ascending=False)

st.dataframe(ranking, use_container_width=True)

# ---------------------------------------------------
# VISUALIZATION 1 — FCCI
# ---------------------------------------------------
st.subheader("📈 FCCI Comparison")

fig = px.bar(
    ranking,
    x="team",
    y="FCCI",
    color="FCCI",
    title="First Contact Control Index (FCCI)"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# VISUALIZATION 2 — WIN VS DANGER
# ---------------------------------------------------
st.subheader("⚽ Defensive Corner Outcomes")

fig2 = px.bar(
    comparison,
    x="team",
    y=["Wins", "Danger"],
    barmode="group"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# RAW DATA
# ---------------------------------------------------
st.subheader("📄 Event-Level Data")

st.dataframe(filtered_df, use_container_width=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.markdown("Author")
st.markdown("Stephen Yaw Ayamah, Football Data Analyst")
