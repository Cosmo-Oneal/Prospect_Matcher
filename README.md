NFL Prospect Matcher
A data-driven tool that compares an NFL draft prospect's combine measurements to every player in the combine database since 2000, identifying the 10 most physically similar historical players. Designed to give scouts and analysts a fast, objective way to project a prospect's draft range based on measurables alone.
---
How It Works
All eight combine metrics are standardized into z-scores so that measurements with different units (inches, lbs, seconds, reps) are directly comparable.
Euclidean distance is calculated between the prospect's z-scores and every player at the same position in the database.
The 10 closest matches are returned, along with a ceiling (highest drafted comparable) and a floor (lowest drafted or undrafted comparable).
---
Features
Position-aware matching — comparisons are restricted to players at the same position
Supports grouped positions (e.g., Edge Rusher pulls from DE, OLB, and Edge data)
Undrafted players are represented as pick 999 and automatically become the floor
Interactive Streamlit UI with a sidebar for entering measurements
---
Tech Stack
Tool	Purpose
Python	Core logic
pandas	Data loading and manipulation
scikit-learn	Z-score standardization and Euclidean distance
Streamlit	Interactive web UI
---
Project Structure
```
nfl-prospect-matcher/
├── ProspectMatcherUI.py        # Streamlit UI
├── ProspectMatcher.py          # Core matching logic
├── NFL_combine_Since_2000.csv  # Combine dataset (2000–present)
└── README.md
```
---
Example Output
Enter a prospect's measurements in the sidebar, select their position, and click Find Matches.
The tool returns:
Top 10 Matches — the most physically similar players, sorted by similarity score
Ceiling — the highest drafted player among the matches (best case outcome)
Floor — the lowest drafted or undrafted player among the matches (worst case outcome)
---
Combine Metrics Used
Metric	Unit
Height	inches
Weight	lbs
40 Yard Dash	seconds
Vertical Jump	inches
Bench Press	reps at 225 lbs
Broad Jump	inches
3 Cone Drill	seconds
20 Yard Shuttle	seconds
