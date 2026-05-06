import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances


# ─────────────────────────────────────────────
# DATA LOADING & CLEANING
# ─────────────────────────────────────────────

# Load NFL Combine data (2000–present) and drop any player missing a required measurement.
# All eight physical metrics must be present for a valid comparison.
NFL_Combine_Data = pd.read_csv('NFL_combine_Since_2000.csv')
NFL_Combine_Data_Clean = NFL_Combine_Data.dropna(
    subset=['Height', 'Weight', '40-yd Dash', 'Vertical Jump',
            'Bench Press', 'Broad Jump', '3-Cone Drill', '20-yd Shuttle']
)


# ─────────────────────────────────────────────
# FEATURE SCALING
# ─────────────────────────────────────────────

# Standardize all eight metrics into z-scores so that measurements with
# different units (inches, lbs, seconds, reps) are directly comparable.
scaler = StandardScaler()
Combine_Scaled = scaler.fit_transform(
    NFL_Combine_Data_Clean[['Height', 'Weight', '40-yd Dash', 'Vertical Jump',
                             'Bench Press', 'Broad Jump', '3-Cone Drill', '20-yd Shuttle']]
)


# ─────────────────────────────────────────────
# PROSPECT MATCHING
# ─────────────────────────────────────────────

def prospect_matcher(prospect: dict, position: list):
    """
    Find the 10 most athletically similar NFL Combine participants to a given prospect.

    Similarity is calculated using Euclidean distance between z-scored combine
    measurements. Comparisons are restricted to players at the same position(s).

    Args:
        prospect (dict): A dictionary of the prospect's combine measurements.
                         Required keys: 'Height', 'Weight', '40-yd Dash',
                         'Vertical Jump', 'Bench Press', 'Broad Jump',
                         '3-Cone Drill', '20-yd Shuttle'.
        position (list): A list of positions to compare against (e.g., ["WR", "TE"]).
                         Accepts multiple positions to allow cross-position comparisons.

    Returns:
        matches (DataFrame):   Top 10 most similar historical players, sorted by similarity score.
        floor_row (Series):    The match with the lowest draft stock (highest pick number).
        ceiling_row (Series):  The match with the highest draft stock (lowest pick number).
    """

    # Filter the dataset to only include players at the specified position(s).
    # Accepts a list so that adjacent positions can be compared (e.g., WR and TE).
    filtered_data = NFL_Combine_Data_Clean.loc[
        NFL_Combine_Data_Clean['Position'].isin(position)
    ].copy()

    # Re-apply the scaler to the position-filtered subset for distance calculations
    filtered_data_scaled = scaler.transform(
        filtered_data[['Height', 'Weight', '40-yd Dash', 'Vertical Jump',
                        'Bench Press', 'Broad Jump', '3-Cone Drill', '20-yd Shuttle']]
    )

    # Scale the prospect's measurements using the same scaler for a fair comparison.
    # transform() is used (not fit_transform()) to preserve the original scaling reference.
    prospect_df = pd.DataFrame([prospect])
    prospect_scaled = scaler.transform(
        prospect_df[['Height', 'Weight', '40-yd Dash', 'Vertical Jump',
                     'Bench Press', 'Broad Jump', '3-Cone Drill', '20-yd Shuttle']]
    )

    # Compute Euclidean distance between the prospect and every player in the filtered set.
    # A smaller distance indicates a closer physical match.
    distances = euclidean_distances(prospect_scaled, filtered_data_scaled)

    # Insert similarity scores as a new column, replacing any previous run's scores
    if 'similarity_score' in filtered_data.columns:
        filtered_data.drop(columns=['similarity_score'], inplace=True)
    filtered_data.insert(loc=1, column='similarity_score', value=distances[0])

    # Treat undrafted players as pick #999 so they sort correctly in floor/ceiling logic
    filtered_data['Pick'] = filtered_data['Pick'].fillna(999)

    # Sort by similarity score and take the top 10 matches
    matches = filtered_data.sort_values('similarity_score').head(10)

    # Floor: the worst draft outcome among the top 10 matches (highest pick number)
    floor_row = matches.loc[matches['Pick'].idxmax()]

    # Ceiling: the best draft outcome among the top 10 matches (lowest pick number)
    ceiling_row = matches.loc[matches['Pick'].idxmin()]

    return matches, floor_row, ceiling_row
