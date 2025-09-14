from flask import Flask, render_template, request
from recommender import get_popular_books, recommend
import pickle
import pandas as pd

# ✅ Load books dataset
books = pd.read_csv("Data/books.csv")

app = Flask(__name__)

@app.route('/')
def index():
    popular_books = get_popular_books()
    return render_template('index.html', books=popular_books)

@app.route('/recommend', methods=['GET', 'POST'])
def recommend_books():
    recommendations = pd.DataFrame(columns=["Book-Title", "Book-Author", "Image-URL-M"])  # Ensure empty DataFrame
    input_name = None

    if request.method == 'POST':
        input_name = request.form.get('book_name', '').strip()
        recommended_list = recommend(input_name)

        if recommended_list:
            recommendations = pd.DataFrame(recommended_list, columns=["Book-Title", "Book-Author", "Image-URL-M"])

    return render_template('recommend.html', recommendations=recommendations, input_name=input_name, books=books)

@app.route('/search')
def search():
    query = request.args.get('query', '').strip().lower()

    if not query:
        popular_books = get_popular_books()
        return render_template('index.html', books=popular_books)

    matched_books = books[books['Book-Title'].str.lower().str.contains(query, na=False, regex=False)]

    if matched_books.empty:
        # Try word-wise matching
        query_words = query.split()
        matched_books = books[books['Book-Title'].str.lower().apply(
            lambda title: all(word in title for word in query_words)
        )]

    matched_books = matched_books.copy()

    # Ensure 'num_ratings' column exists
    if 'num_ratings' not in matched_books.columns:
        matched_books['num_ratings'] = 0

    return render_template('index.html', books=matched_books)

if __name__ == '__main__':
    print("✅ Flask server is starting...")
    app.run(debug=True)