# ============================================================
# app.py - Netflix Movie Recommendation System
# Streamlit Web App - Cinematic Dark Theme UI
# Run with: streamlit run app.py
# ============================================================
# Attempt to load environment variables from a .env file if python-dotenv is available;
# this avoids import errors in environments where python-dotenv is not installed.
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    # python-dotenv not installed or/or failed to load — proceed without it
    pass

import os
import streamlit as st
import pickle
import requests
import pandas as pd
import bz2
import time

# ============================================================
# Page config - MUST be first Streamlit call
# ============================================================
st.set_page_config(
    page_title="CineMatch · Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# Custom CSS - Cinematic dark theatre aesthetic
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #080808 !important;
    color: #e8e0d4 !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 40% at 50% -10%, rgba(180,50,30,0.18) 0%, transparent 70%),
        radial-gradient(ellipse 60% 30% at 80% 110%, rgba(120,40,20,0.12) 0%, transparent 60%),
        #080808 !important;
    min-height: 100vh;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
#MainMenu, footer, header { visibility: hidden; }

/* Hide ALL deprecation warnings */
[data-testid="stNotification"],
.stAlert,
div[data-baseweb="notification"],
div[role="alert"] { display: none !important; }

.block-container {
    max-width: 1200px !important;
    padding: 0 2rem 4rem !important;
}

.hero-wrap {
    text-align: center;
    padding: 5rem 1rem 3.5rem;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #c0392b;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(4rem, 10vw, 8rem);
    letter-spacing: 0.04em;
    line-height: 0.92;
    color: #f0ebe3;
    margin-bottom: 1.2rem;
    text-shadow: 0 2px 40px rgba(200,60,40,0.25);
}
.hero-title span { color: #e8372a; }
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    font-weight: 300;
    color: #7a746c;
    letter-spacing: 0.02em;
}

.divider {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(200,60,40,0.4), transparent);
    margin: 0 auto 3rem;
}

[data-testid="stSelectbox"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.3em !important;
    text-transform: uppercase !important;
    color: #7a746c !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stSelectbox"] > div > div {
    background: #141414 !important;
    border: 1px solid #2a2420 !important;
    border-radius: 4px !important;
    color: #e8e0d4 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
}
[data-testid="stSelectbox"] > div > div:hover,
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #c0392b !important;
    box-shadow: 0 0 0 3px rgba(192,57,43,0.12) !important;
}

[data-testid="stButton"] > button {
    width: 100%;
    background: #c0392b !important;
    color: #fff !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.28em !important;
    text-transform: uppercase !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    box-shadow: 0 4px 20px rgba(192,57,43,0.3) !important;
    margin-top: 0.75rem !important;
}
[data-testid="stButton"] > button:hover {
    background: #a93226 !important;
    box-shadow: 0 6px 28px rgba(192,57,43,0.45) !important;
}

