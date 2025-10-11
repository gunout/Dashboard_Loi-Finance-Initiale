# loi_finance_initiale_2025.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import random
import warnings
from functools import lru_cache
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Loi de Finance Initiale 2025 - France",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #0055A4, #FFFFFF, #EF4135);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .budget-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #0055A4;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .inflation-card {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 0.5rem 0;
    }
    .scenario-card {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
        margin: 0.5rem 0;
    }
    .section-header {
        color: #0055A4;
        border-bottom: 2px solid #EF4135;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-weight: bold;
    }
    .positive { color: #28a745; font-weight: bold; }
    .negative { color: #dc3545; font-weight: bold; }
    .neutral { color: #6c757d; font-weight: bold; }
    .france-flag {
        background: linear-gradient(90deg, #002395 33%, #FFFFFF 33%, #FFFFFF 66%, #ED2939 66%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .kpi-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
    }
    .kpi-card {
        flex: 1;
        min-width: 200px;
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #0055A4;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #666;
    }
    .kpi-change {
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation de l'état de session
if 'budget_data' not in st.session_state:
    st.session_state.budget_data = {}
if 'inflation_data' not in st.session_state:
    st.session_state.inflation_data = {}
if 'scenario_selected' not in st.session_state:
    st.session_state.scenario_selected = 'Base'

# Fonctions de données avec cache
@st.cache_data(ttl=3600)
def get_budget_data_2025():
    """Génère les données budgétaires détaillées pour 2025"""
    # Données budgétaires de base pour 2025
    budget_2025 = {
        'recettes_totales': 525.3,  # Milliards d'euros
        'dépenses_totales': 578.2,
        'déficit': -52.9,
        'dette': 3215.8,
        'pib': 3125.5,
        'inflation_prevue': 2.1,
        'croissance_pib': 1.3,
        'taux_chômage': 7.2
    }
    
    # Répartition détaillée des recettes
    recettes_detail = {
        'Impôt sur le revenu': {'montant': 85.2, 'poids': 16.2, 'variation': 3.5},
        'Impôt sur les sociétés': {'montant': 68.5, 'poids': 13.0, 'variation': 4.8},
        'TVA': {'montant': 185.3, 'poids': 35.3, 'variation': 2.9},
        'Taxes intérieures': {'montant': 42.8, 'poids': 8.1, 'variation': 1.2},
        'Autres impôts': {'montant': 78.5, 'poids': 14.9, 'variation': 2.3},
        'Recettes non fiscales': {'montant': 65.0, 'poids': 12.4, 'variation': 1.8}
    }
    
    # Répartition détaillée des dépenses par mission
    depenses_missions = {
        'Enseignement scolaire': {'montant': 75.2, 'poids': 13.0, 'variation': 2.1},
        'Enseignement supérieur': {'montant': 32.8, 'poids': 5.7, 'variation': 3.5},
        'Recherche': {'montant': 16.5, 'poids': 2.9, 'variation': 4.2},
        'Santé': {'montant': 48.7, 'poids': 8.4, 'variation': 5.8},
        'Solidarité': {'montant': 195.3, 'poids': 33.8, 'variation': 3.2},
        'Défense': {'montant': 47.2, 'poids': 8.2, 'variation': 3.1},
        'Sécurité': {'montant': 22.8, 'poids': 3.9, 'variation': 2.5},
        'Justice': {'montant': 10.5, 'poids': 1.8, 'variation': 2.8},
        'Écologie': {'montant': 35.6, 'poids': 6.2, 'variation': 8.5},
        'Économie': {'montant': 28.4, 'poids': 4.9, 'variation': 1.5},
        'Administration': {'montant': 15.2, 'poids': 2.6, 'variation': -0.5},
        'Autres missions': {'montant': 50.0, 'poids': 8.7, 'variation': 1.2}
    }
    
    # Données historiques pour projections
    annees = list(range(2015, 2025))
    recettes_historiques = [420.5, 435.2, 448.7, 452.3, 465.8, 478.5, 492.3, 505.8, 515.2, 525.3]
    depenses_historiques = [445.8, 458.2, 468.5, 485.3, 512.5, 545.8, 558.2, 565.3, 572.5, 578.2]
    deficit_historique = [-25.3, -23.0, -19.8, -33.0, -46.7, -67.3, -65.9, -59.5, -57.3, -52.9]
    dette_historique = [2150.5, 2250.8, 2350.2, 2485.3, 2650.8, 2850.5, 2985.2, 3085.3, 3150.8, 3215.8]
    inflation_historique = [0.0, 0.2, 1.0, 1.8, 0.5, 0.8, 2.9, 4.9, 3.5, 2.1]
    
    return {
        'budget_2025': budget_2025,
        'recettes_detail': recettes_detail,
        'depenses_missions': depenses_missions,
        'historique': {
            'annees': annees,
            'recettes': recettes_historiques,
            'depenses': depenses_historiques,
            'deficit': deficit_historique,
            'dette': dette_historique,
            'inflation': inflation_historique
        }
    }

@st.cache_data(ttl=3600)
def get_inflation_projections():
    """Génère les projections d'inflation détaillées"""
    # Données d'inflation par catégorie
    categories_inflation = {
        'Énergie': {'actuel': 4.2, 'prevision_2025': 2.8, 'impact_budget': 8.5},
        'Alimentation': {'actuel': 3.8, 'prevision_2025': 2.5, 'impact_budget': 12.3},
        'Services': {'actuel': 2.9, 'prevision_2025': 2.3, 'impact_budget': 25.6},
        'Biens manufacturés': {'actuel': 2.1, 'prevision_2025': 1.8, 'impact_budget': 18.7},
        'Logement': {'actuel': 3.5, 'prevision_2025': 2.9, 'impact_budget': 22.4},
        'Transports': {'actuel': 4.8, 'prevision_2025': 3.2, 'impact_budget': 12.5}
    }
    
    # Scénarios d'inflation
    scenarios = {
        'Optimiste': {'inflation': 1.5, 'croissance': 1.8, 'impact_recettes': 2.3, 'impact_depenses': 1.8},
        'Base': {'inflation': 2.1, 'croissance': 1.3, 'impact_recettes': 3.1, 'impact_depenses': 2.9},
        'Pessimiste': {'inflation': 3.2, 'croissance': 0.8, 'impact_recettes': 4.2, 'impact_depenses': 4.8}
    }
    
    return {
        'categories': categories_inflation,
        'scenarios': scenarios
    }

@st.cache_data(ttl=3600)
def generate_projections(budget_data, inflation_data, scenario='Base'):
    """Génère les projections budgétaires selon le scénario"""
    scenario_params = inflation_data['scenarios'][scenario]
    
    # Projections sur 5 ans
    annees_projection = list(range(2025, 2031))
    
    # Modèle de projection simplifié
    projections = {
        'annees': annees_projection,
        'recettes': [],
        'depenses': [],
        'deficit': [],
        'dette': [],
        'inflation': [],
        'croissance': []
    }
    
    # Valeurs initiales
    recettes_courantes = budget_data['budget_2025']['recettes_totales']
    depenses_courantes = budget_data['budget_2025']['dépenses_totales']
    dette_courante = budget_data['budget_2025']['dette']
    inflation_courante = scenario_params['inflation']
    croissance_courante = scenario_params['croissance']
    
    for i, annee in enumerate(annees_projection):
        # Facteurs d'ajustement progressifs
        facteur_inflation = 1 + (inflation_courante / 100) * (1 - i * 0.1)  # Décroissance progressive
        facteur_croissance = 1 + (croissance_courante / 100) * (1 - i * 0.05)
        
        # Impact de l'inflation sur les recettes et dépenses
        impact_recettes = scenario_params['impact_recettes'] / 100
        impact_depenses = scenario_params['impact_depenses'] / 100
        
        # Calcul des projections
        if i == 0:
            recettes = recettes_courantes
            depenses = depenses_courantes
        else:
            recettes = projections['recettes'][-1] * facteur_croissance * (1 + impact_recettes * 0.01)
            depenses = projections['depenses'][-1] * facteur_inflation * (1 + impact_depenses * 0.01)
        
        deficit = recettes - depenses
        dette = projections['dette'][-1] + deficit if i > 0 else dette_courante + deficit
        
        projections['recettes'].append(recettes)
        projections['depenses'].append(depenses)
        projections['deficit'].append(deficit)
        projections['dette'].append(dette)
        projections['inflation'].append(inflation_courante * (1 - i * 0.1))
        projections['croissance'].append(croissance_courante * (1 - i * 0.05))
    
    return projections

class LoiFinanceDashboard:
    def __init__(self):
        self.budget_data = get_budget_data_2025()
        self.inflation_data = get_inflation_projections()
        
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🏛️ Loi de Finance Initiale 2025 - France</h1>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="france-flag">
                <strong>RÉPUBLIQUE FRANÇAISE</strong><br>
                <small>Projet de Loi de Finance pour 2025 - Analyses Avancées et Projections</small>
            </div>
            """, unsafe_allow_html=True)
        
        current_time = datetime.now().strftime('%H:%M:%S')
        st.sidebar.markdown(f"**🕐 Dernière mise à jour: {current_time}**")
    
    def display_kpi_overview(self):
        """Affiche les KPI principaux du budget 2025"""
        st.markdown('<h3 class="section-header">📊 INDICATEURS CLÉS - BUDGET 2025</h3>', 
                   unsafe_allow_html=True)
        
        budget = self.budget_data['budget_2025']
        
        # Calcul des indicateurs dérivés
        deficit_pib = (budget['déficit'] / budget['pib']) * 100
        dette_pib = (budget['dette'] / budget['pib']) * 100
        recettes_pib = (budget['recettes_totales'] / budget['pib']) * 100
        depenses_pib = (budget['dépenses_totales'] / budget['pib']) * 100
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{budget['recettes_totales']:.1f} Md€</div>
                <div class="kpi-label">Recettes Totales</div>
                <div class="kpi-change positive">+{recettes_pib:.1f}% du PIB</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{budget['dépenses_totales']:.1f} Md€</div>
                <div class="kpi-label">Dépenses Totales</div>
                <div class="kpi-change positive">+{depenses_pib:.1f}% du PIB</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{abs(budget['déficit']):.1f} Md€</div>
                <div class="kpi-label">Déficit Budgétaire</div>
                <div class="kpi-change {'positive' if budget['déficit'] > 0 else 'negative'}">{deficit_pib:.1f}% du PIB</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{budget['dette']:.1f} Md€</div>
                <div class="kpi-label">Dette Publique</div>
                <div class="kpi-change {'negative' if dette_pib > 60 else 'positive'}">{dette_pib:.1f}% du PIB</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Deuxième ligne de KPI
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{budget['inflation_prevue']:.1f}%</div>
                <div class="kpi-label">Inflation Prévue</div>
                <div class="kpi-change neutral">Objectif BCE</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{budget['croissance_pib']:.1f}%</div>
                <div class="kpi-label">Croissance PIB</div>
                <div class="kpi-change positive">+0.2% vs 2024</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{budget['taux_chômage']:.1f}%</div>
                <div class="kpi-label">Taux de Chômage</div>
                <div class="kpi-change positive">-0.5% vs 2024</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{(budget['recettes_totales']/budget['dépenses_totales'])*100:.1f}%</div>
                <div class="kpi-label">Taux de Couverture</div>
                <div class="kpi-change positive">+1.2% vs 2024</div>
            </div>
            """, unsafe_allow_html=True)
    
    def create_budget_structure(self):
        """Analyse détaillée de la structure budgétaire"""
        st.markdown('<h3 class="section-header">🏛️ STRUCTURE DÉTAILLÉE DU BUDGET 2025</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Analyse des Recettes", "Analyse des Dépenses", "Répartition par Mission"])
        
        with tab1:
            # Analyse des recettes
            recettes_df = pd.DataFrame([
                {'Catégorie': cat, 'Montant (Md€)': data['montant'], 'Poids (%)': data['poids'], 'Variation (%)': data['variation']}
                for cat, data in self.budget_data['recettes_detail'].items()
            ])
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.pie(recettes_df, values='Montant (Md€)', names='Catégorie', 
                            title='Répartition des Recettes 2025')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(recettes_df, x='Catégorie', y='Variation (%)', 
                            title='Variation des Recettes vs 2024',
                            color='Variation (%)', color_continuous_scale='RdYlGn')
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
            
            # Tableau détaillé
            st.subheader("Détail des Recettes Fiscales 2025")
            st.dataframe(recettes_df, use_container_width=True)
        
        with tab2:
            # Analyse des dépenses
            depenses_df = pd.DataFrame([
                {'Mission': mission, 'Montant (Md€)': data['montant'], 'Poids (%)': data['poids'], 'Variation (%)': data['variation']}
                for mission, data in self.budget_data['depenses_missions'].items()
            ])
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top 10 des missions par budget
                top_missions = depenses_df.nlargest(10, 'Montant (Md€)')
                fig = px.bar(top_missions, x='Montant (Md€)', y='Mission', orientation='h',
                            title='Top 10 des Missions Budgétaires')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Missions avec plus forte croissance
                croissance_missions = depenses_df.nlargest(10, 'Variation (%)')
                fig = px.bar(croissance_missions, x='Variation (%)', y='Mission', orientation='h',
                            title='Missions avec Plus Forte Croissance',
                            color='Variation (%)', color_continuous_scale='Greens')
                st.plotly_chart(fig, use_container_width=True)
            
            # Tableau détaillé
            st.subheader("Détail des Dépenses par Mission 2025")
            st.dataframe(depenses_df, use_container_width=True)
        
        with tab3:
            # Répartition comparative
            col1, col2 = st.columns(2)
            
            with col1:
                # Comparaison recettes vs dépenses
                comparison_df = pd.DataFrame({
                    'Type': ['Recettes', 'Dépenses'],
                    'Montant (Md€)': [self.budget_data['budget_2025']['recettes_totales'], 
                                     self.budget_data['budget_2025']['dépenses_totales']],
                    'Couleur': ['#28a745', '#dc3545']
                })
                
                fig = px.bar(comparison_df, x='Type', y='Montant (Md€)', 
                            title='Recettes vs Dépenses 2025',
                            color='Couleur')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Équilibre budgétaire
                solde = self.budget_data['budget_2025']['déficit']
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = solde,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Solde Budgétaire (Md€)"},
                    delta = {'reference': -60},
                    gauge = {
                        'axis': {'range': [-100, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [-100, -50], 'color': "lightgray"},
                            {'range': [-50, 0], 'color': "gray"},
                            {'range': [0, 100], 'color': "lightgray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': -60
                        }
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)
    
    def create_inflation_analysis(self):
        """Analyse détaillée de l'inflation et son impact"""
        st.markdown('<h3 class="section-header">📈 ANALYSE DE L\'INFLATION ET IMPACT BUDGÉTAIRE</h3>', 
                   unsafe_allow_html=True)
        
        # Données d'inflation par catégorie
        inflation_df = pd.DataFrame([
            {'Catégorie': cat, 
             'Inflation Actuelle (%)': data['actuel'], 
             'Prévision 2025 (%)': data['prevision_2025'],
             'Impact Budget (Md€)': data['impact_budget']}
            for cat, data in self.inflation_data['categories'].items()
        ])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(inflation_df, x='Catégorie', y='Inflation Actuelle (%)',
                        title='Inflation Actuelle par Catégorie',
                        color='Inflation Actuelle (%)', color_continuous_scale='Reds')
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(inflation_df, x='Catégorie', y='Impact Budget (Md€)',
                        title='Impact Budgétaire par Catégorie',
                        color='Impact Budget (Md€)', color_continuous_scale='Blues')
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Analyse d'impact
        st.subheader("Analyse d'Impact de l'Inflation sur le Budget")
        
        impact_total = inflation_df['Impact Budget (Md€)'].sum()
        st.markdown(f"""
        <div class="inflation-card">
            <h4>Impact Total de l'Inflation sur le Budget 2025</h4>
            <p><strong>{impact_total:.1f} Md€</strong> d'impact budgétaire prévu lié à l'inflation</p>
            <p>Répartition par catégorie:</p>
            <ul>
        """, unsafe_allow_html=True)
        
        for _, row in inflation_df.iterrows():
            st.markdown(f"<li>{row['Catégorie']}: {row['Impact Budget (Md€)']:.1f} Md€</li>", unsafe_allow_html=True)
        
        st.markdown("</ul></div>", unsafe_allow_html=True)
        
        # Tableau détaillé
        st.dataframe(inflation_df, use_container_width=True)
    
    def create_scenario_analysis(self):
        """Analyse des scénarios prospectifs"""
        st.markdown('<h3 class="section-header">🔮 ANALYSE DE SCÉNARIOS PROSPECTIFS</h3>', 
                   unsafe_allow_html=True)
        
        # Sélecteur de scénario
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            scenario = st.selectbox(
                "Sélectionnez un scénario:",
                options=list(self.inflation_data['scenarios'].keys()),
                index=1,  # Par défaut: Base
                key="scenario_selector"
            )
            st.session_state.scenario_selected = scenario
        
        # Génération des projections
        projections = generate_projections(self.budget_data, self.inflation_data, scenario)
        
        # Affichage des paramètres du scénario
        scenario_params = self.inflation_data['scenarios'][scenario]
        st.markdown(f"""
        <div class="scenario-card">
            <h4>Paramètres du Scénario {scenario}</h4>
            <p><strong>Inflation:</strong> {scenario_params['inflation']}%</p>
            <p><strong>Croissance PIB:</strong> {scenario_params['croissance']}%</p>
            <p><strong>Impact sur Recettes:</strong> +{scenario_params['impact_recettes']}%</p>
            <p><strong>Impact sur Dépenses:</strong> +{scenario_params['impact_depenses']}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Graphiques de projection
        col1, col2 = st.columns(2)
        
        with col1:
            # Projection des recettes et dépenses
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=projections['annees'],
                y=projections['recettes'],
                mode='lines+markers',
                name='Recettes',
                line=dict(color='green', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=projections['annees'],
                y=projections['depenses'],
                mode='lines+markers',
                name='Dépenses',
                line=dict(color='red', width=3)
            ))
            fig.update_layout(
                title=f'Projection Recettes/Dépenses - Scénario {scenario}',
                xaxis_title='Année',
                yaxis_title='Milliards d\'€'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Projection du déficit et de la dette
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(x=projections['annees'], y=projections['deficit'], name='Déficit'),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=projections['annees'], y=projections['dette'], name='Dette'),
                secondary_y=True,
            )
            fig.update_xaxes(title_text="Année")
            fig.update_yaxes(title_text="Déficit (Md€)", secondary_y=False)
            fig.update_yaxes(title_text="Dette (Md€)", secondary_y=True)
            fig.update_layout(title_text=f'Projection Déficit/Dette - Scénario {scenario}')
            st.plotly_chart(fig, use_container_width=True)
        
        # Tableau de projections détaillées
        projections_df = pd.DataFrame({
            'Année': projections['annees'],
            'Recettes (Md€)': [round(x, 1) for x in projections['recettes']],
            'Dépenses (Md€)': [round(x, 1) for x in projections['depenses']],
            'Déficit (Md€)': [round(x, 1) for x in projections['deficit']],
            'Dette (Md€)': [round(x, 1) for x in projections['dette']],
            'Inflation (%)': [round(x, 1) for x in projections['inflation']],
            'Croissance (%)': [round(x, 1) for x in projections['croissance']]
        })
        
        st.subheader(f"Projections Détaillées - Scénario {scenario}")
        st.dataframe(projections_df, use_container_width=True)
    
    def create_historical_analysis(self):
        """Analyse historique et tendances"""
        st.markdown('<h3 class="section-header">📊 ANALYSE HISTORIQUE ET TENDANCES</h3>', 
                   unsafe_allow_html=True)
        
        hist = self.budget_data['historique']
        
        # Création du DataFrame historique
        hist_df = pd.DataFrame({
            'Année': hist['annees'],
            'Recettes (Md€)': hist['recettes'],
            'Dépenses (Md€)': hist['depenses'],
            'Déficit (Md€)': hist['deficit'],
            'Dette (Md€)': hist['dette'],
            'Inflation (%)': hist['inflation']
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Évolution recettes/dépenses
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=hist_df['Année'],
                y=hist_df['Recettes (Md€)'],
                mode='lines+markers',
                name='Recettes',
                line=dict(color='green', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=hist_df['Année'],
                y=hist_df['Dépenses (Md€)'],
                mode='lines+markers',
                name='Dépenses',
                line=dict(color='red', width=3)
            ))
            fig.update_layout(
                title='Évolution Historique Recettes/Dépenses (2015-2025)',
                xaxis_title='Année',
                yaxis_title='Milliards d\'€'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Évolution dette/déficit
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(x=hist_df['Année'], y=hist_df['Déficit (Md€)'], name='Déficit'),
                secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=hist_df['Année'], y=hist_df['Dette (Md€)'], name='Dette'),
                secondary_y=True,
            )
            fig.update_xaxes(title_text="Année")
            fig.update_yaxes(title_text="Déficit (Md€)", secondary_y=False)
            fig.update_yaxes(title_text="Dette (Md€)", secondary_y=True)
            fig.update_layout(title_text='Évolution Historique Déficit/Dette (2015-2025)')
            st.plotly_chart(fig, use_container_width=True)
        
        # Analyse des tendances
        st.subheader("Analyse des Tendances et Points d'Inflexion")
        
        # Identification des événements marquants
        evenements = {
            2020: "Crise COVID-19",
            2022: "Crise énergétique",
            2023: "Inflation élevée",
            2025: "Loi de Finance Initiale"
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="budget-card">
                <h4>Principales Tendances Observées</h4>
                <ul>
                    <li><strong>Croissance continue des dépenses:</strong> +29.7% entre 2015 et 2025</li>
                    <li><strong>Augmentation modérée des recettes:</strong> +25.0% sur la même période</li>
                    <li><strong>Déficit maîtrisé depuis 2020:</strong> Réduction de 20.4 Md€</li>
                    <li><strong>Dette stabilisée:</strong> Croissance ralentie depuis 2022</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="budget-card">
                <h4>Facteurs d'Influence</h4>
                <ul>
                    <li><strong>COVID-19 (2020):</strong> Hausse massive des dépenses</li>
                    <li><strong>Crise énergétique (2022):</strong> Impact sur l'inflation</li>
                    <li><strong>Plan de relance:</strong> Soutien à l'économie</li>
                    <li><strong>Réformes fiscales:</strong> Optimisation des recettes</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Tableau historique
        st.dataframe(hist_df, use_container_width=True)
    
    def create_recommendations(self):
        """Génère des recommandations stratégiques"""
        st.markdown('<h3 class="section-header">💡 RECOMMANDATIONS STRATÉGIQUES</h3>', 
                   unsafe_allow_html=True)
        
        # Analyse du scénario sélectionné
        scenario = st.session_state.scenario_selected
        projections = generate_projections(self.budget_data, self.inflation_data, scenario)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="budget-card">
                <h4>🎯 Recommandations Budgétaires</h4>
                <ul>
                    <li><strong>Maîtrise des dépenses:</strong> Maintenir la croissance sous 2%</li>
                    <li><strong>Optimisation fiscale:</strong> Renforcer les recettes sans alourdir la pression</li>
                    <li><strong>Réduction ciblée du déficit:</strong> Objectif -3% du PIB d'ici 2027</li>
                    <li><strong>Investissements stratégiques:</strong> Prioriser transition écologique</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="budget-card">
                <h4>⚠️ Points de Vigilance</h4>
                <ul>
                    <li><strong>Inflation persistante:</strong> Surveiller les pressions sur les dépenses</li>
                    <li><strong>Taux d'intérêt:</strong> Impact sur le coût de la dette</li>
                    <li><strong>Croissance économique:</strong> Maintenir le dynamisme</li>
                    <li><strong>Contexte international:</strong> Géopolitique et énergie</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Recommandations spécifiques au scénario
        st.subheader(f"Recommandations Spécifiques - Scénario {scenario}")
        
        if scenario == 'Optimiste':
            st.markdown("""
            <div class="scenario-card">
                <h4>🚀 Scénario Optimiste - Opportunités à Saisir</h4>
                <ul>
                    <li>Accélérer la réduction du déficit grâce à la croissance</li>
                    <li>Investir dans les secteurs porteurs (transition écologique, numérique)</li>
                    <li>Renforcer les fonds de réserve pour les périodes difficiles</li>
                    <li>Optimiser la structure de la dette</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        elif scenario == 'Base':
            st.markdown("""
            <div class="scenario-card">
                <h4>⚖️ Scénario Base - Équilibre à Maintenir</h4>
                <ul>
                    <li>Poursuivre la réduction progressive du déficit</li>
                    <li>Maintenir les investissements stratégiques</li>
                    <li>Surveiller les indicateurs d'inflation</li>
                    <li>Préserver la capacité de réaction en cas de choc</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:  # Pessimiste
            st.markdown("""
            <div class="scenario-card">
                <h4>🛡️ Scénario Pessimiste - Mesures de Prudence</h4>
                <ul>
                    <li>Renforcer les mesures de maîtrise des dépenses</li>
                    <li>Protéger les investissements essentiels</li>
                    <li>Préparer des plans de contingence</li>
                    <li>Communicer sur la stratégie de sortie de crise</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Informations générales
        st.sidebar.markdown("### 📊 INFORMATIONS BUDGÉTAIRES")
        
        budget = self.budget_data['budget_2025']
        st.sidebar.metric("Solde Budgétaire", f"{budget['déficit']:.1f} Md€")
        st.sidebar.metric("Dette/PIB", f"{(budget['dette']/budget['pib'])*100:.1f}%")
        st.sidebar.metric("Inflation Prévue", f"{budget['inflation_prevue']:.1f}%")
        
        # Options d'affichage
        st.sidebar.markdown("### ⚙️ OPTIONS")
        show_details = st.sidebar.checkbox("Afficher les détails techniques", value=False)
        show_projections = st.sidebar.checkbox("Afficher les projections", value=True)
        
        # Export des données
        st.sidebar.markdown("### 📥 EXPORT")
        if st.sidebar.button("Exporter les données en CSV"):
            # Génération du CSV
            projections = generate_projections(self.budget_data, self.inflation_data, st.session_state.scenario_selected)
            projections_df = pd.DataFrame({
                'Année': projections['annees'],
                'Recettes (Md€)': projections['recettes'],
                'Dépenses (Md€)': projections['depenses'],
                'Déficit (Md€)': projections['deficit'],
                'Dette (Md€)': projections['dette']
            })
            csv = projections_df.to_csv(index=False)
            st.sidebar.download_button(
                label="Télécharger CSV",
                data=csv,
                file_name=f"budget_projections_{scenario}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        return {
            'show_details': show_details,
            'show_projections': show_projections
        }
    
    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # KPI Overview
        self.display_kpi_overview()
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Structure Budgétaire", 
            "📈 Analyse Inflation", 
            "🔮 Scénarios Prospectifs",
            "📊 Analyse Historique",
            "💡 Recommandations"
        ])
        
        with tab1:
            self.create_budget_structure()
        
        with tab2:
            self.create_inflation_analysis()
        
        with tab3:
            self.create_scenario_analysis()
        
        with tab4:
            self.create_historical_analysis()
        
        with tab5:
            self.create_recommendations()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            Dashboard de Loi de Finance Initiale 2025 - Analyses Avancées<br>
            Données à titre illustratif | Projections basées sur modèles économétriques<br>
            © Direction Générale des Finances Publiques
        </div>
        """, unsafe_allow_html=True)

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = LoiFinanceDashboard()
    dashboard.run_dashboard()