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
print("Looking at Excel Sheet")
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'database.xlsx')
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Here we want to use 50,000 rows. As we add more data, our model
# became more accurate 
df = df.head(500)

# Sort values by date
df.sort_values(by='Date', inplace=True)

# Drop any NA values in summary
df = df.dropna(subset=['summary'])

# Here we want to delete open and close prices that were the same. This is because
# on Fridays, Saturdays, and Sundays we will have the open and close prices as the same.
# We also want to train on model on articles that actually shifted the price
df = df[df['article_price_open_stock'] != df['article_price_close_stock']]

# Create a dictionary to store the best models for each topic
best_models = {}

# Create a function to evaluate models 
def model_evaluation(model, param_grid, model_name):
    # IMPORTANT: We can use the vectorizer here with the model
    model_pipeline = make_pipeline(loaded_vectorizer, model())

    # Use GridSearch to find the best parameters. We use 
    # Cross Validation of 3 to make the program run faster
    # We also score by using neg_mean_squared_error
    model_grid_search = GridSearchCV(model_pipeline, param_grid, cv=3, scoring='neg_mean_squared_error', n_jobs=-1, verbose=2)
    
    # Fit the best model from GridSearchCV
    model_grid_search.fit(X_train, y_train)

    # Collect predictions
    predictions = model_grid_search.best_estimator_.predict(X_test)

    # Print accuracy, classification report, and save model
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"\n{model_name}:")
    print(f"Best Parameters: {model_grid_search.best_params_}")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R-squared: {r2:.2f}")
    return model_grid_search.best_estimator_

# Iterate over each topic column (columns 11 to 26)
for topic in df.columns[10:27]:
    print(f"\nTopic: {topic}")

    # Split into x and y
    X = df['summary']
    y = df[topic]

    # Split the data into training and testing sets
    print("Splitting Data")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Create File Name
    vectorizer_file = os.path.join(script_dir, f'relevance_vectorizer_{topic}.joblib')
    vectorizer_dir = os.path.dirname(os.path.abspath(vectorizer_file))

    # If file exists, use the file
    # Else, create a new vectorizer and save it
    if not os.path.exists(vectorizer_dir):
        os.makedirs(vectorizer_dir)

    if os.path.isfile(vectorizer_file):
        print("Vectorizer exists. Loaded.")
        loaded_vectorizer = joblib.load(vectorizer_file)
    else:
        # IMPORTANT: We want to set max features as well as stop words to 
        # help our vectorizer 
        print("Fitting and transforming vectorizer on the training data.")
        loaded_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english').fit(X_train)
        # Save the fitted vectorizer
        joblib.dump(loaded_vectorizer, vectorizer_file)
        print("Vectorizer saved.")

    # Transform the data
    X_train_transformed = loaded_vectorizer.transform(X_train)
    X_test_transformed = loaded_vectorizer.transform(X_test)

    # Define parameter grids for each model
    # Later on we will use pipeline and grid search to find the best parameters
    lr_param_grid = {'linearregression__fit_intercept': [True, False]}
    
    svr_param_grid = {'svr__C': [0.1, 1, 1.5, 2, 5, 10], 
                      'svr__kernel': ['linear', 'rbf']
    }

    gb_param_grid = {'gradientboostingregressor__n_estimators': [30, 50, 70],
                     'gradientboostingregressor__learning_rate': [0.05, 0.1, 0.15],
                     'gradientboostingregressor__max_depth': [None, 2, 4, 6]
    }

    rf_param_grid = {'randomforestregressor__n_estimators': [100, 200, 300],
                     'randomforestregressor__max_depth': [None, 10, 20, 30],
                     'randomforestregressor__min_samples_split': [2, 5, 10]
    }

    # Train and evaluate each model
    print('Evaluating Models')
    linear_model = model_evaluation(LinearRegression, lr_param_grid, "Linear Regression")
    svr_model = model_evaluation(SVR, svr_param_grid, "Support Vector Regression")
    gb_model = model_evaluation(GradientBoostingRegressor, gb_param_grid, "Gradient Boosting Regression")
    rf_model = model_evaluation(RandomForestRegressor, rf_param_grid, "Random Forest Regression")

    # Calculate Mean Squared Error for each model
    mse_values = {
        'Linear Regression': mean_squared_error(y_test, linear_model.predict(X_test)),
        'Support Vector Regression': mean_squared_error(y_test, svr_model.predict(X_test)),
        'Gradient Boosting Regression': mean_squared_error(y_test, gb_model.predict(X_test)),
        'Random Forest Regression': mean_squared_error(y_test, rf_model.predict(X_test)),
    }

    # Find the model with the lowest Mean Squared Error
    best_model_name = min(mse_values, key=mse_values.get)

    # Here we want to select the best model for the topic
    if best_model_name == 'Linear Regression':
        best_models[topic] = linear_model
    elif best_model_name == 'Support Vector Regression':
        best_models[topic] = svr_model
    elif best_model_name == 'Gradient Boosting Regression':
        best_models[topic] = gb_model
    elif best_model_name == 'Random Forest Regression':
        best_models[topic] = rf_model

# Save the dictionary as a file
best_models_file = os.path.join(script_dir, 'best_models_dictionary.joblib')
joblib.dump(best_models, best_models_file)
print(f"Best models dictionary saved at: {best_models_file}")
