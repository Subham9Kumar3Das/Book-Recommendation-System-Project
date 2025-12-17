import streamlit as st
import pandas as pd
from recommender import get_popular_books, recommend

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Book Recommender",
    layout="wide"
)

st.title("📚 Book Recommendation System")

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_books():
    return pd.read_csv("Data/books.csv")

books = load_books()

# ------------------ SIDEBAR ------------------
st.sidebar.header("🔍 Options")

option = st.sidebar.radio(
    "Choose Action",
    ["Popular Books", "Search Book", "Recommend Book"]
)

# ------------------ POPULAR BOOKS ------------------
if option == "Popular Books":
    st.subheader("🔥 Popular Books")

    popular_books = get_popular_books()

    cols = st.columns(4)
    for i, row in popular_books.iterrows():
        with cols[i % 4]:
            st.image(row["Image-URL-M"], width=150)
            st.markdown(f"**{row['Book-Title']}**")
            st.text(row["Book-Author"])

# ------------------ SEARCH BOOK ------------------
elif option == "Search Book":
    st.subheader("🔎 Search Books")

    query = st.text_input("Enter book name")

    if query:
        query = query.lower().strip()

        matched_books = books[
            books["Book-Title"].str.lower().str.contains(query, na=False, regex=False)
        ]

        if matched_books.empty:
            query_words = query.split()
            matched_books = books[
                books["Book-Title"].str.lower().apply(
                    lambda title: all(word in title for word in query_words)
                )
            ]

        if matched_books.empty:
            st.warning("No books found ❌")
        else:
            st.success(f"Found {len(matched_books)} books")

            cols = st.columns(4)
            for i, row in matched_books.iterrows():
                with cols[i % 4]:
                    st.image(row["Image-URL-M"], width=150)
                    st.markdown(f"**{row['Book-Title']}**")
                    st.text(row["Book-Author"])

# ------------------ RECOMMEND BOOK ------------------
elif option == "Recommend Book":
    st.subheader("🤖 Recommend Similar Books")

    book_name = st.text_input("Enter a book name")

    if st.button("Recommend"):
        if not book_name.strip():
            st.warning("Please enter a book name")
        else:
            recommended_list = recommend(book_name.strip())

            if not recommended_list:
                st.error("No recommendations found ❌")
            else:
                st.success("Recommended Books")

                rec_df = pd.DataFrame(
                    recommended_list,
                    columns=["Book-Title", "Book-Author", "Image-URL-M"]
                )

                cols = st.columns(4)
                for i, row in rec_df.iterrows():
                    with cols[i % 4]:
                        st.image(row["Image-URL-M"], width=150)
                        st.markdown(f"**{row['Book-Title']}**")
                        st.text(row["Book-Author"])
