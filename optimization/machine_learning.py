import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Read the training data from the CSV file
data = pd.read_csv('training.csv')

# Split the data into input features (pitch) and target variable (velocity)
X = data['pitch'].values.reshape(-1, 1)
y = data['velocity'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a linear regression model
model = LinearRegression()

# Train the model using the training data
model.fit(X_train, y_train)

# test accuracy
accuracy = model.score(X_test, y_test)
print(accuracy*100, '%')