.results-heading {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #7a746c;
    text-align: center;
    margin: 2.5rem 0 0.4rem;
}
.results-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(1.8rem, 4vw, 3rem);
    letter-spacing: 0.06em;
    color: #f0ebe3;
    text-align: center;
    margin-bottom: 2.5rem;
}
.results-title span { color: #e8372a; }

.movie-card-label {
    background: #111111;
    border: 1px solid #1e1a17;
    border-top: none;
    border-radius: 0 0 6px 6px;
    padding: 0.75rem 0.85rem 0.9rem;
}
.movie-rank {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    color: #c0392b;
    margin-bottom: 0.2rem;
}
.movie-name {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    font-weight: 500;
    color: #e8e0d4;
    line-height: 1.35;
}

[data-testid="stImage"] {
    border-radius: 6px 6px 0 0 !important;
    overflow: hidden !important;
    margin-bottom: 0 !important;
    border: 1px solid #1e1a17 !important;
    border-bottom: none !important;
}
[data-testid="stImage"] img {
    border-radius: 0 !important;
    display: block !important;
}

.site-footer {
    text-align: center;
    padding: 3rem 0 1.5rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #3a3530;
}
.site-footer span { color: #c0392b; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d0d0d; }
::-webkit-scrollbar-thumb { background: #2a2420; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #c0392b; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Load saved model files (cached — loads only once per session)
# ============================================================
@st.cache_resource
def load_models():
    movies_data = pickle.load(open('movies.pkl', 'rb'))
    data = bz2.BZ2File('similarity.pbz2', 'rb')
    sim_matrix = pickle.load(data)
    return movies_data, sim_matrix

movies, similarity = load_models()
movie_list = movies['title'].values

# ============================================================
# Load genre mapping for evaluation
# ============================================================
@st.cache_data
def load_genre_map():
    import ast
    try:
        df = pd.read_csv('tmdb_5000_movies.csv')
        def parse_genres(genre_str):
            try:
                return [i['name'] for i in ast.literal_eval(genre_str)]
            except:
                return []
        df['genres_clean'] = df['genres'].apply(parse_genres)
        return dict(zip(df['title'], df['genres_clean']))
    except Exception:
        return {}

genre_map = load_genre_map()

# UPDATED: Load the OMDb API Key instead of TMDB
API_KEY = os.environ.get("OMDB_API_KEY")
# HARDCODED FOR TESTING ONLY
# API_KEY = "a4ffab94"
# ============================================================
# Fetch a single poster — sequential with retries using OMDB
# ============================================================
def fetch_poster(movie_title):
    # UPDATED: OMDb uses the movie title and a different endpoint
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie_title}"

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 429:        # rate limited
                time.sleep(2 * (attempt + 1))
                continue

            if response.status_code == 200:
                data = response.json()
                # OMDb returns 'Response': 'True' if found, and a 'Poster' link
                if data.get('Response') == 'True' and data.get('Poster') and data.get('Poster') != 'N/A':
                    return data['Poster']

            # Got a response but no poster → stop retrying
            break

        except requests.exceptions.Timeout:
            time.sleep(1)
            continue
        except Exception:
            break

    # Return a clean "not available" placeholder image
    return "https://placehold.co/500x750/111111/444444?text=Poster%0ANot+Available"


# ============================================================
# Core recommendation function
# ============================================================
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances   = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies    = []
    recommended_posters   = []
    recommended_scores    = []

    for i in movies_list:
        title = movies.iloc[i[0]].title
        
        recommended_movies.append(title)
        
        # UPDATED: Pass the 'title' to fetch_poster instead of 'movie_id'
        recommended_posters.append(fetch_poster(title))
        
        match_percentage = round(i[1] * 100, 1)
        recommended_scores.append(match_percentage)

    return recommended_movies, recommended_posters, recommended_scores


# ============================================================
# UI — Hero
# ============================================================
st.markdown("""
<div class="hero-wrap">
    <p class="hero-eyebrow">WELCOME TO</p>
    <h1 class="hero-title">CINE<span>MATCH</span></h1>
    <p class="hero-sub">Discover films that share the soul of what you love</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ============================================================
# UI — Search panel (centred)
# ============================================================
_, col_mid, _ = st.columns([1, 2, 1])

with col_mid:
    selected_movie_name = st.selectbox(
        "PICK A MOVIE YOU LOVE",
        movie_list,
        index=0
    )
    recommend_btn = st.button("Find Similar Films")

# ============================================================
# UI — Results
# ============================================================
if recommend_btn:
    with st.spinner("Fetching recommendations..."):
        names, posters, scores = recommend(selected_movie_name)

    st.markdown(f"""
    <p class="results-heading">Recommended for you</p>
    <h2 class="results-title">Because you liked &nbsp;<span>{selected_movie_name}</span></h2>
    """, unsafe_allow_html=True)

    cols  = st.columns(5, gap="medium")
    ranks = ["PICK 01", "PICK 02", "PICK 03", "PICK 04", "PICK 05"]

    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)

            st.markdown(f"""
            <div class="movie-card-label">
                <p class="movie-rank">{ranks[idx]}</p>
                <p class="movie-name">{names[idx]}</p>
                <p style="color: #46d369; font-size: 13px; font-weight: bold; margin-top: 5px;">{scores[idx]}% Match</p>
            </div>
            """, unsafe_allow_html=True)

    # ============================================================
    # Real-time Evaluation Dashboard
    # ============================================================
    query_genres = set(genre_map.get(selected_movie_name, []))
    precisions = []
    recalls = []

    for name in names:
        rec_genres = set(genre_map.get(name, []))
        overlap = query_genres.intersection(rec_genres)
        p = len(overlap) / len(rec_genres) if rec_genres else 0.0
        r = len(overlap) / len(query_genres) if query_genres else 0.0
        precisions.append(p)
        recalls.append(r)

    avg_precision = round((sum(precisions) / len(precisions)) * 100, 1) if precisions else 0.0
    avg_recall = round((sum(recalls) / len(recalls)) * 100, 1) if recalls else 0.0
    avg_sim = round(sum(scores) / len(scores), 1) if scores else 0.0

    st.markdown(f"""
    <div class="metrics-container" style="background: #111111; border: 1px solid #1e1a17; border-radius: 6px; padding: 1.5rem; margin-top: 2.5rem; text-align: left;">
        <h3 style="font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; color: #f0ebe3; letter-spacing: 0.1em; margin-bottom: 1rem; border-bottom: 1px solid rgba(200,60,40,0.3); padding-bottom: 0.5rem;">📊 RECOMMENDATION SYSTEM EVALUATION METRICS</h3>
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
            <div style="flex: 1; min-width: 200px;">
                <p style="font-family: 'DM Sans', sans-serif; font-size: 0.75rem; letter-spacing: 0.1em; color: #7a746c; text-transform: uppercase;">Average Cosine Similarity</p>
                <p style="font-family: 'Bebas Neue', sans-serif; font-size: 2.2rem; color: #e8372a; margin-top: 0.2rem;">{avg_sim}% Match</p>
                <p style="font-family: 'DM Sans', sans-serif; font-size: 0.8rem; color: #5a544c; font-style: italic; margin-top: 0.3rem;">Measures metadata similarity of keywords, cast, crew, and description.</p>
            </div>
            <div style="flex: 1; min-width: 200px;">
                <p style="font-family: 'DM Sans', sans-serif; font-size: 0.75rem; letter-spacing: 0.1em; color: #7a746c; text-transform: uppercase;">Genre Precision@5</p>
                <p style="font-family: 'Bebas Neue', sans-serif; font-size: 2.2rem; color: #46d369; margin-top: 0.2rem;">{avg_precision}%</p>
                <p style="font-family: 'DM Sans', sans-serif; font-size: 0.8rem; color: #5a544c; font-style: italic; margin-top: 0.3rem;">Percentage of recommended movies' genres that match the query film's genres.</p>
            </div>
            <div style="flex: 1; min-width: 200px;">
                <p style="font-family: 'DM Sans', sans-serif; font-size: 0.75rem; letter-spacing: 0.1em; color: #7a746c; text-transform: uppercase;">Genre Recall@5</p>
                <p style="font-family: 'Bebas Neue', sans-serif; font-size: 2.2rem; color: #3498db; margin-top: 0.2rem;">{avg_recall}%</p>
                <p style="font-family: 'DM Sans', sans-serif; font-size: 0.8rem; color: #5a544c; font-style: italic; margin-top: 0.3rem;">Percentage of the query film's genres captured in the recommendations.</p>
            </div>
        </div>
        <div style="margin-top: 1rem; border-top: 1px solid rgba(42, 36, 32, 0.5); padding-top: 0.8rem;">
            <p style="font-family: 'DM Sans', sans-serif; font-size: 0.85rem; color: #7a746c; line-height: 1.4;">
                <strong>Evaluation Insight:</strong> In unsupervised recommendation systems, genre overlap (Precision and Recall) serves as an objective proxy for relevancy. Higher similarity ensures context matching, while balanced genre scores indicate consistent thematic overlap.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# UI — Footer
# ============================================================
st.markdown("""
<div class="site-footer">
    Built with <span>♥</span> 
            &nbsp;·&nbsp; Python &nbsp;·&nbsp; Scikit-learn
    &nbsp;·&nbsp; NLTK &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; OMDb API
</div>
""", unsafe_allow_html=True)