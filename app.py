import streamlit as st
import pandas as pd
import re

# Título
st.title("Análise H2H - First Goal")

# Função de extração e cálculo da média
def preprocess_df(df, team_col):
    # Extrai número de partidas de 'Matches' (antes do " out of")
    df['Matches'] = df['Matches'].str.extract(r'(\d+)').astype(float)

    # Extrai gols marcados da coluna 'Goals' (antes do " - ")
    df['Goals_For'] = df['Goals'].str.extract(r'(\d+)').astype(float)

    # Calcula a média
    df['AVG_Goals'] = (df['Goals_For'] / df['Matches']).round(2)
    return df

# Carregamento dos dados do GitHub
@st.cache_data
def load_data():
    home_url = 'https://raw.githubusercontent.com/scooby75/firstgoal/main/scored_first_home.csv'
    away_url = 'https://raw.githubusercontent.com/scooby75/firstgoal/main/scored_first_away.csv'
    
    home_df = pd.read_csv(home_url)
    away_df = pd.read_csv(away_url)

    home_df = preprocess_df(home_df, 'Team_Home')
    away_df = preprocess_df(away_df, 'Team_Away')

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
        st.markdown(f"### 📊 Estatísticas de {team_name} ({local})")
        selected_cols = ['Matches', 'First_Gol', 'PPG', 'AVG_Goals']
        display_stats = stats[selected_cols] if all(col in stats.columns for col in selected_cols) else stats
        st.dataframe(display_stats.reset_index(drop=True))
    else:
        st.warning(f"Nenhuma estatística encontrada para {team_name} ({local})")

# Exibição comparativa
if team1 and team2:
    st.markdown("## Head-to-Head")

    col1, col2 = st.columns(2)

    with col1:
        show_team_stats(team1, home_df, 'Team_Home', 'Casa')

    with col2:
        show_team_stats(team2, away_df, 'Team_Away', 'Fora')
