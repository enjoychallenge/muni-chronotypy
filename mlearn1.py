# https://machinelearningmastery.com/machine-learning-in-python-step-by-step/

# compare algorithms
import pandas as pd
from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

# Load dataset
url = "data/derived/zsj_full.csv"
dataset = read_csv(url)

scatter_matrix(dataset)
pyplot.show()

# # Split-out validation dataset
array = dataset.values
X = array[:, 2:7]
y = array[:, 7]

X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1, shuffle=True)
# # Spot Check Algorithms

models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))
# evaluate each model in turn
results = []
names = []
for name, model in models:
	kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
	cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
	results.append(cv_results)
	names.append(name)
	print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))

# LR: 0.631028 (0.107070)
# LDA: 0.627668 (0.056587)
# KNN: 0.500000 (0.058633)
# CART: 0.540119 (0.072839)
# NB: 0.460277 (0.109231)
# SVM: 0.543874 (0.019460)

model = LinearDiscriminantAnalysis()
model.fit(X_train, Y_train)
predictions = model.predict(X_validation)

print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))

predictions = model.predict(X)
print(accuracy_score(y, predictions))
print(confusion_matrix(y, predictions))
print(classification_report(y, predictions))

df_chronotyp = pd.DataFrame({'chronotyp_guessed': predictions})
df_export = pd.concat([dataset, df_chronotyp], axis=1, sort=False)
df_export.to_csv('data/derived/zsj_full_guess.csv', encoding='utf-8', index=False)
