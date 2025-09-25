import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="IPL Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply the exact style from your notebook
plt.style.use('default')

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #ff6b6b;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="main-header">🏏 IPL Cricket Dashboard</div>', unsafe_allow_html=True)
st.write("Complete IPL match data analysis with all visualizations from the Jupyter notebook")

# Load and preprocess data (exactly as in your notebook)
@st.cache_data
def load_data():
    df = pd.read_csv("ipl_matches_summary.csv")
    
    # Display basic info (as in notebook)
    st.sidebar.subheader("Dataset Info")
    st.sidebar.text(f"Shape: {df.shape}")
    st.sidebar.text(f"Columns: {len(df.columns)}")
    
    # Convert date column to datetime format (exactly as in notebook)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Extract year from date (exactly as in notebook)
    df['year'] = df['date'].dt.year
    
    # Filter data for last 5 years (2019-2023) - exactly as in notebook
    df_recent = df[df['year'].between(2019, 2023)]
    
    # Handle missing values (exactly as in notebook)
    df_recent.fillna("Unknown", inplace=True)
    
    return df, df_recent

df, df_recent = load_data()

# Sidebar for filters
st.sidebar.header("🔧 Filters and Options")

# Display first few rows as in notebook
if st.sidebar.checkbox("Show Data Sample (as in notebook)"):
    st.sidebar.subheader("First 5 rows (like df.head())")
    st.sidebar.dataframe(df.head())

# Team selection
all_teams = list(set(list(df_recent['team_1'].unique()) + list(df_recent['team_2'].unique())))
selected_team = st.sidebar.selectbox("Select a Team", ["All Teams"] + sorted(all_teams))

# Season selection
seasons = sorted(df_recent['season'].unique(), reverse=True)
selected_seasons = st.sidebar.multiselect("Select Seasons", seasons, default=seasons)

# Apply season filter
if selected_seasons:
    filtered_df = df_recent[df_recent['season'].isin(selected_seasons)]
else:
    filtered_df = df_recent.copy()

# Apply team filter
if selected_team != "All Teams":
    team_matches = filtered_df[(filtered_df['team_1'] == selected_team) | (filtered_df['team_2'] == selected_team)]
else:
    team_matches = filtered_df.copy()

# Main content - Recreating all notebook visualizations exactly
st.markdown('<div class="section-header">📊 All Visualizations from Jupyter Notebook</div>', unsafe_allow_html=True)

# Tab layout
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 Exact Notebook Charts", "🏆 Team Analysis", "⭐ Player Analysis", "📈 Season Trends", "🔍 Data Explorer"])

with tab1:
    st.subheader("Exact Replica of Jupyter Notebook Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 1. Top Players by Player of Match Awards (EXACT replica)
        st.subheader("Top 10 Players (Player of the Match Awards)")
        st.write("**Exact replica of the notebook chart**")
        
        top_players = df_recent['player_of_match'].value_counts().head(10)
        
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        # Using the exact same parameters as your notebook
        sns.barplot(x=top_players.values, y=top_players.index, palette="viridis", ax=ax1)
        ax1.set_xlabel("Number of Awards")
        ax1.set_ylabel("Players")
        ax1.set_title("Top 10 Players (Player of the Match Awards)")
        plt.tight_layout()
        st.pyplot(fig1)
        
        # Display the exact data used
        with st.expander("Show data used for this chart"):
            st.dataframe(top_players)
    
    with col2:
        # 2. Team Wins Chart (EXACT replica)
        st.subheader("Top Teams by Wins")
        st.write("**Additional chart from notebook analysis**")
        
        team_wins = df_recent['match_winner'].value_counts().head(10)
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        # Using the exact same parameters
        sns.barplot(x=team_wins.index, y=team_wins.values, palette="coolwarm", ax=ax2)
        ax2.set_xlabel("Teams")
        ax2.set_ylabel("Number of Wins")
        ax2.set_title("Top 10 Teams by Number of Wins")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig2)
        
        with st.expander("Show data used for this chart"):
            st.dataframe(team_wins)

    # 3. Matches per Season (line chart as mentioned in your code)
    st.subheader("Matches per Season")
    st.write("**Matches distribution across seasons**")
    
    season_counts = df_recent['season'].value_counts().sort_index()
    
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    season_counts.plot(kind='line', marker='o', ax=ax3, color='blue', linewidth=2, markersize=8)
    ax3.set_title('Number of Matches per Season')
    ax3.set_xlabel('Season')
    ax3.set_ylabel('Number of Matches')
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig3)
    
    with st.expander("Show data used for this chart"):
        st.dataframe(season_counts)

