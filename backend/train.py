import pandas as pd
import re

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Load dataset
df = pd.read_csv("emails.csv")

# Initialize stemmer
ps = PorterStemmer()

# Text preprocessing function
def transform_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Split into words
    words = text.split()

    # Remove stopwords
    words = [word for word in words if word not in stopwords.words('english')]

    # Stemming
    words = [ps.stem(word) for word in words]

    return " ".join(words)

# Apply preprocessing
df['processed_text'] = df['text'].apply(transform_text)

# Print sample
print(df[['text', 'processed_text']].head())
from sklearn.feature_extraction.text import TfidfVectorizer

# Create TF-IDF object
tfidf = TfidfVectorizer(max_features=5000)

# Convert text into vectors
X = tfidf.fit_transform(df['processed_text']).toarray()

# Labels
y = df['spam']

print(X.shape)
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print(X_train.shape)
print(X_test.shape)
from sklearn.naive_bayes import MultinomialNB

# Create model
model = MultinomialNB()

# Train model
model.fit(X_train, y_train)
from sklearn.metrics import accuracy_score

# Predict
y_pred = model.predict(X_test)

# Accuracy
print("Accuracy:", accuracy_score(y_test, y_pred))
import pickle

# Save vectorizer
pickle.dump(tfidf, open('models/vectorizer.pkl', 'wb'))

# Save model
pickle.dump(model, open('models/model.pkl', 'wb'))

print("Model and vectorizer saved successfully!")
sample_email = ["Congratulations! You won a free iPhone. Click now!"]

# Preprocess
processed_email = transform_text(sample_email[0])

# Convert to vector
vector_input = tfidf.transform([processed_email])

# Predict
result = model.predict(vector_input)[0]

if result == 1:
    print("Spam Email")
else:
    print("Not Spam")