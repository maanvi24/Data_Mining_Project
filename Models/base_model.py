# Import the following
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
import joblib
import os

# Load data from excel file
# This excel file was created from our database.py file
print("Looking at Excel Sheet")
df = pd.read_excel('database.xlsx', sheet_name='Sheet1')

# Here we want to use 10,000 rows. As we add more data, our model
# became less accurate 
df = df.head(10000)

# Sort values
df.sort_values(by='Date', inplace=True)

# Drop any NA values in summary
df = df.dropna(subset=['summary'])

# Here we want to delete open and close prices that were the same. This is because
# on Fridays, Saturdays, and Sundays we will have the open and close prices as the same.
# We also want to train on model on articles that actually shifted the price
df = df[df['article_price_open_stock'] != df['article_price_close_stock']]

# Create Target variable called price movement. This will let us know
# if the price increased or decreased the next day
df['price_movement'] = (df['article_price_close_stock'].shift(-1) > df['article_price_close_stock']).astype(int)

# Remove the last row because price_movement will be NA at the last row 
df = df[:-1]

# Split into x and y
X = df[['summary']]
y = df['price_movement']

# Split the data into training and testing sets
print("Splitting Data")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Define parameter grids for each model
# Later on we will use pipeline and grid search to find the best parameters
logreg_param_grid = {
    'columntransformer__tfidf__max_features': [1500, 2000, 2500],
    'logisticregression__C': [.25, .5, 1, 2, 3],
    'logisticregression__penalty': ['l1', 'l2'],
    'logisticregression__max_iter': [50, 100, 150]
}

rf_param_grid = {
    'columntransformer__tfidf__max_features': [1500, 2000, 250],
    'randomforestclassifier__n_estimators': [450, 500, 550, 600],
    'randomforestclassifier__max_depth': [None, 40, 50, 60],
    'randomforestclassifier__min_samples_split': [12, 15, 20, 25]
}

gb_param_grid = {
    'columntransformer__tfidf__max_features': [1500, 2000, 2500],
    'gradientboostingclassifier__n_estimators': [30, 40, 50, 75],
    'gradientboostingclassifier__learning_rate': [0.05, 0.1, 0.15],
    'gradientboostingclassifier__max_depth': [None, 2, 3, 4]
}

knn_param_grid = {
    'columntransformer__tfidf__max_features': [500, 1000, 1500],
    'kneighborsclassifier__n_neighbors': [9, 10, 11],
    'kneighborsclassifier__algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
    'kneighborsclassifier__leaf_size': [10, 30, 50],
}

# Create tfidf_vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Check if the preprocessor file exists
if os.path.isfile('preprocessor.joblib'):
    # Load the preprocessor if it exists
    print("Preprocessor exists. Loaded")
    preprocessor = joblib.load('preprocessor.joblib')
else:
    # Process summaries using tfidf_vectorizer and save it as preprocessor
    # Use ColumnTransformer
    # https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html
    print("Now vectorizing")
    preprocessor = ColumnTransformer(
        transformers=[
            ('tfidf', tfidf_vectorizer, 'summary')
        ],
        remainder='passthrough'  
    )
    # Save the preprocessor
    joblib.dump(preprocessor, 'preprocessor.joblib')
    print("Vectorizing saved")

# Create a function to save models
# put the accuracy scores in the file so that we can 
# pick the best models
def save_model(model, model_name, accuracy):
    filename = f"{model_name}_accuracy_{accuracy:.2f}.joblib"
    joblib.dump(model, filename)
    print(f"Model saved as: {filename}")

# Create a function to train and evalue models
# For each model, we will do the following:
# 1. Make a pipeline and use gridsearch with a cross validation of 3 
#    to find the best parameters
# 2. We fit the model
# 3. We print the accuracy and classification scores
# 4. Save the model
def model_evaluation(model, param_grid, model_name):
    model_pipeline = make_pipeline(preprocessor, model())
    model_grid_search = GridSearchCV(model_pipeline, param_grid, cv=3, scoring='accuracy', n_jobs=-1, verbose=2)
    model_grid_search.fit(X_train, y_train)
    predictions = model_grid_search.best_estimator_.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)
    print(f"\n{model_name}:")
    print(f"Best Parameters: {model_grid_search.best_params_}")
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", report)
    save_model(model_grid_search.best_estimator_, model_name.lower().replace(' ', '_'), accuracy)

# Train and evaluate each model
print('Evaluating Models')
model_evaluation(LogisticRegression, logreg_param_grid, "Logistic Regression")
model_evaluation(RandomForestClassifier, rf_param_grid, "Random Forest")
model_evaluation(GradientBoostingClassifier, gb_param_grid, "Gradient Boosting")
model_evaluation(KNeighborsClassifier, knn_param_grid, "K-Nearest Neighbors")
