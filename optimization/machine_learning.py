import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
# Read the training data from the CSV file
data = pd.read_csv('training.csv')

X = data[['pitch','mv','error']].values
y = data['velocity'].values

# Scale the input features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the scaled data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Create a linear regression model
model = LinearRegression()

# Train the model using the training data
model.fit(X_train, y_train)

# Test accuracy
accuracy = model.score(X_test, y_test)
print(accuracy)
