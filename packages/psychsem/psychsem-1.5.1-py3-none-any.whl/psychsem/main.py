def DWquantile():
    print('''import pandas as pd
df=pd.read_csv("/content/SampleData.csv")
print(df)
print(df.info())
print(df["Name"].isnull())
df.fillna("null",inplace=True)
print(df["Name"].isnull())
df["Name"]=df["Name"].str.replace("null","alex")
df["Name"]=df["Name"].str.lower()
df["Name"]=df["Name"].str.upper()
df['Name']=df['Name'].str.strip()

import pandas as pd
df={'Value':[10,26,80,34,27,27,19,38,28]}
df=pd.DataFrame(df)
print(df)
Q1=df['Value'].quantile(0.25)
Q3=df['Value'].quantile(0.75)
IQR=Q3-Q1
lower_bound=Q1-1.5*IQR
upper_bound=Q3+1.5*IQR
outliers=df[(df['Value']<lower_bound) | (df['Value']>upper_bound)]
print("Outliers:\n",outliers)

import pandas as pd
df=pd.read_csv("/content/SampleData.csv")
data=df['Age']
dataInt=data.astype(int)
datatolist=dataInt.tolist()
print(datatolist)
Q1=dataInt.quantile(0.25)
Q3=dataInt.quantile(0.75)
IQR=Q3-Q1
lower_bound=Q1-1.5*IQR
upper_bound=Q3+1.5*IQR
outliers=dataInt[(dataInt<lower_bound) | (dataInt>upper_bound)]
print("Outliers:\n",outliers)

''')
    
def DWhistbar():
    print('''
# Libraries Required

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df=pd.read_csv("/content/train.csv")
print(df)
print(df.describe())
print(df.describe(include='all'))
x = df.drop(["Survived"], axis=1)
y = df["Survived"]
print("Features :\n", x)
print("Targets :\n", y)

df.hist()
plt.show()

df.plot.bar()
plt.bar(df['Age'], df['Pclass'])
plt.xlabel("Age")
plt.ylabel("Pclass")
plt.title("KSMS")
plt.show()

plt.scatter(df['Pclass'], df['Age'])
plt.xlabel("Pclass")
plt.ylabel("Age")
plt.title("KSMS")
plt.show()


sns.boxplot(x='Pclass', y='Age', data=df)
plt.xlabel("Pclass")
plt.ylabel("Age")
plt.title("KSMS")
plt.show()''')
    
def DWirisbin():
    print('''
# Libraries Required
import numpy as np
import pandas as pd
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.preprocessing import Binarizer
df=pd.read_csv("/content/iris.csv")
print(df['species'].unique)
from sklearn import preprocessing
le=preprocessing.LabelEncoder()
df['species']=le.fit_transform(df['species'])
print(df['species'].unique())
data = load_iris(as_frame=True)
df = data.frame
print(df['sepal length (cm)'])
binarizer = Binarizer(threshold=5)
df['sepal length (cm) binary'] = binarizer.fit_transform(df[['sepal length (cm)']])
print(df['sepal length (cm) binary'])''')
    
def DWirisdtreecsv():
    print('''# Libraries Required
import numpy as np
import pandas as pd

data=pd.read_csv("/content/iris.csv")
data.head()
x = data.drop('species', axis=1)
y = data['species']
print("Features")
print(x)
print("Target")
print(y)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
print("Training Data")
print(x_train)
print(y_train)
print("Testing Data")
print(x_test)
print(y_test)

# Model Creation and Training
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier()
model.fit(x_train, y_train)

# Test the Mode
y_pred = model.predict(x_test)
print(y_pred)
# Calculate Accuracy of Model

from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
# Plot Decision Tree


import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

plt.figure(figsize=(10, 6))
plot_tree(model, feature_names=x.columns, class_names=model.classes_, filled=True, rounded=True)
plt.title("\n\nKSMSC")
plt.show()
''')
    
def DWirisdtreeds():
    print('''# To train Decision Tree Classifier
from sklearn.datasets import load_iris
data = load_iris()
x = data.data
y = data.target
print("x : \n", x)
print("y : \n", y)
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
model = DecisionTreeClassifier(criterion='gini', random_state=42)
model.fit(x, y)
# To Test Decision Tree Classifier
test_data = [[6.1,3.4,9,1.8]]
prediction = model.predict(test_data)
print("Prediction : \n", prediction)
tree_rules = export_text(model, feature_names=data.feature_names)
print(tree_rules)

import matplotlib.pyplot as plt
plt.figure(figsize=(12, 8))
plot_tree(model, filled=True, feature_names=data.feature_names, class_names=data.target_names)
plt.title("Decision Tree using Gini Index")
plt.show()
          

''')

