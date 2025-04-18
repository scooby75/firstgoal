import streamlit as st
import pandas as pd

# Título
st.title("⚽ Análise H2H - Gol Marcado Primeiro")

# Carregamento dos dados do GitHub (substitua pela URL bruta do seu repo)
@st.cache_data
def load_data():
    home_url = 'https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPOSITORIO/main/data/scored_first_home.csv'
    away_url = 'https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPOSITORIO/main/data/scored_first_away.csv'
    
    home_df = pd.read_csv(home_url)
    away_df = pd.read_csv(away_url)
    
    home_df['Type'] = 'Home'
    away_df['Type'] = 'Away'
    
    return pd.concat([home_df, away_df], ignore_index=True)

df = load_data()

# Seleção de times
teams = sorted(df['Team'].dropna().unique())
team1 = st.selectbox("Selecione o Time 1", teams)
team2 = st.selectbox("Selecione o Time 2", teams)

# Exibir dados
def show_team_stats(team_name):
    stats = df[df['Team'] == team_name]
    if not stats.empty:
        st.markdown(f"### 📊 Estatísticas de {team_name}")
        st.dataframe(stats.reset_index(drop=True))
    else:
        st.warning("Nenhuma estatística encontrada para este time.")

# Comparação H2H
if team1 and team2:
    st.markdown("## ⚔️ Comparação Head-to-Head")
    col1, col2 = st.columns(2)

    with col1:
        show_team_stats(team1)
    with col2:
        show_team_stats(team2)
