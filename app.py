from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

popular_df = pickle.load(open('popular.pkl', 'rb'))
ptable = pickle.load(open('ptable.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)
df = pd.read_csv("final_ratings.csv")


@app.route('/')
def hello():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['Nos_Rating'].values),
                           rating=list(popular_df['avg_Rating'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    drop = sorted(df["Book-Title"].unique())
    return render_template('recommend.html', drop=drop)


@app.route('/recommend_books', methods=['post'])
def recommend():

    drop = sorted(df["Book-Title"].unique())
    user_input = request.form.get('user_input')
    index = np.where(ptable.index == user_input)[0][0]
    similar_items = sorted(
        list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    hold = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == ptable.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates(
            'Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates(
            'Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates(
            'Book-Title')['Image-URL-M'].values))

        hold.append(item)

    print(hold)

    
    return render_template('recommend.html',data = hold, drop=drop)


if __name__ == '__main__':
    app.run(debug=True)
