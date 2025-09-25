# 🏏 IPL Team Analysis Dashboard

A dynamic **Streamlit web application** for analyzing IPL cricket match data from 2019–2023 with interactive visualizations and team/player performance insights.

[Watch Demo](Recording 2025-09-26 025415.mp4)
**Demo:**  
![Demo GIF](images/demo.gif)

---

## 📊 Features

- **Interactive Visualizations**: All graphs from Jupyter notebook rendered dynamically.
- **Team Analysis**: Compare team performance metrics over multiple seasons.
- **Player Statistics**: Top performers, award winners, and player trends.
- **Season Trends**: Analyze match patterns across different seasons.
- **Toss Analysis**: See how toss decisions impact match outcomes.
- **Data-Driven Insights**: Based on IPL match data (`ipl_matches_summary.csv`).

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip package manager
- Streamlit library

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/vaibhav-belekar/IPL-TEAM-ANALYSIS.git
cd IPL-TEAM-ANALYSIS
Create a virtual environment (recommended)

bash
Copy code
python -m venv venv
Activate the environment

bash
Copy code
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
Install dependencies

bash
Copy code
pip install -r requirements.txt
Run the Streamlit app

bash
Copy code
streamlit run app.py
Open your browser at http://localhost:8501 to see the dashboard.

🗂️ Project Structure
bash
Copy code
IPL-TEAM-ANALYSIS/
│
├── app.py                  # Main Streamlit app
├── ipl5.ipynb              # Jupyter notebook with analysis
├── ipl5.py                 # Python scripts for data processing
├── ipl_matches_summary.csv # IPL dataset
├── images/                 # Screenshots and GIF
│   └── demo.gif            # Demo GIF
├── requirements.txt        # Python dependencies
└── README.md
📈 Visualizations
Team performance by season

Player statistics and awards

Toss decision impact on outcomes

Match outcome trends over years

Comparison of top teams and players

🔗 Useful Links
GitHub Repository

Streamlit Documentation

IPL Official Website

🎯 Future Enhancements
Add live IPL score updates.

Implement player comparison tool.

Add predictive analysis using ML for match outcomes.

Mobile-responsive dashboard design.

📝 License
This project is licensed under the MIT License. See the LICENSE file for details.
