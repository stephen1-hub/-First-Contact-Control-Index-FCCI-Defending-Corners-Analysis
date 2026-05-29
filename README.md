# First Contact Control Index (FCCI)
Defensive Set-Piece Intelligence from StatsBomb Open Data
# Project Overview

Corners are often analysed through goals, xG, or final outcomes.

But in reality:

⚽ Set-pieces are frequently decided before the shot — at the first contact phase.

This project introduces the First Contact Control Index (FCCI), a custom football analytics metric designed to evaluate how effectively teams control the first meaningful action after a corner delivery.

Instead of focusing on end results, this model evaluates the initial defensive response to danger.

🧠 Core Idea

When a corner is delivered, the most important phase is not the shot.

It is the first 2–3 seconds after delivery, where teams either:

regain control
concede immediate danger
enter a contested aerial/second-ball phase
# Objective

Build a data-driven framework to:

Identify which teams win first contact on corners
Measure how often dangerous situations are allowed
Quantify defensive set-piece stability
Compare teams across an entire league season
# Dataset

Source: StatsBomb Open Data
Competition: La Liga (selected season)

Data used:
Match events data
Corner deliveries
Defensive actions (clearances, blocks, interceptions)
Shot events
Duel and ball recovery sequences
# Methodology
1. Corner Extraction

Corners are identified using:

Event type = Pass
Pass type = Corner
2. First Contact Detection

For each corner:

A short post-delivery window is scanned to identify the first meaningful football action.

Key event types considered:

Clearance
Block
Interception
Duel
Ball Receipt
Miscontrol
Shot

A priority-based system determines the most impactful first contact.

3. Outcome Classification

Each first contact is classified as:

Outcome	Definition
Win	Defensive control (clearance, block, interception)
Danger	Immediate attacking threat (shot)
Contested	Aerial/physical duel or unstable control phase
Other	Neutral or low-impact events
4. FCCI Formula

The First Contact Control Index (FCCI) is defined as:

FCCI = Win Rate − Danger Rate

# Interpretation:
High FCCI → strong defensive control at first contact
Low / negative FCCI → vulnerability in early set-piece phases
📈 Key Results (League-Level Analysis)
🟢 Strong Defensive Control
Team	FCCI
Athletic Club	71.4
Cádiz	50.0
Osasuna	50.0
Real Valladolid	50.0

These teams consistently neutralise corners at the first contact stage.

🟡 Balanced / Mixed Profiles
Team	FCCI
Barcelona	8.9
Real Madrid	31.2
Valencia	12.5

These teams show moderate control but allow structured danger phases.

🔴 Weak First-Contact Control
Team	FCCI
Sevilla	-18.2
Villarreal	-14.3
Real Betis	-12.5
Levante	-8.3

These teams frequently concede dangerous first-contact situations.

📊 Key Insights
Set-piece outcomes are heavily influenced by first-contact battles, not final shots.
Teams with strong aerial structure suppress danger early.
Barcelona’s large sample shows consistent exposure but moderate control.
Some teams show systemic weakness in defensive set-piece organisation rather than isolated mistakes.
# Tools & Technologies
Python
Pandas
Requests
StatsBomb Open Data API
Plotly (visualisation)
Streamlit (dashboard development)
#  Project Structure
├── data/
├── notebooks/
├── app34.py                # Streamlit dashboard
├── FCCI_analysis.ipynb  # Exploratory analysis
├── README.md
└── requirements.txt
# Streamlit Dashboard Features
Interactive FCCI leaderboard
Team filtering
Win vs Danger breakdown
League-wide ranking visualization
Raw event inspection
Fully cached multi-match pipeline
# live demo: https://gpjemckqbzy3eoepoenj6k.streamlit.app/
📌 Key Contribution

This project reframes set-piece analysis by shifting focus from:

❌ Final outcomes (goals, xG)

to:

✅ First-contact control dynamics

# Future Work
Zone-based corner analysis (near post vs far post)
Weighted FCCI (event importance scoring)
xG integration for set-piece danger
Player-level aerial dominance metrics
Multi-season comparison model
# Author

Stephen Yaw Ayamah
Football Data Analytics Project

# Data Source

StatsBomb Open Data
https://github.com/statsbomb/open-data

# Final Insight

“Teams don’t lose corners at the shot — they lose them at the first contact.”
