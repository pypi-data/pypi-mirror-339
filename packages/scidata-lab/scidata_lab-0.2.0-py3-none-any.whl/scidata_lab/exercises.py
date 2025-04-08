def show_code_exercise_1():
    code = """
import pandas as pd 
import numpy as np
data = pd.read_csv('Attack Identification.csv')
print(data)
d = np.array(data)[:,:-1]
print("The attributes are",d)
target = np.array(data)[:,-1]
print("The target is",target)
def train(c, t):
    for i, val in enumerate(t):
        if val == "Yes":
            specific_hypothesis = c[i].copy()
            break
    for i, val in enumerate(c):
        if t[i] == "Yes":
            for x in range(len(specific_hypothesis)):
                if val[x] != specific_hypothesis[x]:
                    specific_hypothesis[x] = '?'
    return specific_hypothesis
print("The Final Hypothesis is:",train(d,target))
"""
    print(code)

def show_code_exercise_2():
    code = """
import numpy as np
import pandas as pd

data = pd.read_csv('Attack Identification.csv')
concepts = np.array(data.iloc[:,0:-1])
target = np.array(data.iloc[:,-1])  
def learn(concepts, target):
    specific_h = concepts[0].copy()  
    print("initialization of specific_h \\n",specific_h)  
    general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]    
    print("initialization of general_h \\n", general_h)  

    for i, h in enumerate(concepts):
        if target[i] == "Yes":
            print("If instance is Positive ")
            for x in range(len(specific_h)):
                if h[x]!= specific_h[x]:                    
                    specific_h[x] ='?'                    
                    general_h[x][x] ='?'
                   
        if target[i] == "No":            
            print("If instance is Negative ")
            for x in range(len(specific_h)):
                if h[x]!= specific_h[x]:                    
                    general_h[x][x] = specific_h[x]                
                else:                    
                    general_h[x][x] = '?'        

        print(" step {}".format(i+1))
        print(specific_h)        
        print(general_h)
        print("\\n")

    indices = [i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]    
    for i in indices:  
        general_h.remove(['?', '?', '?', '?', '?', '?'])
    return specific_h, general_h

s_final, g_final = learn(concepts, target)

print("Final Specific_h:", s_final, sep="\\n")
print("Final General_h:", g_final, sep="\\n")
"""
    print(code)

def show_code_exercise_3():
    code = """
import numpy as np 
import pandas as pd 
from mlxtend.frequent_patterns import apriori, association_rules 
from mlxtend.preprocessing import TransactionEncoder 
data = pd.read_csv('purchase.csv', names=['Items Bought'], header=None) 
data = list(data['Items Bought'].apply(lambda x: x.split(','))) 
te = TransactionEncoder() 
te_data = te.fit(data).transform(data) 
df = pd.DataFrame(te_data, columns=te.columns_) 
frq_items = apriori(df, min_support=0.3, use_colnames=True) 
print(frq_items) 
rules = association_rules(frq_items, metric="confidence", min_threshold=0.5) 
rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']] 
print(rules)
"""
    print(code)

def show_code_exercise_4a():
    code = """
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('advertising.csv')

# Define input and output
X = df[['TV']]   # Simple Linear → Only one feature
y = df['Sales']

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
print("R² Score:", r2_score(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))

# Visualization
plt.scatter(X_test, y_test, color='green', label='Actual')
plt.plot(X_test, y_pred, color='red', label='Predicted Line')
plt.xlabel('TV Budget')
plt.ylabel('Sales')
plt.title('Simple Linear Regression')
plt.legend()
plt.show()
"""
    print(code)

def show_code_exercise_4b():
    code = """
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("insurance.csv")

# Convert categorical variables to dummies
df = pd.get_dummies(df, drop_first=True)

# Features and target
X = df.drop("charges", axis=1)
y = df["charges"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
print("R² Score:", r2_score(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))

# Visualization: Actual vs Predicted
plt.scatter(y_test, y_pred, color='green', alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('Actual Charges')
plt.ylabel('Predicted Charges')
plt.title('Multiple Linear Regression: Actual vs Predicted')
plt.grid(True)
plt.show()
"""
    print(code)

