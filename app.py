import streamlit as st
import pandas as pd

# Título
st.title("⚽ Análise H2H - Gol Marcado Primeiro")

# URLs dos arquivos no GitHub
home_url = 'https://raw.githubusercontent.com/scooby75/firstgoal/refs/heads/main/scored_first_home.csv'
away_url = 'https://raw.githubusercontent.com/scooby75/firstgoal/refs/heads/main/scored_first_away.csv'

# Carregamento dos dados
@st.cache_data
def load_home_data():
    df_home = pd.read_csv(home_url)
    df_home['Type'] = 'Home'
    return df_home

@st.cache_data
def load_away_data():
    df_away = pd.read_csv(away_url)
    df_away['Type'] = 'Away'
    return df_away

home_df = load_home_data()
away_df = load_away_data()

# Lista de times disponíveis
teams_home = sorted(home_df['Team'].dropna().unique())
teams_away = sorted(away_df['Team'].dropna().unique())

# Seleção dos times
team1 = st.selectbox("Selecione o Time 1 (Mandante)", teams_home)
team2 = st.selectbox("Selecione o Time 2 (Visitante)", teams_away)

# Exibição de estatísticas individuais
def show_team_stats(team_name, df, tipo):
    stats = df[df['Team'] == team_name]
    if not stats.empty:
        st.markdown(f"### 📊 Estatísticas de {team_name} ({tipo})")
        st.dataframe(stats.reset_index(drop=True), use_container_width=True)
    else:
        st.warning(f"Nenhuma estatística encontrada para {team_name} ({tipo}).")

# Comparação H2H
if team1 and team2:
    if team1 == team2:
        st.warning("Os times devem ser diferentes para uma comparação H2H.")
    else:
        st.markdown("## ⚔️ Comparação Head-to-Head")
        col1, col2 = st.columns(2)

        with col1:
            show_team_stats(team1, home_df, "Mandante")

        with col2:
            show_team_stats(team2, away_df, "Visitante")
