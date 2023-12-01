# Import the following
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.pipeline import make_pipeline
import joblib
import os

# Load data from excel file
print("Looking at Excel Sheet")
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'database.xlsx')
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Here we want to use 10,000 rows. As we add more data, our model
# became less accurate 
df = df.head(10000)

# Sort values by date
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
X = df['summary']
y = df['price_movement']

# Split the data into training and testing sets
print("Splitting Data")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Write name of file for movement_vectorizer_file in this directory
movement_vectorizer_file = os.path.join(script_dir, 'movement_vectorizer.joblib')

# If file exists, use the file
# Else, create a new vectorizer and save it
if os.path.isfile(movement_vectorizer_file):
    print("Vectorizer exists. Loaded.")
    loaded_vectorizer = joblib.load(movement_vectorizer_file)
else:
    # IMPORTANT: We want to set max features as well as stop words to 
    # help our vectorizer 
    print("Fitting and transforming vectorizer on the training data.")
    loaded_vectorizer = TfidfVectorizer(max_features=500, stop_words='english').fit(X_train)
    joblib.dump(loaded_vectorizer, movement_vectorizer_file)
    print("Vectorizer saved.")

# Create a function to save models
def save_model(model, model_name, accuracy):
    
    # Create File Name with model and accuracy in it
    filename = os.path.join(script_dir, f"{str(model_name)}_accuracy_{accuracy:.2f}.joblib")
    joblib.dump(model, filename)
    print(f"Model saved as: {filename}")

# Create a function to train and evaluate models
def model_evaluation(model, param_grid, model_name):
    
    # IMPORTANT: We can use the vectorizer here with the model
    model_pipeline = make_pipeline(loaded_vectorizer, model())
    
    # Use GridSearch to find the best paramters. We use 
    # Cross Validation of 3 to make the program run faster
    model_grid_search = GridSearchCV(model_pipeline, param_grid, cv=3, scoring='accuracy', n_jobs=-1, verbose=2)
    
    # Fit the best model from GridSearchCV
    model_grid_search.fit(X_train, y_train)

    # Collect predictions
    predictions = model_grid_search.best_estimator_.predict(X_test)
    
    # Print accuracy, classification report, and save model
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)
    print(f"\n{model_name}:")
    print(f"Best Parameters: {model_grid_search.best_params_}")
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", report)
    save_model(model_grid_search.best_estimator_, model_name, accuracy)

# Define parameter grids for each model
# Later on we will use pipeline and grid search to find the best parameters
logreg_param_grid = {
    'logisticregression__C': [0.25, 0.5, 1, 1.5, 2],
    'logisticregression__penalty': ['l1', 'l2', 'none'],
    'logisticregression__max_iter': [50, 100, 150]
}

rf_param_grid = {
    'randomforestclassifier__n_estimators': [450, 500, 550, 600],
    'randomforestclassifier__max_depth': [None, 40, 50, 60, 80],
    'randomforestclassifier__min_samples_split': [5, 10, 15, 20]
}

gb_param_grid = {
    'gradientboostingclassifier__n_estimators': [30, 50, 75, 100],
    'gradientboostingclassifier__learning_rate': [0.05, 0.1, 0.15],
    'gradientboostingclassifier__max_depth': [None, 2, 3, 4]
}

knn_param_grid = {
    'kneighborsclassifier__n_neighbors': [5, 10, 15],
    'kneighborsclassifier__algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
    'kneighborsclassifier__leaf_size': [10, 30, 50, 70],
}

# Train and evaluate each model
print('Evaluating Models')
model_evaluation(LogisticRegression, logreg_param_grid, "Logistic Regression")
model_evaluation(RandomForestClassifier, rf_param_grid, "Random Forest")
model_evaluation(GradientBoostingClassifier, gb_param_grid, "Gradient Boosting")
model_evaluation(KNeighborsClassifier, knn_param_grid, "K-Nearest Neighbors")