def show_code_exercise_4c():
    code = """
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Sample data
data = {
    'Book Name': ['AI Basics', 'Data Wrangling', 'Algo Design', 'CS Theory', 'NetSec 101'],
    'Author': ['John Doe', 'Jane Smith', 'John Doe', 'John Doe', 'Marissa Lee'],
    'Ratings': [4.2, 3.8, 4.2, 4.2, 3.5],
    'Recommended (yes/no)': ['yes', 'no', 'yes', 'yes', 'no']
}

df = pd.DataFrame(data)

# Convert labels
df['Recommended'] = df['Recommended (yes/no)'].map({'yes': 1, 'no': 0})

# Dummies for categorical features
df = pd.get_dummies(df.drop(columns=['Recommended (yes/no)', 'Book Name']), drop_first=True)

# Features and target
X = df.drop('Recommended', axis=1)
y = df['Recommended']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
print("Accuracy:", accuracy_score(y_test, y_pred))

# Visualization: Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Not Recommended", "Recommended"])
disp.plot(cmap="Blues")
plt.title("Logistic Regression - Confusion Matrix")
plt.grid(False)
plt.show()
"""
    print(code)

def show_code_exercise_5():
    code = """
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

file_path = "Dataset.csv"
df = pd.read_csv(file_path)

label_encoders = {}
for column in df.columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

X = df.drop('Decision', axis=1)
y = df['Decision']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

clf = DecisionTreeClassifier(criterion='entropy', random_state=42, max_depth=4)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\\nDataset Accuracy: {accuracy:.2f}")

tree_rules = export_text(clf, feature_names=list(X.columns))
print("\\nDecision Tree Rules:\\n")
print(tree_rules)

plt.figure(figsize=(20, 12))
plot_tree(clf, filled=True, feature_names=X.columns, class_names=['No', 'Yes'], rounded=True, fontsize=20)
plt.title("Decision Tree Visualization", fontsize=30)
plt.tight_layout()
plt.show()

new_sample = {
    'Alternate': [1],
    'Reservation': [0],
    'Hungry': [1],
    'Patrons': [2],
    'Price': [2],
    'Raining': [0],
    'WaitEstimate': [1],
}
new_sample_df = pd.DataFrame(new_sample)
new_sample_df = new_sample_df[X_train.columns]

predicted_class = clf.predict(new_sample_df)
print(f"\\nPredicted class for the new sample: {'Yes' if predicted_class[0] == 1 else 'No'}")
"""
    print(code)

def show_code_exercise_6():
    code = """
import pandas as pd
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB

data = pd.read_csv('/content/sample_data/tennisdata.csv')
print("The first 5 Values of data is :\\n", data.head())

data = data.apply(LabelEncoder().fit_transform)
data.head()

X = data.iloc[:, :-1]
print("\\nThe First 5 values of the train data is\\n", X.head())

y = data.iloc[:, -1]
print("\\nThe First 5 values of train output is\\n", y.head())

le_PlayTennis = LabelEncoder()
y = le_PlayTennis.fit_transform(y)
print("\\nNow the Train output is\\n", y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

classifier = GaussianNB()
classifier.fit(X_train, y_train)

from sklearn.metrics import accuracy_score
print("Accuracy is:", accuracy_score(classifier.predict(X_test), y_test))
"""
    print(code)

