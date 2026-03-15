# 🎬 CineMatch — Movie Recommendation System

A content-based movie recommendation engine built with Python as an interactive web app. Enter any movie and instantly get 5 similar recommendations with posters — powered by NLP and cosine similarity on the TMDB 5000 dataset.

## 📸 Preview

> *(Add a screenshot of your app here after deployment)*
> `![App Screenshot](screenshot.png)`

---

## 🧠 How It Works

1. Each movie's **overview, genres, keywords, cast and director** are combined into a single `tags` string
2. Tags are **stemmed** using NLTK's PorterStemmer to normalize word forms
3. A **CountVectorizer** converts all tags into a 4806 × 5000 word-count matrix
4. **Cosine similarity** is computed between every pair of movies
5. Given a movie, the app returns the **top 5 most similar** movies by cosine score

---

## 🗂️ Project Structure

```
cinematch/
├── app.py                          # Streamlit web app
├── netflix_recommendation.py       # Full notebook logic (all steps)
├── movies.pkl                      # Preprocessed movie dataframe
├── similarity.pkl                  # Cosine similarity matrix
├── requirements.txt                # Python dependencies
└── README.md                       # You are here
```

---

## ⬇️ Downloads

You need **two dataset files** from Kaggle and **two model files** to run this project.

### 1. Dataset Files — from Google Drive

Download both CSV files and place them in the project root:

| File | Description | Link |
|------|-------------|------|
| `tmdb_5000_movies.csv` | Movie metadata (budget, genres, keywords, overview) | [⬇️ Download](https://drive.google.com/file/d/1s8UA56Rr6oklG_xa0jHWb3VvRDgPXLc2/view?usp=sharing) |
| `tmdb_5000_credits.csv` | Cast and crew information | [⬇️ Download](https://drive.google.com/file/d/1PwoVAndEObW0yRWYEiKLdp_8aXpY7Hs3/view?usp=sharing) |

### 2. Model Files — pkl files

If you don't want to run the notebook yourself, download the pre-built model files:

| File | Description | Link |
|------|-------------|------|
| `movies.pkl` | Preprocessed movie titles + tags | [⬇️ Download](https://drive.google.com/file/d/1uhPwVT4n2hwzoViV33hFqC4awIsc3F7u/view?usp=sharing) |
| `similarity.pkl` | 4806×4806 cosine similarity matrix | [⬇️ Download](https://drive.google.com/file/d/1Df7amtdQ_qeRe3cTc3yOuqYB7L3DP1uo/view?usp=sharing) |

> Place all downloaded files in the project root folder alongside `app.py`.

---

## 🚀 Run Locally

### Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/cinematch.git
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

### Step 4 — Add your TMDB API key

Open `app.py` and replace the API key on this line:

```python
API_KEY = "your_api_key_here"
```

Get a free key at → [themoviedb.org](https://www.themoviedb.org/settings/api)
*(Sign up → Settings → API → Create → Developer → Copy API Key v3)*

### Step 5 — Download the pkl files

Download `movies.pkl` and `similarity.pkl` from the links above and place them in the project root.

**Or generate them yourself** by running all cells in `netflix_recommendation.py` inside Jupyter:

```bash
pip install jupyter
jupyter notebook
# Open netflix_recommendation.py and run all cells
# This will generate movies.pkl and similarity.pkl automatically
```

### Step 6 — Launch the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Pandas & NumPy | Data manipulation |
| NLTK | Text stemming |
| Scikit-learn | CountVectorizer + Cosine Similarity |
| Streamlit | Web app framework |
| TMDB API | Fetching movie posters |

---

## 📦 Requirements

```
streamlit
pandas
numpy
scikit-learn
nltk
requests
```

Install with:
```bash
pip install -r requirements.txt
```


> **Note:** `similarity.pkl` is ~90MB. If GitHub rejects it, use [Git LFS](https://git-lfs.github.com/) or host it on Google Drive and load it in the app via `gdown`.

---

## 🙋 FAQ

**Q: The app loads but posters are missing?**
Your TMDB API key may not be activated yet. It can take up to 30 minutes after signup. Replace `API_KEY` in `app.py` with your key.

**Q: `similarity.pkl` is too large to push to GitHub?**
Use Git LFS:
```bash
brew install git-lfs       # Mac
git lfs install
git lfs track "*.pkl"
git add .gitattributes similarity.pkl
git commit -m "Add model via LFS"
git push
```

**Q: How do I regenerate the model files?**
Run all cells in `netflix_recommendation.py` in Jupyter Notebook. It will create fresh `movies.pkl` and `similarity.pkl` files.

---

## 👩‍💻 Author

**Gargi Joshi**
- GitHub: [@gargijoshi9](https://github.com/gargijoshi9)
- LinkedIn:[Gargi Joshi](https://www.linkedin.com/in/gargi-joshi-a9246b331/)

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

<p align="center">Built with ♥ using Python · Scikit-learn · NLTK · Streamlit · TMDB API</p>
