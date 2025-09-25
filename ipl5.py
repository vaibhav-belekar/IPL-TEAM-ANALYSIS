#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd


# In[2]:


# Load the CSV file
ipl_df = pd.read_csv("ipl_matches_summary.csv")

# Display basic info
print(ipl_df.info())

# Show first few rows
ipl_df.head()


# In[3]:


# Convert date column to datetime format
ipl_df['date'] = pd.to_datetime(ipl_df['date'], errors='coerce')

# Extract year from date
ipl_df['year'] = ipl_df['date'].dt.year

# Filter data for last 5 years (2019-2023)
ipl_recent = ipl_df[ipl_df['year'].between(2019, 2023)]

# Handle missing values (if any)
ipl_recent.fillna("Unknown", inplace=True)

# Show cleaned data
ipl_recent.head()


# In[4]:


# Count player of match awards
top_players = ipl_recent['player_of_match'].value_counts().head(10)

# Plot top players
plt.figure(figsize=(10, 5))
sns.barplot(x=top_players.values, y=top_players.index, palette="viridis")
plt.xlabel("Number of Awards")
plt.ylabel("Players")
plt.title("Top 10 Players (Player of the Match Awards)")
plt.show()


# In[5]:


# Count match wins per team
team_wins = ipl_recent['match_winner'].value_counts()

# Plot team wins
plt.figure(figsize=(12, 6))
sns.barplot(x=team_wins.index, y=team_wins.values, palette="coolwarm")
plt.xticks(rotation=45)
plt.xlabel("Teams")
plt.ylabel("Number of Wins")
plt.title("IPL Team Wins (2019-2023)")
plt.show()


# In[6]:


# Count matches played at each venue
venue_counts = ipl_recent['venue'].value_counts().head(10)

# Plot venue analysis
plt.figure(figsize=(12, 6))
sns.barplot(x=venue_counts.values, y=venue_counts.index, palette="magma")
plt.xlabel("Number of Matches")
plt.ylabel("Venue")
plt.title("Top 10 IPL Venues (2019-2023)")
plt.show()


# In[7]:


# Compare toss winners vs match winners
toss_wins = ipl_recent[ipl_recent['toss_winner'] == ipl_recent['match_winner']]

# Calculate percentage of matches where toss winner also won
toss_impact = len(toss_wins) / len(ipl_recent) * 100
print(f"Toss Winning Impact on Match Outcome: {toss_impact:.2f}%")


# In[8]:


# Calculate Toss Winning Impact
toss_wins = ipl_recent[ipl_recent['toss_winner'] == ipl_recent['match_winner']]
toss_impact = [len(toss_wins), len(ipl_recent) - len(toss_wins)]

# Plot Pie Chart
plt.figure(figsize=(6, 6))
plt.pie(toss_impact, labels=["Toss Winner Also Won", "Toss Winner Lost"], autopct="%1.1f%%", colors=["green", "red"])
plt.title("Impact of Toss on Match Winning (2019-2023)")
plt.show()


# In[9]:


plt.figure(figsize=(10, 6))
sns.violinplot(x="year", y="toss_decision", data=ipl_recent, palette="coolwarm")
plt.xlabel("Year")
plt.ylabel("Toss Decision")
plt.title("Toss Decisions Distribution Over IPL Seasons")
plt.show()


# In[10]:


# Count Match Outcomes
outcome_counts = ipl_recent['match_winner'].fillna("No Result").value_counts()

# Plot Donut Chart
plt.figure(figsize=(8, 8))
plt.pie(outcome_counts, labels=outcome_counts.index, autopct="%1.1f%%", startangle=140, colors=sns.color_palette("pastel"), wedgeprops=dict(width=0.4))
plt.title("Match Results Distribution (2019-2023)")
plt.show()


# In[11]:


import plotly.express as px

# Ensure correct column name for year/season
year_col = "season" if "season" in ipl_recent.columns else "year"

# Group data by Year & Match Winner
wins_per_team = ipl_recent.groupby([year_col, "match_winner"]).size().reset_index(name="wins")

# Create Animated Line Chart
fig = px.line(
    wins_per_team, 
    x=year_col, 
    y="wins", 
    color="match_winner", 
    markers=True, 
    title="IPL Team Wins Trend Over 5 Seasons",
    animation_frame=year_col,
    line_shape="spline"  # Smoothens the lines
)

# 🎨 **Manually Set Animation Speed**
fig.update_layout(
    updatemenus=[{
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 1500, "redraw": True}, "fromcurrent": True}],
                "label": "▶ Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                "label": "❚❚ Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }]
)

# Improve Aesthetics
fig.update_traces(marker=dict(size=8))  # Increase marker size
fig.update_layout(
    xaxis_title="Season", 
    yaxis_title="Total Wins", 
    legend_title="Teams",
    transition={"duration": 800}  # Smooth transitions
)

