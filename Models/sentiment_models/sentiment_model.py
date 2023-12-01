# Import the following
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from imblearn.pipeline import make_pipeline
import joblib
import os

# Load data from excel file
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'database.xlsx')
print("Looking at Excel Sheet")
df = pd.read_excel(file_path, sheet_name='Sheet1')

df = df.head(500)

# Sort values by date
df.sort_values(by='Date', inplace=True)

# Drop any NA values in summary
df = df.dropna(subset=['summary'])

# Here we want to delete open and close prices that were the same. This is because
# on Fridays, Saturdays, and Sundays we will have the open and close prices as the same.
# We also want to train on model on articles that actually shifted the price
df = df[df['article_price_open_stock'] != df['article_price_close_stock']]

# Split into x and y
X = df['summary']
y = df['overall_sentiment_score']

# Split the data into training and testing sets
print("Splitting Data")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create File Name
vectorizer_file = os.path.join(script_dir, 'sentiment_vectorizer.joblib')

# If file exists, use the file
# Else, create a new vectorizer and save it
if os.path.isfile(vectorizer_file):
    print("Vectorizer exists. Loaded.")
    loaded_vectorizer = joblib.load(vectorizer_file)
else:
    # IMPORTANT: We want to set max features as well as stop words to 
    # help our vectorizer 
    print("Fitting and transforming vectorizer on the training data.")
    loaded_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english').fit(X_train)
    joblib.dump(loaded_vectorizer, vectorizer_file)
    print("Vectorizer saved.")

# Create a function to save models
def save_model(model, model_name, mse, r2):
    # Create File Name with model and accuracy in it
    filename = f"{str(model_name)}_mse_{mse:.2f}_r2_{r2:.2f}.joblib"
    joblib.dump(model, os.path.join(script_dir, filename))
    print(f"Model saved as: {filename}")

# Create a function to train and evaluate models
def model_evaluation(model, param_grid, model_name):
    # IMPORTANT: We can use the vectorizer here with the model
    model_pipeline = make_pipeline(loaded_vectorizer, model())  

    # Use GridSearch to find the best paramters. We use 
    # Cross Validation of 3 to make the program run faster
    model_grid_search = GridSearchCV(model_pipeline, param_grid, cv=3, scoring='neg_mean_squared_error', n_jobs=-1, verbose=2)
    
    # Fit the best model from GridSearchCV
    model_grid_search.fit(X_train, y_train)

    # Collect predictions
    predictions = model_grid_search.best_estimator_.predict(X_test)
    
    # Print Best Parameters, Mean Squared Error, R-squared, and save model
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"\n{model_name}:")
    print(f"Best Parameters: {model_grid_search.best_params_}")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R-squared: {r2:.2f}")
    save_model(model_grid_search.best_estimator_, model_name, mse, r2)

# Define parameter grids for each model
# Later on we will use pipeline and grid search to find the best parameters
lr_param_grid = {'linearregression__fit_intercept': [True, False]}

svr_param_grid = {'svr__C': [0.1, 1, 1.5, 2, 5, 10], 
                  'svr__kernel': ['linear', 'rbf']
}

gb_param_grid = {'gradientboostingregressor__n_estimators': [30, 50, 70, 100],
                    'gradientboostingregressor__learning_rate': [0.05, 0.1, 0.15, 2],
                    'gradientboostingregressor__max_depth': [None, 2, 3, 4, 10]
}

rf_param_grid = {'randomforestregressor__n_estimators': [100, 200, 300, 500],
                    'randomforestregressor__max_depth': [None, 10, 20, 30],
                    'randomforestregressor__min_samples_split': [2, 5, 10]
}

# Train and evaluate each model
print('Evaluating Models')
model_evaluation(LinearRegression, lr_param_grid, "Linear Regression")
model_evaluation(SVR, svr_param_grid, "Support Vector Regression")
model_evaluation(GradientBoostingRegressor, gb_param_grid, "Gradient Boosting Regression")
model_evaluation(RandomForestRegressor, rf_param_grid, "Random Forest Regression")
