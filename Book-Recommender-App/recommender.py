import pickle
import numpy as np

# Load data
popular_df = pickle.load(open("models/popular.pkl", "rb"))
pt = pickle.load(open("models/pt.pkl", "rb"))
books = pickle.load(open("models/books.pkl", "rb"))
similarity_scores = pickle.load(open("models/similarity_scores.pkl", "rb"))

def get_popular_books():
    """Returns top 50 popular books DataFrame"""
    return popular_df

def recommend(book_name):
    """Returns a list of recommended books [title, author, image_url]"""
    try:
        index = np.where(pt.index == book_name)[0][0]
    except IndexError:
        return []

    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:5]

    data = []
    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item = [
            temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0],
            temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0],
            temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0],
        ]
        data.append(item)

    return data
