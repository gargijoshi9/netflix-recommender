
# 🎬 CineMatch — AI Movie Recommendation System

A semantic movie recommendation engine built with Python and Streamlit. Unlike standard genre-matchers, CineMatch uses **SentenceTransformers** to understand the actual "DNA" and context of a film. Enter any movie and instantly get 5 highly accurate recommendations with official posters.

## 📸 Preview

> <img src="Screenshot 2026-06-18 at 7.29.45 PM.jpg" alt="CineMatch App Interface" width="800"/>

---

## 🧠 How It Works (The AI Engine)

1. **Feature Engineering:** Each movie's overview, genres, keywords, cast, and director are combined into a single `tags` string. 
2. **Custom Weighting:** Metadata is mathematically weighted to improve accuracy (Director is weighted 3x, while Cast, Genres, and Keywords are weighted 2x).
3. **Text Normalization:** Tags are processed using NLTK's `PorterStemmer` to reduce words to their root forms.
4. **Semantic Vectorization:** A pre-trained **SentenceTransformer** (`all-MiniLM-L6-v2`) converts the structured text into dense semantic vector embeddings. 
5. **Cosine Similarity:** The model computes the distance between vectors, generating a massive 4,800 × 4,800 similarity matrix (over 23 million data points).

---

## 🗂️ Project Structure

```text
cinematch/
├── app.py                      # Streamlit web app & UI
├── netflix-recommender.ipynb   # Full Jupyter Notebook (Data cleaning & AI Model building)
├── movie_dict.pkl              # Preprocessed movie dictionary
├── similarity.pbz2             # Compressed Cosine Similarity Matrix
├── requirements.txt            # Python dependencies
└── README.md                   # You are here

```

---

## ⬇️ Downloads & Data

You need the TMDB 5000 dataset to train the model, and two exported model files to run the app.

### 1. Dataset Files (For the Jupyter Notebook)

If you want to train the AI yourself, download both CSV files and place them in the project root:

| File | Description | Link |
| --- | --- | --- |
| `tmdb_5000_movies.csv` | Movie metadata (budget, genres, keywords, overview) | [⬇️ Download](https://drive.google.com/file/d/1s8UA56Rr6oklG_xa0jHWb3VvRDgPXLc2/view?usp=sharing) |
| `tmdb_5000_credits.csv` | Cast and crew information | [⬇️ Download](https://drive.google.com/file/d/1PwoVAndEObW0yRWYEiKLdp_8aXpY7Hs3/view?usp=sharing) |

### 2. Model Files (For the Streamlit App)

If you just want to run the web app immediately, download the pre-built model files:

| File | Description |
| --- | --- |
| `movie_dict.pkl` | Preprocessed movie titles & IDs (Dictionary) |
| `similarity.pbz2` | BZ2 Compressed semantic similarity matrix |

> **Note on Compression:** The similarity matrix is massive. It is highly compressed using `bz2` (`.pbz2`) to bypass GitHub's 100MB file limit, completely eliminating the need for Git LFS!

---

## 🚀 Run Locally

### Step 1 — Clone the repository

```bash
git clone [https://github.com/YOUR_USERNAME/cinematch.git](https://github.com/YOUR_USERNAME/cinematch.git)
cd cinematch

```

### Step 2 — Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows

```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt

```

### Step 4 — Add your OMDb API key (Securely)

This app fetches posters via the **OMDb API** and uses Streamlit Secrets to keep your key safe.

1. Get a free API key at → [omdbapi.com](http://www.omdbapi.com/apikey.aspx)
2. Inside your project folder, create a hidden folder and file: `.streamlit/secrets.toml`
3. Add your key to the file exactly like this:

```toml
OMDB_API_KEY = "your_actual_api_key_here"

```

### Step 5 — Launch the app

```bash
streamlit run app.py

```

The app will open at `http://localhost:8501` with a sleek, cinematic dark-mode UI.

---

## 🛠️ Tech Stack

| Tool | Purpose |
| --- | --- |
| Python 3.10+ | Core language |
| Pandas & NumPy | Data manipulation & mathematical blending |
| SentenceTransformers | Generating semantic context-aware embeddings |
| Scikit-learn | Cosine Similarity computation |
| BZ2 | High-ratio spatial matrix compression |
| Streamlit | Web app framework & UI |
| OMDb API | Real-time movie poster fetching w/ retry logic |

---

## 🙋 FAQ

**Q: The app loads but posters are missing?**
Your OMDb API key might be incorrect, or you hit the daily rate limit. Ensure your key is properly placed in `.streamlit/secrets.toml` (if running locally) or in the Streamlit Cloud Dashboard Secrets (if deployed).

**Q: How do I regenerate the model files?**
Run all cells in `netflix-recommender.ipynb` in Jupyter Notebook. It will process the raw CSVs, apply the stemming and custom weights, download the AI model, and export fresh `movie_dict.pkl` and `similarity.pbz2` files.

---

## 👩‍💻 Author

**Gargi Joshi**

* GitHub: [@gargijoshi9](https://github.com/gargijoshi9)
* LinkedIn: [Gargi Joshi](https://www.linkedin.com/in/gargi-joshi-a9246b331/)

---

## 📄 License

This project is open source under the [MIT License](https://www.google.com/search?q=LICENSE).

---