fig.show()




# In[12]:


import seaborn as sns
import matplotlib.pyplot as plt

# Plot Ridge Plot
plt.figure(figsize=(10, 6))
sns.violinplot(x="year", y="match_winner", data=ipl_recent, palette="magma")
plt.xlabel("Year")
plt.ylabel("Team")
plt.title("Runs Distribution Across IPL Seasons")
plt.show()


# In[13]:


import plotly.express as px

# Aggregate Data: Count Wins per Team per Season
team_stats = ipl_recent.groupby(["season", "match_winner"]).size().reset_index(name="wins")

# Create Bubble Chart (Wins Over Time)
fig = px.scatter(
    team_stats, 
    x="season", 
    y="wins", 
    size="wins", 
    color="match_winner", 
    animation_frame="season",
    title="IPL Team Performance Over the Years (Based on Wins)",
    labels={"wins": "Total Wins", "season": "Year"},
    hover_name="match_winner",
    size_max=50
)

fig.show()


# In[14]:


import plotly.express as px

# Count Wins per Team per Year
team_wins_yearly = ipl_recent.groupby(["season", "match_winner"]).size().reset_index(name="wins")

# Animated Bar Chart Race
fig = px.bar(
    team_wins_yearly, 
    x="wins", 
    y="match_winner", 
    color="match_winner",
    animation_frame="season",
    orientation="h",
    title="IPL Team Wins Over the Years (Animated Bar Chart Race)",
    labels={"wins": "Total Wins", "match_winner": "Teams"},
)

fig.update_layout(xaxis_title="Total Wins", yaxis_title="Teams")
fig.show()


# In[15]:


import plotly.express as px

# Calculate Cumulative Wins
team_wins_yearly["cumulative_wins"] = team_wins_yearly.groupby("match_winner")["wins"].cumsum()

# Animated Line Chart
fig = px.line(
    team_wins_yearly, 
    x="season", 
    y="cumulative_wins", 
    color="match_winner",
    animation_frame="season",
    markers=True,
    title="Cumulative Wins by IPL Teams Over the Years",
    labels={"cumulative_wins": "Total Wins", "season": "Year"},
    line_shape="spline"  # Smooth lines
)

fig.show()


# In[16]:


import plotly.express as px

# Count Matches Played Per Team
matches_per_team = ipl_recent.groupby(["season", "match_winner"]).size().reset_index(name="wins")
matches_played = ipl_recent.groupby(["season", "team_1"]).size().reset_index(name="matches")

# Merge Wins & Matches Played
team_stats = matches_per_team.merge(matches_played, left_on=["season", "match_winner"], right_on=["season", "team_1"])
team_stats.drop(columns=["team_1"], inplace=True)

# Animated Scatter Plot (Wins vs. Matches)
fig = px.scatter(
    team_stats, 
    x="matches", 
    y="wins", 
    color="match_winner",
    animation_frame="season",
    size="wins",
    title="IPL Team Wins vs. Matches Played Over the Years",
    labels={"matches": "Total Matches Played", "wins": "Total Wins"},
    size_max=50
)

fig.show()


# In[17]:


import plotly.express as px

# Create a Pivot Table: Seasons vs. Teams (Total Wins)
heatmap_data = ipl_recent.groupby(["season", "match_winner"]).size().reset_index(name="wins")

# Heatmap Animation
fig = px.imshow(
    heatmap_data.pivot(index="match_winner", columns="season", values="wins"),
    color_continuous_scale="Viridis",
    title="IPL Team Performance Over Seasons (Heatmap)",
    labels=dict(x="Season", y="Teams", color="Total Wins"),
)

fig.show()


# In[18]:


import plotly.express as px

# Create sample data (as runs are missing, using wins)
team_stats = ipl_recent.groupby(["season", "match_winner"]).size().reset_index(name="wins")

# 3D Scatter Plot
fig = px.scatter_3d(
    team_stats, 
    x="season", 
    y="match_winner", 
    z="wins", 
    color="match_winner", 
    size="wins",
    title="3D IPL Team Performance: Wins Across Seasons",
    labels={"season": "Year", "match_winner": "Team", "wins": "Total Wins"}
)

fig.show()


# In[19]:


import plotly.express as px

# Group by Season → Team → Wins
sunburst_data = ipl_recent.groupby(["season", "match_winner"]).size().reset_index(name="wins")

# Sunburst Chart
fig = px.sunburst(
    sunburst_data, 
    path=["season", "match_winner"], 
    values="wins", 
    title="IPL Tournament Hierarchy: Wins Across Seasons",
    color="wins", 
    color_continuous_scale="Blues"
)

fig.show()


# In[ ]:




