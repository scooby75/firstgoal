import streamlit as st
import pandas as pd
import numpy as np
import math  # Importando o módulo math para usar a função factorial

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
        selected_cols = ['Matches', 'First_Gol', 'Goals', 'PPG']
        # Verifica se as colunas existem antes de exibir
        display_stats = stats[selected_cols] if all(col in stats.columns for col in selected_cols) else stats
        st.dataframe(display_stats.reset_index(drop=True))
    else:
        st.warning(f"Nenhuma estatística encontrada para {team_name} ({local})")

# Função para calcular a média de gols por jogo (PPG) a partir da coluna Goals
def calculate_ppg(goals_column, matches_column):
    # Extrai o número de gols marcados e os jogos disputados
    goals_for, goals_against = map(int, goals_column.split(' - '))
    matches_played = int(matches_column.split(' out of ')[0])  # Número de jogos disputados
    
    # Calcula a média de gols por jogo (PPG)
    return (goals_for + goals_against) / matches_played

# Função para calcular os 6 placares mais prováveis com base no PPG
def calculate_probable_scores(team1_ppg, team2_ppg):
    # Média de gols marcados por partida para cada time
    team1_goals = team1_ppg
    team2_goals = team2_ppg
    
    # Placar máximo que vamos considerar (ex: 5x5)
    max_goals = 5
    
    # Lista de possíveis placares
    scores = []
    
    # Calculando os placares possíveis com base na média de gols
    for home_goals in range(max_goals + 1):
        for away_goals in range(max_goals + 1):
            home_prob = np.exp(-team1_goals) * (team1_goals ** home_goals) / math.factorial(home_goals)
            away_prob = np.exp(-team2_goals) * (team2_goals ** away_goals) / math.factorial(away_goals)
            prob = home_prob * away_prob
            scores.append((home_goals, away_goals, prob))
    
    # Ordenando os placares pela probabilidade
    scores.sort(key=lambda x: x[2], reverse=True)
    
    # Retornando os 6 placares mais prováveis
    return scores[:6]

# Exibição comparativa
if team1 and team2:
    st.markdown("## ⚔️ Comparação Head-to-Head")

    col1, col2 = st.columns(2)

    with col1:
        show_team_stats(team1, home_df, 'Team_Home', 'Casa')

    with col2:
        show_team_stats(team2, away_df, 'Team_Away', 'Fora')

    # Calculando o PPG de cada time
    team1_row = home_df[home_df['Team_Home'] == team1]
    team2_row = away_df[away_df['Team_Away'] == team2]
    
    if not team1_row.empty and not team2_row.empty:
        # Calculando o PPG para o time da casa e o time visitante
        team1_ppg = calculate_ppg(team1_row['Goals'].values[0], team1_row['Matches'].values[0])
        team2_ppg = calculate_ppg(team2_row['Goals'].values[0], team2_row['Matches'].values[0])

        st.markdown("### 🔮 Placar Mais Provável")
        probable_scores = calculate_probable_scores(team1_ppg, team2_ppg)
        score_table = pd.DataFrame(probable_scores, columns=["Placar Casa", "Placar Visitante", "Probabilidade"])
        st.dataframe(score_table)
    else:
        st.warning("Não foi possível calcular os placares devido à falta de dados para as equipes.")