with tab2:
    st.subheader("Team Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Win/Loss ratio for selected team
        if selected_team != "All Teams":
            st.subheader(f"Performance Analysis for {selected_team}")
            
            # Calculate metrics
            matches_played = len(team_matches)
            wins = len(team_matches[team_matches['match_winner'] == selected_team])
            losses = matches_played - wins
            win_percentage = (wins / matches_played) * 100 if matches_played > 0 else 0
            
            # Display metrics
            st.metric("Matches Played", matches_played)
            st.metric("Wins", wins)
            st.metric("Losses", losses)
            st.metric("Win Percentage", f"{win_percentage:.1f}%")
            
            # Win/Loss pie chart
            fig, ax = plt.subplots(figsize=(8, 8))
            labels = ['Wins', 'Losses']
            sizes = [wins, losses]
            colors = ['#4CAF50', '#F44336']
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            ax.set_title(f'{selected_team} - Win/Loss Distribution')
            st.pyplot(fig)
    
    with col2:
        # Toss analysis for selected team
        if selected_team != "All Teams":
            st.subheader(f"Toss Analysis for {selected_team}")
            
            # Toss wins
            toss_wins = len(team_matches[team_matches['toss_winner'] == selected_team])
            
            # Toss decision when team won toss
            team_toss_wins = team_matches[team_matches['toss_winner'] == selected_team]
            if len(team_toss_wins) > 0:
                toss_decisions = team_toss_wins['toss_decision'].value_counts()
                
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie(toss_decisions.values, labels=toss_decisions.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                ax.set_title(f'{selected_team} - Toss Decisions when Won Toss')
                st.pyplot(fig)
            
            st.metric("Times Won Toss", toss_wins)

with tab3:
    st.subheader("Player Performance Analysis")
    
    # Top players analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Player of match awards by season
        st.subheader("Player of Match Awards Trend")
        
        # Prepare data for top players across seasons
        top_players_list = df_recent['player_of_match'].value_counts().head(5).index
        
        player_trend_data = []
        for player in top_players_list:
            if player != "Unknown":
                player_data = df_recent[df_recent['player_of_match'] == player]
                awards_by_season = player_data['season'].value_counts().sort_index()
                for season, count in awards_by_season.items():
                    player_trend_data.append({'Player': player, 'Season': season, 'Awards': count})
        
        if player_trend_data:
            player_trend_df = pd.DataFrame(player_trend_data)
            fig = px.line(player_trend_df, x='Season', y='Awards', color='Player',
                         title='Top Players - Awards Trend Over Seasons',
                         markers=True)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Player search functionality
        st.subheader("Player Performance Search")
        
        all_players = df_recent['player_of_match'].unique()
        selected_player = st.selectbox("Select a Player", 
                                     ["Select a player"] + sorted([p for p in all_players if p != "Unknown"]))
        
        if selected_player != "Select a player":
            player_stats = df_recent[df_recent['player_of_match'] == selected_player]
            awards_count = len(player_stats)
            
            st.write(f"**{selected_player}**")
            st.metric("Player of Match Awards", awards_count)
            
            # Awards by season
            awards_by_season = player_stats['season'].value_counts().sort_index()
            fig, ax = plt.subplots(figsize=(10, 4))
            awards_by_season.plot(kind='bar', ax=ax, color='orange')
            ax.set_title(f'{selected_player} - Awards by Season')
            ax.set_xlabel('Season')
            ax.set_ylabel('Number of Awards')
            plt.xticks(rotation=45)
            st.pyplot(fig)

with tab4:
    st.subheader("Season Trends and Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Venue popularity by season
        st.subheader("Venue Usage Trend")
        
        venue_trends = df_recent.groupby(['season', 'venue']).size().reset_index(name='matches')
        top_venues = df_recent['venue'].value_counts().head(5).index
        
        fig = px.line(venue_trends[venue_trends['venue'].isin(top_venues)], 
                     x='season', y='matches', color='venue',
                     title='Top Venues Usage Over Seasons',
                     markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Toss impact analysis
        st.subheader("Toss Impact on Match Results")
        
        # Calculate toss winner match winner correlation
        toss_win_match_win = len(df_recent[df_recent['toss_winner'] == df_recent['match_winner']])
        total_matches = len(df_recent)
        toss_win_match_lose = total_matches - toss_win_match_win
        
        labels = ['Toss Winner Won', 'Toss Winner Lost']
        values = [toss_win_match_win, toss_win_match_lose]
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#66BB6A', '#EF5350'])
        ax.axis('equal')
        ax.set_title('Toss Winner vs Match Winner')
        st.pyplot(fig)
        
        win_percentage = (toss_win_match_win / total_matches) * 100
        st.metric("Toss Winner Win Percentage", f"{win_percentage:.1f}%")

with tab5:
    st.subheader("Data Exploration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Interactive data table
        st.subheader("Filtered Match Data")
        
        # Add filters for the data table
        st.write("**Apply additional filters to the data:**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            venue_filter = st.selectbox("Filter by Venue", ["All Venues"] + list(df_recent['venue'].unique()))
        with col2:
            toss_decision_filter = st.selectbox("Filter by Toss Decision", 
                                              ["All Decisions"] + list(df_recent['toss_decision'].unique()))
        with col3:
            result_filter = st.selectbox("Filter by Result", 
                                       ["All Results"] + list(df_recent['match_winner'].unique()))
        
        # Apply filters
        filtered_table = filtered_df.copy()
        if venue_filter != "All Venues":
            filtered_table = filtered_table[filtered_table['venue'] == venue_filter]
        if toss_decision_filter != "All Decisions":
            filtered_table = filtered_table[filtered_table['toss_decision'] == toss_decision_filter]
        if result_filter != "All Results":
            filtered_table = filtered_table[filtered_table['match_winner'] == result_filter]
        
        st.dataframe(filtered_table, height=400)
    
    with col2:
        # Quick stats
        st.subheader("Dataset Statistics")
        
        st.metric("Total Matches", len(filtered_df))
        st.metric("Unique Teams", len(all_teams))
        st.metric("Seasons Covered", len(seasons))
        st.metric("Venues", len(df_recent['venue'].unique()))
        
        # Data quality info
        st.subheader("Data Quality")
        missing_data = df.isnull().sum().sum()
        st.metric("Missing Values in Original", missing_data)
        st.metric("Matches with Unknown Winner", 
                 len(df_recent[df_recent['match_winner'] == "Unknown"]))

# Additional exact replicas of notebook analyses
st.markdown("---")
st.markdown('<div class="section-header">📋 Additional Exact Replicas from Notebook</div>', unsafe_allow_html=True)

# Show the exact data processing steps from notebook
with st.expander("Show Data Processing Steps (as in notebook)"):
    st.write("**Original dataset info (like df.info()):**")
    st.text(f"RangeIndex: {len(df)} entries, 0 to {len(df)-1}")
    st.text(f"Data columns: {len(df.columns)} columns")
    
    st.write("**First 5 rows (like df.head()):**")
    st.dataframe(df.head())
    
    st.write("**Recent data (2019-2023) head:**")
    st.dataframe(df_recent.head())

# Footer
st.markdown("---")
st.markdown("### 📝 About this Dashboard")
st.markdown("""
This dashboard replicates **all visualizations** from your Jupyter notebook exactly, with additional interactive features.

**Charts included:**
- Top 10 Players by Player of Match Awards (exact replica)
- Team performance charts
- Season trend analysis
- Toss impact analysis
- And all other visualizations from your notebook

The charts use the **same styling, colors, and formatting** as your original Jupyter notebook.
""")

# Add download option
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Export Options")

if st.sidebar.button("Download Recent Data (2019-2023) as CSV"):
    csv = df_recent.to_csv(index=False)
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"ipl_recent_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )

if st.sidebar.button("Download Full Dataset as CSV"):
    csv = df.to_csv(index=False)
    st.sidebar.download_button(
        label="Download Full CSV",
        data=csv,
        file_name=f"ipl_full_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )