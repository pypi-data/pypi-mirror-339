def p1a():
    return """import numpy as np
import matplotlib.pyplot as plt
x=np.arange(-6.0,6.0,0.1)
y=3*(x)+2
y_noise=2*np.random.normal(size=x.size)
ydata=y+y_noise
plt.plot(x,ydata, 'bo')
plt.plot(x,y,'r')
plt.ylabel("dependent variable")
plt.xlabel ("independent variable")
plt.show()"""

def p1b():
    return """import matplotlib.pyplot as plt
import numpy as np
def log(x):
    return 1 / (1 + np.exp(-x))
x_value = np.linspace(-10, 10, 20)
y_value = log(x_value)
plt.figure(figsize=(8, 5))
plt.plot(x_value, y_value, label='Logistic curve: y = 1 / (1 + exp(-x))', color="blue")
plt.scatter(x_value, y_value, color="red")
plt.title("Basic Logistic Regression Curve")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()"""

def p2():
    return """import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.svm import SVC
X, y = make_classification(
    n_features=2, n_classes=2, n_redundant=0,
    n_informative=2, n_clusters_per_class=1, random_state=42)
clf = SVC(kernel='linear', C=1.0)
clf.fit(X, y)
xx, yy = np.meshgrid(
    np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 500),
    np.linspace(X[:, 1].min() - 1, X[:, 1].max() + 1, 500))
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.figure(figsize=(10, 6))
plt.contourf(xx, yy, Z > 0, alpha=0.3, cmap=plt.cm.coolwarm)
plt.contour(xx, yy, Z, levels=[0], colors='black', linestyles='-')
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm, edgecolor='k')
plt.title("SVM Decision Boundary with Linear Kernel")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()"""

def p3():
    return """import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
iris = load_wine()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)
knn = KNeighborsClassifier(n_neighbors=3)
y_pred = knn.fit(X_train, y_train).predict(X_test)
x = np.linspace(2.2, 3.8, 15)
y = np.linspace(5.0, 7.0, 15)
for i in range(len(y_test)):
    print(f"Sample {i}: True={y_test[i]}, Predicted={y_pred[i]} ({'Correct' if y_test[i] == y_pred[i] else 'Wrong'})")
plt.scatter(X_test[:, 0], X_test[:, 1], c=(y_test == y_pred), cmap=plt.cm.RdYlGn, edgecolor='k')
plt.scatter(y, x, color='green')
plt.xlabel(iris.feature_names[0])
plt.ylabel(iris.feature_names[1])
plt.grid(True)
plt.title("KNN Classification (Correct/Incorrect)")
plt.show()"""

def p4():
    return """import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
X,y=make_classification(n_samples=200,n_features=20,n_classes=2,random_state=42)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)
single_layer=Perceptron(max_iter=1000,tol=1e-3,random_state=42)
multi_layer=MLPClassifier(hidden_layer_sizes=(100,50),max_iter=1000,random_state=42)
single_layer.fit(X_train,y_train)
single_layer_accuracy=accuracy_score(y_test,single_layer.predict(X_test))
multi_layer.fit(X_train,y_train)
multi_layer_accuracy=accuracy_score(y_test,multi_layer.predict(X_test))
print(f"Single-Layer Accuracy: {single_layer_accuracy:.2f}")
print(f"Multilayer Accuracy: {multi_layer_accuracy:.2f}")
model_names=['Single-Layer Perceptron','Multilayer Perceptron']
accuracies=[single_layer_accuracy,multi_layer_accuracy]
plt.bar(model_names,accuracies,color=['blue','green'])
plt.ylabel('Accuracy')
plt.title('Comparison of Single-Layer and Multilayer Perceptrons')
plt.ylim(0,1)
plt.show()"""

def p5():
    return """import matplotlib.pyplot as plt
from sklearn.datasets import load_iris,load_wine,load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
datasets=[load_iris(),load_wine(),load_breast_cancer()]
accuracies=[]
for i,dataset in enumerate(datasets):
    X_train,X_test,y_train,y_test=train_test_split(dataset.data,dataset.target,test_size=0.2,random_state=42)
    clf=GaussianNB()
    clf.fit(X_train,y_train)
    y_pred=clf.predict(X_test)
    accuracy=accuracy_score(y_test,y_pred)
    accuracies.append(accuracy)
    print(f"{dataset.target_names[0]} Dataset: {accuracy:.2f}")
plt.bar(['Iris','Wine','Breast Cancer'],accuracies)
plt.xlabel('Dataset')
plt.ylabel('Accuracy')
plt.title('Naive Bayes Classifier Accuracy')
plt.show()"""

