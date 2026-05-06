import pandas as pd
from sklearn.preprocessing import StandardScaler #used to create Z-scores on combine data
from sklearn.metrics.pairwise import euclidean_distances # used to calculate the distance from a prospect to a current player using the z-scores 

NFL_Combine_Data = pd.read_csv('NFL_combine_Since_2000.csv')

NFL_Combine_Data_Clean = NFL_Combine_Data.dropna(subset=['Height','Weight','40-yd Dash','Vertical Jump', 'Bench Press', 'Broad Jump', '3-Cone Drill', '20-yd Shuttle']) # deletes all of the players that have NAN in combine drills (can't compare them to prospects if they have no combine data)

scaler = StandardScaler() # object used to scale data
Combine_Scaled = scaler.fit_transform(NFL_Combine_Data_Clean[['Height','Weight','40-yd Dash','Vertical Jump', 'Bench Press', 'Broad Jump', '3-Cone Drill', '20-yd Shuttle']]) # puts z-scores on all of the NFL combine data, height and weight


def prospect_matcher(prospect, position):
    # makes sure that the prospect matches are only of the same position 
    filtered_NFL_Combine_Date = NFL_Combine_Data_Clean.loc[NFL_Combine_Data_Clean['Position'].isin(position)]         # only use players of the same postion filters the data 
    filtered_NFL_Combine_Date_Scaled = scaler.transform(filtered_NFL_Combine_Date[['Height','Weight','40-yd Dash','Vertical Jump', 'Bench Press', 'Broad Jump', '3-Cone Drill', '20-yd Shuttle']]) # rescales the data based on only using the position 
    
    # makes the prospect data into a data frame
    prospect_data = pd.DataFrame([prospect])         # makes a dictionary into a list
    Prospect_Scaled = scaler.transform(prospect_data[['Height','Weight','40-yd Dash','Vertical Jump', 'Bench Press', 'Broad Jump', '3-Cone Drill', '20-yd Shuttle']])    # use trasnform here becasue using the same scale method previously created

    # creates the distance and then makes a similarity score based on physicals used to compare prospects to a player
    distances = euclidean_distances(Prospect_Scaled,filtered_NFL_Combine_Date_Scaled)     # caclulates the linear distance from the z-scores of the prospect to the data set of current nfl players
    if 'similarity_score' in filtered_NFL_Combine_Date.columns:                    # checks if a column is already made so no error appears if made twice
        filtered_NFL_Combine_Date.drop(columns=['similarity_score'], inplace=True)     # drops the column becasue the next line of code will create the column again
    filtered_NFL_Combine_Date .insert(loc=1, column='similarity_score', value=distances[0])     # adds the euclidean distances to the current data frame of clean data as a new column

    filtered_NFL_Combine_Date['Pick'] = filtered_NFL_Combine_Date['Pick'].fillna(999)   # undrafted players have a pick number of 999 which will make them the floor automatically
    # creates the best 10 matches from the data set and then choses the floor (worst case) and ceiling (best case) of the prospects
    matches = filtered_NFL_Combine_Date.sort_values('similarity_score').head(10)    # the top 10 similarty scores to the data set of prospects    
    floor_index = matches['Pick'].idxmax()          # floor is the highest pick of the group     
    floor_Row = matches.loc[floor_index]
    ceiling_index = matches['Pick'].idxmin()       # ceiling is the lowest pick of the group
    ceiling_Row = matches.loc[ceiling_index] 

    return matches, floor_Row, ceiling_Row