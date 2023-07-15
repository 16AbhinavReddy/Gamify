import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from gensim.models import Word2Vec
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

def load_dataset():
    # Load the IMDb dataset
    df = pd.read_csv('imdb-videogames.csv')

    # Select the relevant features
    features = ['name', 'plot', 'url', 'votes', 'rating', 'certificate']

    # Remove any rows with missing values in selected features
    df = df[features].dropna()

    # Remove commas from the 'votes' column
    df['votes'] = df['votes'].str.replace(',', '')

    # Convert 'votes' column to numeric
    df['votes'] = pd.to_numeric(df['votes'], errors='coerce')

    return df


def preprocess_text(text):
    # Lowercase the text
    text = text.lower()

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words and token not in string.punctuation]

    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return tokens


def train_recommendation_system(df):
    # Preprocess the plot text
    df['processed_plot'] = df['plot'].apply(preprocess_text)

    # Train Word2Vec model
    word2vec_model = Word2Vec(df['processed_plot'], min_count=1)

    # Scale the votes and rating features
    scaler = MinMaxScaler()
    df[['votes', 'rating']] = scaler.fit_transform(df[['votes', 'rating']])

    # Compute the plot embeddings
    df['plot_embedding'] = df['processed_plot'].apply(lambda tokens: sum([word2vec_model.wv[token] for token in tokens if token in word2vec_model.wv]))

    # Drop rows with missing plot embeddings
    df = df.dropna(subset=['plot_embedding'])

    # Compute the pairwise similarity matrix based on plot embeddings
    plot_embeddings = df['plot_embedding'].tolist()
    cosine_sim_plot = cosine_similarity(plot_embeddings, plot_embeddings)

    # Compute the similarity matrix based on votes and rating
    votes_rating_sim = cosine_similarity(df[['votes', 'rating']], df[['votes', 'rating']])

    # Combine the similarity scores from different features
    alpha = 0.5  # Weight for plot similarity
    beta = 0.5  # Weight for votes and rating similarity
    cosine_sim_combined = (alpha * cosine_sim_plot) + (beta * votes_rating_sim)

    return cosine_sim_combined


def get_recommendations(game_title, cosine_sim_combined, df):
    # Convert the game title to lowercase for case-insensitive matching
    game_title = game_title.lower()

    # Find the index of the game_title
    index = df['name'].str.lower().eq(game_title).idxmax()

    if pd.isnull(index):
        return []

    # Get the pairwise similarity scores of the game_title with other games
    sim_scores = list(enumerate(cosine_sim_combined[index]))

    # Sort the games based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 5 similar games (excluding duplicates)
    top_games = []
    recommended_titles = []
    for game in sim_scores:
        game_index = game[0]
        if df['name'].iloc[game_index].lower() != game_title and df['name'].iloc[game_index] not in recommended_titles:
            top_games.append(game)
            recommended_titles.append(df['name'].iloc[game_index])
        if len(top_games) >= 5:
            break

    # Get the game titles, plots, and URLs of the top similar games
    recommendations = []
    for game in top_games:
        game_index = game[0]
        recommendations.append({
            'game_title': df['name'].iloc[game_index],
            'plot': df['plot'].iloc[game_index],
            'url': df['url'].iloc[game_index]
        })

    return recommendations