def show_code_exercise_7():
    code = """
import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        # Initialize weights and biases
        self.weights_input_hidden = np.random.randn(self.input_size, self.hidden_size)
        self.bias_hidden = np.zeros((1, self.hidden_size))
        self.weights_hidden_output = np.random.randn(self.hidden_size, self.output_size)
        self.bias_output = np.zeros((1, self.output_size))
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def forward(self, X):
        # Forward pass
        self.hidden_layer_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        self.hidden_layer_output = self.sigmoid(self.hidden_layer_input)
        self.output_layer_input = np.dot(self.hidden_layer_output, self.weights_hidden_output) + self.bias_output
        self.output = self.sigmoid(self.output_layer_input)
        return self.output
    
    def backward(self, X, y, output, learning_rate):
        # Backpropagation
        error = y - output
        output_delta = error * self.sigmoid_derivative(output)
        hidden_error = output_delta.dot(self.weights_hidden_output.T)
        hidden_delta = hidden_error * self.sigmoid_derivative(self.hidden_layer_output)
        # Update weights and biases
        self.weights_hidden_output += self.hidden_layer_output.T.dot(output_delta) * learning_rate
        self.bias_output += np.sum(output_delta, axis=0, keepdims=True) * learning_rate
        self.weights_input_hidden += X.T.dot(hidden_delta) * learning_rate
        self.bias_hidden += np.sum(hidden_delta, axis=0, keepdims=True) * learning_rate
    
    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output, learning_rate)
            if epoch % 100 == 0:
                print(f'Epoch {epoch}: Error {np.mean(np.square(y - output))}')

# Example usage:
input_size = 1
hidden_size = 1
output_size = 1
# Initialize neural network
nn = NeuralNetwork(input_size, hidden_size, output_size)
# Example training data
X = np.array([[5]])  # Input
y = np.array([[1]])  # Target output
# Train the neural network
nn.train(X, y, epochs=1000, learning_rate=0.1)
# Make predictions
predictions = nn.forward(X)
print("Predictions:", predictions)

# Example usage with XOR:
input_size = 2
hidden_size = 3
output_size = 1
nn = NeuralNetwork(input_size, hidden_size, output_size)
# Example training data
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])
# Train the neural network
nn.train(X, y, epochs=1000, learning_rate=0.1)
# Make predictions
predictions = nn.forward(X)
print("Predictions:", predictions)
"""
    print(code)

def show_code_exercise_8():
    code = """
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df = pd.read_csv("/content/sample_data/kmeansdata.csv")
kmeans = KMeans(n_clusters=3).fit(df)
centroids = kmeans.cluster_centers_
print(centroids)

plt.scatter(df['X'], df['Y'], c=kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.show()
"""
    print(code)

def show_code_exercise_9():
    code = """
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn

sns.set_style("whitegrid")
data = pd.read_csv("/content/sample_data/matches.csv")
data.describe()
data.isnull().sum()

data = data.iloc[:,:-1]
data.dropna(inplace=True)
data["team1"].unique()

# For Delhi Capitals
data['team1'] = data['team1'].str.replace('Delhi Daredevils', 'Delhi Capitals')
data['team2'] = data['team2'].str.replace('Delhi Daredevils', 'Delhi Capitals')
data['winner'] = data['winner'].str.replace('Delhi Daredevils', 'Delhi Capitals')
# For Sunrisers Hyderabad
data['team1'] = data['team1'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
data['team2'] = data['team2'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
data['winner'] = data['winner'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')

# Number of IPL matches won by each team
plt.figure(figsize=(10,6))
sns.countplot(y='winner', data=data, order=data['winner'].value_counts().index)
plt.xlabel('Wins')
plt.ylabel('Team')
plt.title('Number of IPL matches won by each team')

# Total number of matches played in different stadiums
plt.figure(figsize=(10,6))
sns.countplot(y='venue', data=data, order=data['venue'].value_counts().iloc[:10].index)
plt.xlabel('No of matches', fontsize=12)
plt.ylabel('Venue', fontsize=12)
plt.title('Total Number of matches played in different stadium')

# Toss decision
plt.figure(figsize=(10,6))
sns.countplot(x="toss_decision", data=data)
plt.xlabel('Toss Decision', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title('Toss Decision')

# Unique values and counts
x = ["city", "toss_decision", "result", "dl_applied"]
for i in x:
    print("------------")
    print(data[i].unique())
    print(data[i].value_counts())

# Drop unnecessary features
data.drop(["id", "season", "city", "date", "player_of_match", "venue", "umpire1", "umpire2"], axis=1, inplace=True)
data.describe()

X = data.drop(["winner"], axis=1)
y = data["winner"]
print(y.unique())

X = pd.get_dummies(X, ["team1", "team2", "toss_winner", "toss_decision", "result"], drop_first=True)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
print(y)
y = le.fit_transform(y)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X, y, train_size=0.8)

from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

model_df = {}
def model_val(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"{model} accuracy is {accuracy_score(y_test, y_pred)}")
    print(y_pred[0:5], y_test[0:5])

model = DecisionTreeClassifier()
model_val(model, X, y)
model = GaussianNB()
model_val(model, X, y)
"""
    print(code)

