import streamlit as st
import pandas as pd

# Título
st.title("Análise H2H - First Goal")

# Função para pré-processar os dados
def preprocess_df(df, team_col):
    # Extrai valores de 'X out of Y' da coluna Matches
    matches_extracted = df['Matches'].str.extract(r'(\d+)\s+out of\s+(\d+)')
    df['Matches_Relevant'] = matches_extracted[0].astype(float)
    df['Matches_Total'] = matches_extracted[1].astype(float)

    # Extrai gols marcados (primeiro número de "X - Y")
    df['Goals_For'] = df['Goals'].str.extract(r'(\d+)').astype(float)

    # Calcula média de gols por partida relevante
    df['AVG_Goals'] = (df['Goals_For'] / df['Matches_Total']).round(2)

    # Porcentagem de jogos em que marcou primeiro
    df['First_Goal'] = (df['Matches_Relevant'] / df['Matches_Total'] * 100).round(1)

    return df

# Carregamento dos dados do GitHub
@st.cache_data
def load_data():
    home_url = 'https://raw.githubusercontent.com/scooby75/firstgoal/main/scored_first_home.csv'
    away_url = 'https://raw.githubusercontent.com/scooby75/firstgoal/main/scored_first_away.csv'
    
    home_df = pd.read_csv(home_url)
    away_df = pd.read_csv(away_url)

    # Pré-processamento
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
        selected_cols = [
            'Matches_Total', 'First_Goal', 'AVG_Goals', 'PPG'
        ]
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