def p6():
    return """import numpy as np
import matplotlib.pyplot as plt
x=np.array([[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]])
y=np.array([[0],[1],[1],[0],[1],[0],[0],[1]])
w1=np.random.randn(3,4)
w2=np.random.randn(4,1)
sigmoid=lambda x:1/(1+np.exp(-x))
for _ in range(1000):
    a1=sigmoid(np.dot(x,w1))
    a2=sigmoid(np.dot(a1,w2))
    w2+=np.dot(a1.T,(y-a2)*a2*(1-a2))
    w1+=np.dot(x.T,np.dot((y-a2)*a2*(1-a2),w2.T)*a1*(1-a1))
fig,ax=plt.subplots()
for x in range(3):
    for y in range(4):
        ax.plot([0,1],[x,y],'k-')
for i in range(4):
    ax.plot([1,2],[i,0],'k-')
ax.scatter([0,0,0],[0,1,2],s=100,c='red')
ax.scatter([1,1,1,1],[0,1,2,3],s=100,c='blue')
ax.scatter([2],[0],s=100,c='green')
op=sigmoid(np.dot(sigmoid(np.dot(x,w1)),w2))
print(op)
plt.show()"""

def p7():
    return """import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import numpy as np
data = pd.DataFrame({
    'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rainy', 'Rainy', 'Sunny'],
    'Temp': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Mild'],
    'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal'],
    'Play': ['No', 'No', 'Yes', 'Yes', 'Yes', 'Yes']})
X = pd.get_dummies(data[['Outlook','Temp','Humidity']])
y = data['Play']
clf = DecisionTreeClassifier(criterion='entropy').fit(X,y)
print("Info gain for each feature")
for feature,gain in zip(X.columns,clf.feature_importances_):
    print(f"{feature}:{gain:.3f}")
plt.barh(X.columns,clf.feature_importances_,color='skyblue')
plt.xlabel('Information Gain')
plt.title('Information Gain (ID3 Algorithm)')
plt.gca().invert_yaxis()
plt.show()"""

def p8():
    return """import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
data,_=make_blobs(n_samples=200,centers=3,random_state=42)
data=StandardScaler().fit_transform(data)
models=[GaussianMixture(3),KMeans(3,n_init=10)]
labels=[model.fit_predict(data) for model in models]
for i,(label,title) in enumerate(zip(labels,['EM Algorithm','K-Means'])):
    plt.subplot(1,2,i+1)
    plt.scatter(data[:,0],data[:,1],c=label,cmap='viridis')
    plt.title(title)
plt.show()"""

def p9():
    return """import numpy as np
def locally_weighted_regression(x,y,query_point,tau):
    x=np.array(x)
    y=np.array(y)
    query_point=np.array(query_point)
    x=np.c_[np.ones(len(x)),x]
    m=len(x)
    weights=np.exp(-np.sum((x-query_point)**2,axis=1)/(2*tau**2))
    W=np.diag(weights)
    theta=np.linalg.inv(x.T@W@x)@x.T@W@y
    query_point=np.append([1],query_point)
    prediction=query_point@theta
    return prediction
if __name__=='__main__':
    x=[1,2,3,4,5]
    y=[2,3,4,5,6]
    query_point=[3.5]
    tau=1.0
    prediction=locally_weighted_regression(x,y,query_point,tau)
    print(f'Prediction at {query_point} is {prediction}')"""

def p10():
    return """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
file_path=r'F:\\\\heart-2.csv'
data=pd.read_csv(file_path)
print("Original dataset:")
print(data.head())
X=data.drop(columns=['target'])
y=data['target']
scaler=StandardScaler()
X_scaled=scaler.fit_transform(X)
pca=PCA(n_components=2)
X_pca=pca.fit_transform(X_scaled)
print("\\nOriginal shape:",X.shape)
print("Reduced shape:",X_pca.shape)
plt.figure(figsize=(10,6))
plt.scatter(X_pca[:,0],X_pca[:,1],c=y,cmap='viridis',edgecolor='k',s=50)
plt.title('PCA of Heart Dataset')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar(label='Target')
plt.grid(True)
plt.show()"""
