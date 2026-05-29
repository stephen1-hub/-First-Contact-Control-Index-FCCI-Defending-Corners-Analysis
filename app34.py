# ⚽ FCCI Streamlit Dashboard — Full Structure


# ---------------------------------------------------
# IMPORT LIBRARIES
# ---------------------------------------------------
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="First Contact Control Index Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("⚽ First Contact Control Index (FCCI)")
st.markdown(
    "Analyzing defensive corner performance using StatsBomb Open Data"
)

# ---------------------------------------------------
# LOAD MATCH DATA
# ---------------------------------------------------
@st.cache_data

def load_matches():

    matches_url = (
        "https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/11/90.json"
    )

    data = requests.get(matches_url).json()

    matches = pd.json_normalize(data)

    return matches

matches = load_matches()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.header("Dashboard Filters")

match_options = matches[
    [
        "match_id",
        "home_team.home_team_name",
        "away_team.away_team_name"
    ]
].copy()

match_options["label"] = (
    match_options["home_team.home_team_name"]
    + " vs "
    + match_options["away_team.away_team_name"]
)

selected_match = st.sidebar.selectbox(
    "Select Match",
    match_options["label"]
)

selected_match_id = match_options[
    match_options["label"] == selected_match
]["match_id"].values[0]

# ---------------------------------------------------
# LOAD EVENT DATA
# ---------------------------------------------------
@st.cache_data

def load_events(match_id):

    events_url = (
        f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json"
    )

    data = requests.get(events_url).json()

    df = pd.json_normalize(data)

    return df


# ---------------------------------------------------
# FIRST CONTACT LOGIC
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


def get_first_contact(df, idx):

    best_event = None
    best_score = 0

    max_index = min(idx + 10, len(df))

    for i in range(idx + 1, max_index):

        event = df.iloc[i]
        etype = event['type.name']

        if etype in priority:

            if priority[etype] > best_score:
                best_event = (etype, event['team.name'])
                best_score = priority[etype]

    return best_event if best_event else (None, None)


# ---------------------------------------------------
# CLASSIFICATION FUNCTION
# ---------------------------------------------------
def classify(event):

    if event in ["Clearance", "Block", "Interception"]:
        return "Win"

    elif event == "Shot":
        return "Danger"

    elif event in ["Duel", "Ball Receipt*", "Miscontrol"]:
        return "Contested"

    else:
        return "Other"


# ---------------------------------------------------
# PROCESS MATCH
# ---------------------------------------------------
df = load_events(selected_match_id)

corners = df[
    (df['type.name'] == 'Pass') &
    (df['pass.type.name'] == 'Corner')
]

results = []

for idx in corners.index:

    event, team = get_first_contact(df, idx)

    results.append({
        "corner_index": idx,
        "team": team,
        "event": event,
        "outcome": classify(event)
    })

fc_df = pd.DataFrame(results)

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------
total_corners = len(fc_df)

wins = len(fc_df[fc_df['outcome'] == 'Win'])

contested = len(fc_df[fc_df['outcome'] == 'Contested'])

danger = len(fc_df[fc_df['outcome'] == 'Danger'])

win_rate = (wins / total_corners) * 100 if total_corners > 0 else 0

danger_rate = (danger / total_corners) * 100 if total_corners > 0 else 0

fcci = win_rate - danger_rate

# ---------------------------------------------------
# DISPLAY KPIs
# ---------------------------------------------------
st.subheader("📊 FCCI Match Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Corners", total_corners)

with col2:
    st.metric("Win Rate", f"{win_rate:.1f}%")

with col3:
    st.metric("Danger Rate", f"{danger_rate:.1f}%")

with col4:
    st.metric("FCCI", f"{fcci:.1f}")

# ---------------------------------------------------
# OUTCOME DISTRIBUTION
# ---------------------------------------------------
st.subheader("📈 First Contact Outcome Distribution")

outcome_counts = (
    fc_df['outcome']
    .value_counts()
    .reset_index()
)

outcome_counts.columns = ['Outcome', 'Count']

fig = px.bar(
    outcome_counts,
    x='Outcome',
    y='Count',
    title='Corner First Contact Outcomes'
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# EVENT DISTRIBUTION
# ---------------------------------------------------
st.subheader("⚽ First Contact Event Types")

fig2 = px.pie(
    fc_df,
    names='event',
    title='Distribution of First Contact Events'
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# TEAM BREAKDOWN
# ---------------------------------------------------
st.subheader("🏟 Team Breakdown")

team_breakdown = (
    fc_df.groupby(['team', 'outcome'])
    .size()
    .reset_index(name='count')
)

fig3 = px.bar(
    team_breakdown,
    x='team',
    y='count',
    color='outcome',
    barmode='stack',
    title='Team First Contact Outcomes'
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# RAW DATA TABLE
# ---------------------------------------------------
st.subheader("🗂 First Contact Event Table")

st.dataframe(fc_df, use_container_width=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.markdown(
    "Built using StatsBomb Open Data | Football Analytics Project"
)

