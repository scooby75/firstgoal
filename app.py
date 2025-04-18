import streamlit as st
import pandas as pd

# Título
st.title("⚽ Análise H2H - Gol Marcado Primeiro")

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

team1 = st.selectbox("🏠 Selecione o Time da Casa (Home)", teams_home)
team2 = st.selectbox("🚗 Selecione o Time Visitante (Away)", teams_away)

# Função para exibir estatísticas com colunas filtradas
def show_team_stats(team_name, df, col_name, local):
    stats = df[df[col_name] == team_name]
    if not stats.empty:
        st.markdown(f"### 📊 Estatísticas de {team_name} ({local})")
        selected_cols = ['Matches', 'First_Gol', 'PPG']
        # Verifica se as colunas existem antes de exibir
        display_stats = stats[selected_cols] if all(col in stats.columns for col in selected_cols) else stats
        # Garantir que 'PPG' seja numérico e não contenha NaN ou valores não numéricos
        display_stats['PPG'] = pd.to_numeric(display_stats['PPG'], errors='coerce')
        # Calculando a odd justa a partir do PPG, com verificação para evitar divisão por zero ou valores NaN
        display_stats['Odd Justa'] = display_stats['PPG'].apply(lambda x: 1 / x if pd.notna(x) and x > 0 else None)
        st.dataframe(display_stats.reset_index(drop=True))
    else:
        st.warning(f"Nenhuma estatística encontrada para {team_name} ({local})")

# Exibição comparativa
if team1 and team2:
    st.markdown("## ⚔️ Comparação Head-to-Head")

    col1, col2 = st.columns(2)

    with col1:
        show_team_stats(team1, home_df, 'Team_Home', 'Casa')

    with col2:
        show_team_stats(team2, away_df, 'Team_Away', 'Fora')
