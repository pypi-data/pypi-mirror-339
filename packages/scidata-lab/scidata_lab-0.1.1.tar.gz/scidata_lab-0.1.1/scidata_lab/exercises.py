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
import numpy as np 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression 
from sklearn.preprocessing import StandardScaler, OneHotEncoder 
from sklearn.compose import ColumnTransformer 
from sklearn.metrics import mean_squared_error, r2_score 
import matplotlib.pyplot as plt 
data = pd.read_csv('insurance.csv')   
X = data.drop('charges', axis=1)  
y = data['charges'] 
categorical_features = ['sex', 'smoker', 'region'] 
numerical_features = ['age', 'bmi', 'children'] 
preprocessor = ColumnTransformer( 
    transformers=[ 
        ('num', StandardScaler(), numerical_features),   
        ('cat', OneHotEncoder(), categorical_features) 
    ]) 
X_processed = preprocessor.fit_transform(X) 
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42) 
model = LinearRegression() 
model.fit(X_train, y_train) 
y_pred = model.predict(X_test) 
mse = mean_squared_error(y_test, y_pred) 
r2 = r2_score(y_test, y_pred) 
print(f"Mean Squared Error: {mse:.2f}") 
print(f"R-squared: {r2:.2f}") 
plt.figure(figsize=(8, 6)) 
plt.scatter(y_test, y_pred, alpha=0.5) 
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--') 
plt.xlabel('Actual Charges') 
plt.ylabel('Predicted Charges') 
plt.title('Actual vs Predicted Charges') 
plt.show()
"""
    print(code)

def show_code_exercise_4b():
    code = """
import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LogisticRegression 
from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import accuracy_score, roc_curve, auc, confusion_matrix, classification_report 
import matplotlib.pyplot as plt 
data = pd.read_csv('diabetes.csv') 
df = pd.DataFrame(data) 
X = df.drop('Outcome', axis=1)  
y = df['Outcome']  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 
scaler = StandardScaler() 
X_train_scaled = scaler.fit_transform(X_train) 
X_test_scaled = scaler.transform(X_test) 
model = LogisticRegression() 
model.fit(X_train_scaled, y_train) 
y_pred = model.predict(X_test_scaled) 
accuracy = accuracy_score(y_test, y_pred) 
print(f"Accuracy: {accuracy*100:.2f}%") 
conf_matrix = confusion_matrix(y_test, y_pred) 
print("Confusion Matrix:") 
print(conf_matrix) 
print("\\nClassification Report:") 
print(classification_report(y_test, y_pred)) 
fpr, tpr, thresholds = roc_curve(y_test, model.predict_proba(X_test_scaled)[:, 1]) 
roc_auc = auc(fpr, tpr) 
plt.figure(figsize=(8, 6)) 
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})') 
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--') 
plt.xlabel('False Positive Rate') 
plt.ylabel('True Positive Rate') 
plt.title('Receiver Operating Characteristic (ROC) Curve') 
plt.legend(loc='lower right') 
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

# Example usage:
if __name__ == "__main__":
    show_code_exercise_1()
    show_code_exercise_2()
    show_code_exercise_3()
    show_code_exercise_4a()
    show_code_exercise_4b()
    show_code_exercise_5()
