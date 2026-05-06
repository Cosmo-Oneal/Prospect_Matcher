import streamlit as st
from ProspectMatcher import prospect_matcher

st.title("NFL Prospect Matcher")
st.write("Enter the prospect's combine measurements in the sidebar on the left and select their position, then press 'Find Matches'.")
st.write("The tool will find the 5 most physically similar NFL players from combine data since 2000. The ceiling is the highest drafted player among the matches (best case outcome), and the floor is the lowest drafted player or undrafted (worst case outcome). Undrafted players are represented as pick 999.")

position_dictionary = {
    "Quarterback"    : ["QB"],
    "Running Back"   : ["RB", "FB"],
    "Receiver"       : ["WR"],
    "Cornerback"     : ["CB", "DB"],
    "Safety"         : ["S", "DB", "SAF"],
    "Edgde Rusher"   : ["DE", "OLB", "Edgde"],
    "Tight End"      : ["TE", "LS"],
    "Linebacker"     : ["LB", "ILB"],
    "Defensive Line" : ["DL", "DE", "DT"],
    "Offensive Line" : ["LS", "OT", "C", "OL", "OG"]
}

with st.sidebar:
    st.header("Prospect Measurements")
    height = st.number_input("Height(inches)", min_value = 55.0, max_value = 90.0, step=0.5)
    weight = st.number_input("Weight(pounds)", min_value = 130.0, max_value = 480.0, step = 5.0)
    fourty_yard_dash = st.number_input("40 Yard Dash(seconds)", min_value = 3.00, max_value = 8.00, step = 0.01)
    vertical_jump = st.number_input("Vertical Jump(inches)", min_value = 16.0, max_value = 50.0, step = 0.5)
    bench_press = st.number_input("Bench Press(reps)", min_value = 0.0, max_value = 60.0, step = 1.0)
    broad_jump = st.number_input("Broad Jump(inches)", min_value = 60.0, max_value = 170.0, step = 0.5)
    three_cone_drill = st.number_input("3 Cone Drill (seconds)", min_value = 6.00, max_value = 8.00, step = 0.1)
    twenty_yard_shuttle = st.number_input("20 Yard Shuttle(seconds)", min_value = 3.00, max_value = 6.00, step = 0.1)
    position = st.selectbox("Position", list(position_dictionary.keys()))
    run_button = st.button("Find Matches")

position_abr = position_dictionary[position]

if run_button:
    prospect = {
    'Height': height,
    'Weight': weight,
    '40-yd Dash': fourty_yard_dash,
    'Vertical Jump': vertical_jump,
    'Bench Press': bench_press,
    'Broad Jump': broad_jump,
    '3-Cone Drill': three_cone_drill,
    '20-yd Shuttle': twenty_yard_shuttle
    }
    matches,floor,ceiling = prospect_matcher(prospect, position_abr) 
    st.subheader("Top 10 Matches")
    st.dataframe(matches[['Player', 'Position', 'Pick', 'similarity_score']])

    st.subheader("Ceiling")
    st.dataframe(ceiling[['Player', 'Position', 'Pick', 'similarity_score']].to_frame().T)

    st.subheader("Floor")
    st.dataframe(floor[['Player', 'Position', 'Pick', 'similarity_score']].to_frame().T)