def DWginiindex():
    print('''
# Example Dataset
parent_node=[50,30,20]
child_1=[30,20,10]
child_2=[20,10,10]

print("Parent Node4 : ",parent_node)
print("Child Node1 : ",child_1)
print("Child Node2 : ",child_2)

def gini_index(classes):
  total = sum(classes)
  gini = 1
  for c in classes:
    gini -= (c/total)**2
  return gini

gini_parent = gini_index(parent_node)

print("Parent Gini Index : \n", gini_parent)
def weighted_gini(children):
  total=sum([sum(child) for child in children])
  weighted_gini=0
  for child in children:
    weighted_gini+=(sum(child)/total)*gini_index(child)
  return weighted_gini

gini_split=weighted_gini([child_1, child_2])

print("Split Gini Index : \n", gini_split)
def gini_gain (parent, children):
  gini_parent = gini_index(parent)
  gini_split = weighted_gini (children)
  return gini_parent- gini_split

gain = gini_gain (parent_node, [child_1, child_2])

print("Gini_Gain: \n", gain)''')


def DWginitree():
    print('''
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
import matplotlib.pyplot as plt

data = load_iris()
X = data.data  # Features
y = data.target  # Labels
clf = DecisionTreeClassifier(criterion='entropy', max_depth=4, random_state=42)
clf.fit(X, y)
plt.figure(figsize=(12, 8))
plot_tree(
    clf,
    feature_names=data.feature_names,
    class_names=data.target_names,
    filled=True,
    rounded=True
)
plt.title("\n\nDecision Tree using (Using Information Gain - Entropy)")
plt.show()
tree_rules = export_text(clf, feature_names=data.feature_names)
print(tree_rules)
''')
    
def DWentropy():
    print('''
import numpy as np
def entropy(classes):
    total = sum(classes)
    proportions = [count / total for count in classes if count > 0]
    return -sum(p * np.log2(p) for p in proportions)
def information_gain(parent, children):
    total_instances = sum(parent)
    parent_entropy = entropy(parent)
    weighted_entropy = sum(
        (sum(child) / total_instances) * entropy(child) for child in children
    )
    return parent_entropy - weighted_entropy
# Dataset
parent_node = [50, 30, 20]  
child_1 = [30, 20, 10]      
child_2 = [20, 10, 10]     
print("Parent Node: ",parent_node)
print("Child Node1: ",child_1)
print("Child Node2: ",child_2)
# Calculations
parent_entropy = entropy(parent_node)
weighted_entropy = sum([entropy(child_1), entropy(child_2)])
gain = information_gain(parent_node, [child_1, child_2])
# Results
print(f"Entropy (Parent Node): {parent_entropy:.4f}")
print(f"Weighted Entropy (After Split): {weighted_entropy:.4f}")
print(f"Information Gain: {gain:.4f}")
''')


def DWnaive():
    print('''
import numpy as np
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
X = np.array([
    [1,1,1,0,0],
    [1,1,0,0,0],
    [1,0,0,0,0],
    [0,0,0,0,0],
    [0,0,1,1,1],
    [0,0,1,1,1]
])

Y = np.array([1,1,1,0,0,0])
X_train , X_test , Y_train , Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)
model = BernoulliNB()
model.fit(X_train,Y_train)
Y_pred = model.predict(X_test)
accuracy = accuracy_score(Y_test,Y_pred)
print(f"Accuracy: { accuracy * 100:.2f}%")
new_email = np.array([[1,1,0,0,0]])
prediction = model.predict(new_email)
print("When we use testing data as [1, 1,0, 0, 0]")
print("Predicted class for the new email (0 = Ham , 1 = Spam):",prediction)

''')
    
def DWgaus():
    print('''

from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data
y = iris.target
print("Dataset \n", iris)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

model = GaussianNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Predicted Output \n" , y_pred)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: { accuracy * 100:.2f}%")

''')

def DWr_iris_dataa():
    print('''
library(datasets)
data(iris)
print(iris)
names(iris)
summary(iris)
summary(iris$Sepal.Width)
is.na(iris$Sepal.Width)
is.na(iris)
length(unique(iris$Sepal.Width))
plot(iris$Sepal.Width)
plot(iris)
plot(iris$Petal.Width,iris$Petal.Length)
''')
    
def DWrdtree():
    print('''# Pract No - 4 (B)
install.packages("party")
library(party) # Load package party
library (datasets) # load datasets package
data (iris) # load dataset
print(iris)
target = Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width
cdt <- ctree(target, iris) #Build tree
table(predict(cdt), iris$Species) # Create confusion matrix
cdt #To display decision tree rulesplot(cdt, type=”simple”) #Plotting of decision tree
plot(cdt, type="simple", main = "Decision Tree, ") #Plotting of decision tree

''')

def DWrnb():
    print('''
# Pract No - 4 (C)
install.packages('e1071')
library('e1071')
data<-read.csv("/content/weather-nominal-weka.csv")
print(data)
weather_df=as.data.frame(data)
weather_df
Naive_Bayes_Model=naiveBayes(play ~.,data=weather_df )
print(Naive_Bayes_Model)
NB_Predictions = predict(Naive_Bayes_Model,weather_df)
table(NB_Predictions, weather_df$play, dnn=c("Prediction", "Actual"))''')
    

