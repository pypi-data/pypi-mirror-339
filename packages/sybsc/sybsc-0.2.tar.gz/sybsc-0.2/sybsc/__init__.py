def topics():
    return [
        "linear",
        "multivariate",
        "poly",
        "logistic",
        "decisiontree",
        "randomforest",
        "extra"
    ]

def get_text(topic=None):
    texts = {
        "linear": '''#Linear Regresion
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Step 1: Load dataset
california_housing = fetch_california_housing(as_frame=True)
df = california_housing.frame

# Step 2: Find feature with highest correlation to target
correlation_matrix = df.corr()
target_correlation = correlation_matrix["MedHouseVal"].drop("MedHouseVal")
top_feature = target_correlation.idxmax()

print(f"Top feature: {top_feature}")
print(f"Correlation Coefficient: {target_correlation[top_feature]}")

# Step 3: Create X and Y
X = df[[top_feature]]
Y = df["MedHouseVal"]

# method 2slection of target feture
# X=df.drop(columns=['price'])
# Y=df['price']
# Step 4: Train Linear Regression model
model = LinearRegression()
model.fit(X, Y)

# Step 5: Coefficients
print(f"Coefficient: {model.coef_[0]}")
print(f"Intercept: {model.intercept_}")

# Step 6: Visualization
plt.figure(figsize=(8, 6))
plt.scatter(X, Y, color='skyblue', label='Actual Data')
plt.plot(X, model.predict(X), color='red', label='Regression Line')
plt.xlabel(top_feature)
plt.ylabel("MedHouseVal")
plt.title("Simple Linear Regression")
plt.legend()
plt.show()

# Step 7: RMSE Calculation
Y_pred = model.predict(X)
rmse = np.sqrt(mean_squared_error(Y, Y_pred))
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
''',
        "multivariate": '''#multi
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

print("don 3 - Multivariate Regression")

# Step 1: Load dataset
california_housing = fetch_california_housing(as_frame=True)
df = california_housing.frame

# Step 2: Find top 2 features with highest correlation to target
correlation_matrix = df.corr()
target_correlation = correlation_matrix["MedHouseVal"].drop("MedHouseVal")
top_2_features = target_correlation.sort_values(ascending=False).head(2).index.tolist()

print("Top 2 Features:", top_2_features)

# Step 3: Prepare data
X = df[top_2_features]
Y = df["MedHouseVal"]

# Step 4: Train model
model = LinearRegression()
model.fit(X, Y)

# Coefficients and Intercept
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# Step 5: Predict and calculate RMSE
Y_pred = model.predict(X)
rmse = np.sqrt(mean_squared_error(Y, Y_pred))
print("RMSE:", rmse)


# import numpy as np
# import pandas as pd
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split

# # Sample dataset
# data = {
#     'Feature1': [1, 2, 3, 4, 5],
#     'Feature2': [2, 4, 6, 8, 10],
#     'Target': [3, 6, 9, 12, 15]
# }

# df = pd.DataFrame(data)

# # Splitting data into features and target
# X = df[['Feature1', 'Feature2']]
# y = df['Target']

# # Splitting into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Creating and training the model
# model = LinearRegression()
# model.fit(X_train, y_train)

# # Making predictions
# y_pred = model.predict(X_test)

# # Display results
# print("Coefficients:", model.coef_)
# print("Intercept:", model.intercept_)
# print("Predictions:", y_pred)
''',
        "poly": '''#poly
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error

# Step 1: Load dataset
california_housing = fetch_california_housing(as_frame=True)
df = california_housing.frame

# Step 2: Find feature with highest correlation to target
correlation_matrix = df.corr()
target_correlation = correlation_matrix["MedHouseVal"].drop("MedHouseVal")
top_feature = target_correlation.idxmax()

print(f"Top feature: {top_feature}")
print(f"Correlation Coefficient: {target_correlation[top_feature]}")

# Step 3: Create X and Y
X = df[[top_feature]]
Y = df["MedHouseVal"]

# Step 4: Transform X to include polynomial (degree 2) terms
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

# Step 5: Train Polynomial Regression model
model = LinearRegression()
model.fit(X_poly, Y)

# Step 6: Coefficients
print(f"Coefficients: {model.coef_}")
print(f"Intercept: {model.intercept_}")

# Step 7: Visualization
plt.figure(figsize=(8, 6))
plt.scatter(X, Y, color='skyblue', label='Actual Data')
plt.plot(X, model.predict(X_poly), color='red', label='Polynomial Regression Line')
plt.xlabel(top_feature)
plt.ylabel("MedHouseVal")
plt.title("Polynomial Regression (Degree 2)")
plt.legend()
plt.show()

# Step 8: RMSE Calculation
Y_pred = model.predict(X_poly)
rmse = np.sqrt(mean_squared_error(Y, Y_pred))
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
''',
        "logistic": '''#Lojistic
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Step 1: Load the dataset
df = pd.read_csv("C://Users//BYada//Downloads//diabetes.csv")
print("Dataset loaded successfully!")
print(df.head())

# Step 2: Split features (X) and target (y)
X = df.drop("label", axis=1)  # Features
y = df["label"]               # Target (0 or 1)

# Step 3: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train Logistic Regression model
model = LogisticRegression(random_state=16)
model.fit(X_train, y_train)

# Step 5: Predict and evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print(f"\nAccuracy: {acc:.4f}")
print("Confusion Matrix:")
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Optional: Visualize the confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()
''',
        "decisiontree": '''#Decision tree
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import matplotlib.pyplot as plt

# Step 1: Load CSV
PlayTennis = pd.read_csv("C://Users//BYada//Downloads//PlayTennis.csv")
PlayTennis

# Step 2: Label Encoding
Le = LabelEncoder()

PlayTennis['Outlook'] = Le.fit_transform(PlayTennis['Outlook'])
PlayTennis['Temperature'] = Le.fit_transform(PlayTennis['Temperature'])
PlayTennis['Humidity'] = Le.fit_transform(PlayTennis['Humidity'])
PlayTennis['Wind'] = Le.fit_transform(PlayTennis['Wind'])
PlayTennis['Play Tennis'] = Le.fit_transform(PlayTennis['Play Tennis'])

PlayTennis

# Step 3: Features and Target
y = PlayTennis['Play Tennis']
X = PlayTennis.drop(['Play Tennis'], axis=1)

# Step 4: Train Model
clf = DecisionTreeClassifier(criterion='entropy')
clf = clf.fit(X, y)

# Step 5: Plot Tree
plt.figure(figsize=(12, 8))
tree.plot_tree(clf, feature_names=X.columns, class_names=["No", "Yes"], filled=True)
plt.show()

''',
        "randomforest": '''# Rendom Forest
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

# Loading the iris plants dataset (classification)
iris = datasets.load_iris()
print(type(iris))  
print(iris.feature_names)
print(iris.target_names)
# print(iris.data)
print(iris.target)

# Dividing dataset into X (features) and y (target)
X, y = datasets.load_iris(return_X_y=True)
print(type(X))      # <class 'numpy.ndarray'>
print(type(y))      # <class 'numpy.ndarray'>
print(X.shape)      # (150, 4)
print(y.shape)      # (150,)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

# Creating a Random Forest classifier
clf = RandomForestClassifier(n_estimators=100)

# Training the model
clf.fit(X_train, y_train)

# Performing predictions
y_pred = clf.predict(X_test)

# Accuracy calculation using metrics
print("ACCURACY OF THE MODEL:", metrics.accuracy_score(y_test, y_pred))  # e.g. 0.9555

# Predicting a new sample
print("Prediction for new sample [3, 3, 2, 2]:", clf.predict([[3, 3, 2, 2]]))

# Using feature importance
feature_imp = pd.Series(clf.feature_importances_, index=iris.feature_names).sort_values(ascending=False)
print("\nFeature Importances:")
print(feature_imp)
  ''',
        "extra": '''#Extra
import pandas as pd

data ={ "customer_id" : [268408,268408,268408,268408,268408,268408,268159,268159],
        "DOB" : ['2-1-70','2-1-70','2-1-70','2-1-70','2-1-70','2-1-70','8-1-70','8-1-70'],
       "Gender" : ["M","M","M","M","M","M","F","F"],
       "city_code" : [4.0,4.0,4.0,4.0,4.0,4.0,8.0,8.0],
       "transaction_id" : [87243835584,87243835584,87243835584,87243835584,87243835584,87243835584,65867401816,65867401816],
       "cust_id" : [268408,268408,268408,268408,268408,268408,268159,268159],
       "tran_date" : ['13-01-2014','13-01-2014','13-01-2014','13-01-2014','13-01-2014','13-01-2014','31-03-2013','31-03-2013'],
       "prod_subcar_code" : [7,7,7,7,7,7,11,11],
       "prod_cat_code" : [5,5,5,5,5,5,5,5],
       "Qty" : [5,5,5,5,5,5,5,5],
       "Rate" : [187,187,187,187,187,187,214,214],
}

df=pd.DataFrame(data)
df

#df.loc with a condition(filter record where city code=4
finding=df.loc[df['city_code'] == 8.0]
print(finding)

#using pandas loc function multiple response
l1=df.loc[6, 'city_code']
l2=df.loc[[1, 7], ['city_code', 'Gender']]
l3=df.loc[df['Rate'] == 214]
print("Particular row and Column Value:-\n",l1)
print('\n')
print("2D dataFrame only selected row,column:-\n",l2)
print('\n')
print("Applying Condition :-\n",)

g=df.groupby(["Gender","city_code"])["Qty"].count()
g2= df.groupby("Gender")["Qty"].count()

print(g2)

dropDupli=df.drop_duplicates()
dropDupli

fill=df.fillna(0)
fill

#Second Prac
#Display The number of Male and female customer
disp = df.groupby("Gender").count()
disp2 = df.groupby("Gender")['Qty'].count()

disp

#Display the total Qty purchased in a city with city_code = 8.0
total_purch = df.loc[df['city_code'] == 8.0]['Qty'].sum()
print(f"total Purchase is {total_purch}")

#Display the total  Rate for Every prod_subcat_code
totRat = df.groupby("prod_cat_code")["Rate"].sum()
totRat
#Display city_wise number of transaction
dd=df.groupby("city_code")["transaction_id"].nunique()
dd
city_wise_transactions = df.groupby("city_code")["transaction_id"].nunique()
city_wise_transactions

# Convert DOB to datetime
df['DOB'] = pd.to_datetime(df['DOB'], format='%d-%m-%y')
df['DOB2'] = pd.to_datetime(df['DOB2'], format='%y-%m-%d')



# Calculate age
current_year = datetime.now().year
df['age'] = current_year - df['DOB'].dt.year

'''
    }

    if topic is None:
        return "Please specify a topic. Use sybsc.topics() to see available topics."

    topic = topic.lower()
    return texts.get(topic, f"No content found for topic: {topic}")