def show_code_exercise_10():
    code = """
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
import joblib

# Convert dataset into dataframe
data = pd.read_csv("/content/drive/MyDrive/Loan_status.csv")

# Print first 5 and last 5 dataframes
print(data.head())
print(data.tail())

# Print number of rows and columns
print("No of rows", data.shape[0])
print("No of columns", data.shape[1])

# Print dataset details
print(data.info())

# Check null values
data.isnull().sum()
data.isnull().sum() * 100 / len(data)

# Handle missing values
columns = ['Gender', 'Married', 'Dependents', 'LoanAmount', 'Loan_Amount_Term']
data = data.dropna(subset=columns)
data['Self_Employed'] = data['Self_Employed'].fillna(data['Self_Employed'].mode()[0])
data['Credit_History'] = data['Credit_History'].fillna(data['Credit_History'].mode()[0])
print(data.isnull().sum() * 100 / len(data))

# Handle categorical columns
data['Dependents'] = data['Dependents'].replace(to_replace='3+', value='4')
data['Dependents'].unique()

# Encode categorical variables
label_encoder = LabelEncoder()
data['Gender'] = label_encoder.fit_transform(data['Gender'])
data['Married'] = label_encoder.fit_transform(data['Married'])
data['Education'] = label_encoder.fit_transform(data['Education'])
data['Self_Employed'] = label_encoder.fit_transform(data['Self_Employed'])
data['Property_Area'] = label_encoder.fit_transform(data['Property_Area'])
data['Loan_Status'] = label_encoder.fit_transform(data['Loan_Status'])

# Drop Loan_ID
data = data.drop("Loan_ID", axis=1)
print(data.head())

# Prepare features and target
X = data.drop('Loan_Status', axis=1)
y = data['Loan_Status']

# Scale numerical columns
cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']
st = StandardScaler()
X[cols] = st.fit_transform(X[cols])
print(X[cols])

# Model evaluation function
model_df = {}
def model_val(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"{model} accuracy is {accuracy_score(y_test, y_pred)}")
    score = cross_val_score(model, X, y, cv=5)
    print(f"{model} avg cross val score is {np.mean(score)}")
    model_df[model] = round(np.mean(score) * 100, 2)

# Train and evaluate models
model = LogisticRegression()
model_val(model, X, y)
model = DecisionTreeClassifier()
model_val(model, X, y)
model = GaussianNB()
model_val(model, X, y)

# Save and load model
nb = GaussianNB()
nb.fit(X, y)
joblib.dump(nb, 'Loan_status_predict')
Model = joblib.load('Loan_status_predict')

# Make prediction
print(y.head(10))
df = X.iloc[6:7]
result = model.predict(df)
if result == 1:
    print('loan approved')
else:
    print('loan not approved')
print(model_df)
"""
    print(code)

# Example usage:
if __name__ == "__main__":
    show_code_exercise_1()
    show_code_exercise_2()
    show_code_exercise_3()
    show_code_exercise_4a()
    show_code_exercise_4b()
    show_code_exercise_4c()
    show_code_exercise_5()
    show_code_exercise_6()
    show_code_exercise_7()
    show_code_exercise_8()
    show_code_exercise_9()
    show_code_exercise_10()