def DWsvm():
    print('''import pandas as pd
data = {
    'feature1': [5.1,4.9,6.2,5.9],
    'feature2': [3.5,3.0,3.4,3.0],
    'feature3': [1.4,1.4,5.4,5.1],
    'target': [0,0,2,1]
}

#  Convert the dictionary into a pandas dataFrame
df = pd.DataFrame(data)
print(df)
# Define feature element
feature_columns = ['feature1','feature2','feature3']
target_column = 'target'
x = df[feature_columns]  #features
y = df[target_column]    # target
print("Features_Columns")
print(x)
print("Target_Columns")
print(y)

# Split the data into training and testing sets
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

print("Training Data")
print(x_train)
print(y_train)
print("Testing Data")
print(x_test)
print(y_test)

# Create SVM Classifier

from sklearn.svm import SVC
svm = SVC(kernel='linear', C=1.0)
#Train the Classifier
svm.fit(x_train,y_train)
print("Model is Trained")

# Make Prediction on test sets

y_pred = svm.predict(x_test)
print("Predicted Values")
print(y_pred)

# Evaluate the Model

from sklearn.metrics import classification_report, accuracy_score
accuracy = accuracy_score(y_test,y_pred)
print("Accuracy of the Model")
print(accuracy)
print("Classification Report")
print(classification_report(y_test,y_pred))




# Visualization

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

plt.figure(figsize=(8,6))
plt.scatter(df['feature1'],df['feature2'], c=df['target'], cmap='viridis', edgecolor='k')
plt.xlabel('Feature1')
plt.ylabel('Feature2')
plt.title('\n\nScatter Plot of Features')



''')
    
def DWrsvm():
    print('''install.packages("e1071")
install.packages("caret")
library(e1071)
library(caret)

data<-data.frame(
  feature1=c(5.1,4.9,6.2,5.9),
  feature2=c(3.5,3.0,3.4,3.0),
  feature3=c(1.4,1.4,5.4,5.1),
  target=as.factor(c(0,0,2,1))
)

set.seed(42)
trainIndex<-createDataPartition(data$target, p = 0.5, list = FALSE)
trainData<-data[trainIndex,]
testData<-data[-trainIndex,]

# Train an SVM model
svm_model <- svm(target ~., data = trainData,kernel = "linear",cost = 1)

predictions <- predict(svm_model, testData)

conf_matrix <- confusionMatrix(predictions, testData$target)
print("Confusion Matrix:")
print(conf_matrix)

accuracy <- conf_matrix$overall['Accuracy']
cat("\nAccuracy", accuracy,"/n")


''')
    
def DWkmeans():
    print('''# Practical No.6-A: Implementation of K-Means Clustering using Python



x = [14, 5, 10, 4, 3, 11, 14 , 6, 10, 12]  # Define x as a list using square brackets []
y = [21, 19, 24, 17, 16, 25, 24, 22, 21, 21]
print("Unlabel Data")
print ("X =")
print (x)
print("Y =")
print (y)


# Plot dataset using matplotlib
import matplotlib.pyplot as plt
plt. scatter (x, y)
plt.title('\n\nKSMSC')
plt. show()
data = list(zip(x, y))
print("Coordinates :")
print(data) 
          
from sklearn.cluster import KMeans
kmeans = KMeans (n_clusters=2)
kmeans. fit(data)
plt. scatter (x, y, c=kmeans. labels_)
plt. title("\n\n \n\nK-Means with 2 Clusters")
plt. show
from sklearn.cluster import KMeans
kmeans = KMeans (n_clusters=3)
kmeans. fit(data)
plt. scatter (x, y, c=kmeans. labels_)
plt. title("\n\n \n\nK-Means with 3 Clusters")
plt. show''')
    
def DWrkmean():
    print('''
install.packages("ggplot2")
install.packages("datasets")
# Load necessary libraries
library(ggplot2)
library(datasets)

# Load dataset and remove categorical column
data(iris)
df <- iris[, 1:4]

# Determine the optimal number of clusters (Elbow Method)
set.seed(123)
wcss <- vector()
for (k in 1:10) {
  wcss[k] <- sum(kmeans(df, centers = k, nstart = 10)$tot.withinss)
}
plot(1:10, wcss, type = "b", pch = 19, col = "blue",
     xlab = "Number of Clusters", ylab = "WCSS",
     main = "Elbow Method for Finding Optimal K")

# Apply K-means clustering with K=3
set.seed(123)
kmeans_result <- kmeans(df, centers = 3, nstart = 25)

# Perform PCA for visualization
pca_result <- prcomp(df, scale. = TRUE)
df_pca <- data.frame(pca_result$x[, 1:2], Cluster = as.factor(kmeans_result$cluster))

# Plot the clusters
ggplot(df_pca, aes(x = PC1, y = PC2, color = Cluster)) +
  geom_point(size = 3) +
  labs(title = "\n\n  \n\nK-means Clustering (PCA Reduced Data)")

''')