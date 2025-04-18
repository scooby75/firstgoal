import streamlit as st
import pandas as pd
import numpy as np
from math import exp, factorial
from itertools import product

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

# Função para calcular as odds justas com base nos PPG das equipes
def calcular_odds_justas(ppg_casa, ppg_fora):
    prob_casa = ppg_casa / 3  # Probabilidade da casa
    prob_fora = ppg_fora / 3  # Probabilidade do visitante
    odd_justa_casa = 1 / prob_casa
    odd_justa_fora = 1 / prob_fora
    return round(odd_justa_casa, 2), round(odd_justa_fora, 2)

# Função para calcular probabilidades de gols usando distribuição de Poisson
def calcular_prob_poisson(media_gols, max_gols=5):
    return [((media_gols ** x) * exp(-media_gols)) / factorial(x) for x in range(max_gols + 1)]

# Função para calcular os placares mais prováveis
def calcular_placares_mais_provaveis(ppg_casa, ppg_fora, max_gols=5):
    media_gols_casa = ppg_casa * 1.10  # Ajuste para casa
    media_gols_fora = ppg_fora * 0.90  # Ajuste para fora
    probs_casa = calcular_prob_poisson(media_gols_casa, max_gols)
    probs_fora = calcular_prob_poisson(media_gols_fora, max_gols)
    placares = {}
    for gols_casa, gols_fora in product(range(max_gols + 1), repeat=2):
        prob = probs_casa[gols_casa] * probs_fora[gols_fora]
        placares[(gols_casa, gols_fora)] = prob
    placares_ordenados = sorted(placares.items(), key=lambda x: x[1], reverse=True)
    return placares_ordenados

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
        # Calcular odds justas
        ppg_casa = display_stats['PPG'].mean() if local == 'Casa' else None
        ppg_fora = display_stats['PPG'].mean() if local == 'Fora' else None
        if ppg_casa and ppg_fora:
            odd_justa_casa, odd_justa_fora = calcular_odds_justas(ppg_casa, ppg_fora)
            st.write(f"**Odd Justa para a Casa**: {odd_justa_casa}")
            st.write(f"**Odd Justa para o Visitante**: {odd_justa_fora}")

        # Calculando as probabilidades de gols e os placares mais prováveis
        placares_provaveis = calcular_placares_mais_provaveis(ppg_casa, ppg_fora)
        st.markdown("#### 🏠 Placares Mais Prováveis para o Time da Casa Vencer:")
        for placar, prob in placares_provaveis[:4]:
            st.write(f"{placar[0]}x{placar[1]} com probabilidade de {prob:.2%}")
        st.markdown("#### 🚗 Placares Mais Prováveis para o Time Visitante Vencer:")
        for placar, prob in placares_provaveis[4:8]:
            st.write(f"{placar[0]}x{placar[1]} com probabilidade de {prob:.2%}")

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
