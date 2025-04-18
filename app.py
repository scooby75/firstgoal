import streamlit as st
import pandas as pd
from itertools import product

# Título
st.title("Análise H2H - First Goal")

# Carregamento dos dados do GitHub
@st.cache_data
def load_data():
    home_url = 'https://raw.githubusercontent.com/scooby75/firstgoal/main/scored_first_home.csv'
    away_url = 'https://raw.githubusercontent.com/scooby75/firstgoal/main/scored_first_away.csv'
    
    home_df = pd.read_csv(home_url)
    away_df = pd.read_csv(away_url)
    
    return home_df, away_df

home_df, away_df = load_data()

# Seleção dos times com base nos respectivos arquivos
teams_home = sorted(home_df['Team_Home'].dropna().unique())
teams_away = sorted(away_df['Team_Away'].dropna().unique())

team1 = st.selectbox("Home", teams_home)
team2 = st.selectbox("Away", teams_away)

# Função para exibir estatísticas com colunas filtradas
def show_team_stats(team_name, df, col_name, local):
    stats = df[df[col_name] == team_name]
    if not stats.empty:
        st.markdown(f"### 📊 {team_name} ({local})")
        selected_cols = ['Matches', 'First_Gol', 'Goals', 'PPG']
        display_stats = stats[selected_cols] if all(col in stats.columns for col in selected_cols) else stats
        st.dataframe(display_stats.reset_index(drop=True))
    else:
        st.warning(f"Nenhuma estatística encontrada para {team_name} ({local})")

# Exibição comparativa e placares prováveis
if team1 and team2:
    st.markdown("## Head-to-Head")

    col1, col2 = st.columns(2)

    with col1:
        show_team_stats(team1, home_df, 'Team_Home', 'Casa')

    with col2:
        show_team_stats(team2, away_df, 'Team_Away', 'Fora')

    # Estimativa de placares mais prováveis com base em gols médios
    try:
        home_stats = home_df[home_df['Team_Home'] == team1].iloc[0]
        away_stats = away_df[away_df['Team_Away'] == team2].iloc[0]

        # Conversão segura para float
        home_goals = float(home_stats['Goals'])
        home_matches = float(home_stats['Matches'])
        away_goals = float(away_stats['Goals'])
        away_matches = float(away_stats['Matches'])

        # Cálculo de gols médios
        home_avg_goals = home_goals / home_matches if home_matches else 0
        away_avg_goals = away_goals / away_matches if away_matches else 0

        # Simulação dos placares prováveis até 4x4
        max_goals = 4
        scorelines = list(product(range(0, max_goals+1), repeat=2))

        # Calcula uma "distância" entre a expectativa e cada placar
        score_probs = []
        for hg, ag in scorelines:
            diff = abs(hg - home_avg_goals) + abs(ag - away_avg_goals)
            score_probs.append((hg, ag, diff))

        # Ordena do mais provável (menor diferença) para o menos provável
        score_probs_sorted = sorted(score_probs, key=lambda x: x[2])

        st.markdown("### 🔮 Estimativa de Placar Mais Provável (com base em gols médios)")
        for hg, ag, _ in score_probs_sorted[:5]:
            st.write(f"{team1} {hg} x {ag} {team2}")

    except Exception as e:
        st.error(f"Erro ao calcular os placares prováveis: {e}")
