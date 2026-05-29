# ⚽ First Contact Control Index (FCCI) — Defending Corners Analysis

## 📌 Project Overview

Corners are often decided before the shot happens.

This project analyzes defensive corner performance using StatsBomb Open Data by measuring which teams control the **first meaningful contact** after a corner delivery.

Rather than focusing only on goals conceded, the analysis evaluates:

* aerial dominance
* defensive structure
* immediate danger prevention
* first-phase control during set pieces

The project introduces a custom metric called the **First Contact Control Index (FCCI)** to quantify how effectively teams neutralize corners at first contact.

---

## 🎯 Objective

Build a football analytics model that tracks:

* who wins first contact after corners
* how corners are resolved
* how often dangerous first contacts are allowed

---

## 📊 Dataset

**Source:** StatsBomb Open Data

* Competition: La Liga
* Season: 2020/21
* Data Type:

  * Events Data
  * Match Data

Data Includes:

* corner deliveries
* defensive clearances
* duels
* blocks
* shots
* second-phase events

---

## ⚽ Key Research Question

> Which teams control corners best at first contact?

---

# 🧠 Methodology

## 1. Corner Extraction

Corner events were isolated using StatsBomb event data:

* Event Type = Pass
* Pass Type = Corner

---

## 2. First Contact Detection

For every corner:

* a short post-corner event window was analyzed
* the first decisive football action was identified

Priority-based event logic was used to avoid noisy event chains.

### Key Events Tracked

* Clearance
* Block
* Interception
* Duel
* Shot
* Ball Receipt*
* Miscontrol

---

## 3. Outcome Classification

First contacts were categorized into:

| Outcome   | Meaning                               |
| --------- | ------------------------------------- |
| Win       | Defensive control of first contact    |
| Contested | Aerial/physical duel situations       |
| Danger    | Immediate dangerous attacking outcome |

---

# 📈 First Contact Control Index (FCCI)

The custom FCCI metric was defined as:

FCCI = Win Rate − Danger Rate

Where:

* Win Rate measures successful defensive control at first contact
* Danger Rate measures immediate dangerous outcomes allowed from corners

Higher FCCI values indicate stronger defensive corner control.

---

# 📊 Example Team Output

| Team            | Win Rate | Danger Rate | FCCI  |
| --------------- | -------- | ----------- | ----- |
| Athletic Club   | 66.7%    | 0.0%        | 66.7  |
| Huesca          | 75.0%    | 25.0%       | 50.0  |
| Elche           | 66.7%    | 33.3%       | 33.3  |
| Barcelona       | 30.4%    | 21.7%       | 8.7   |
| Atlético Madrid | 25.0%    | 50.0%       | -25.0 |

---

# 🔍 Key Insights

* Most corners are decided through contested aerial phases rather than immediate shots.
* Teams with strong first-contact control significantly reduce dangerous outcomes.
* Barcelona faced a high number of corners but showed relatively weak first-contact dominance in this sample.
* Atlético Madrid recorded the weakest FCCI score in the analyzed sample, indicating vulnerability in defensive corner phases.

---

# 🛠 Tools & Libraries

* Python
* Pandas
* Requests
* StatsBomb Open Data
* Matplotlib / Plotly
* Streamlit (planned dashboard)

---

# 🚀 Future Improvements

Planned extensions include:

* zone-based corner analysis
* near-post vs far-post deliveries
* second-ball control metrics
* xG weighting of corner outcomes
* full Streamlit dashboard deployment

---

# 📁 Project Structure

```bash
├── data/
├── notebooks/
├── app34.py
├── README.md
└── requirements.txt
```

---

# 📌 Data Source

StatsBomb Open Data

https://github.com/statsbomb/open-data

---

# 👤 Author

Stephen Yaw Ayamah

Football Data Analytics Project
