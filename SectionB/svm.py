# Support Vector Machine (SVM)

# Importing the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.svm import SVC

from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score


# Importing the dataset
dataset = pd.read_csv('zoo.data', header = None )
X = dataset.iloc[:, 1:].values
y = dataset.iloc[:, [0]].values
y_class = y

#Converting to respective classes (animals corresponding to a class represents a class)
for i,b in enumerate(y_class):
    if(b == 'aardvark' or b == 'antelope' or b == 'bear' or b == 'boar' or b == 'buffalo' or b == 'calf' or
                  b == 'cavy' or b == 'cheetah' or b == 'deer' or b == 'dolphin' or b == 'elephant' or b == 'fruitbat' 
                  or b == 'giraffe' or b == 'girl' or b == 'goat' or b == 'gorilla' or b == 'hamster' or b == 'hare' 
                  or b == 'leopard' or b == 'lion' or b == 'lynx' or b == 'mink' or b == 'mole' or b == 'mongoose' or
                  b == 'opossum' or b == 'oryx' or b == 'platypus' or b == 'polecat' or b == 'pony' or
                  b == 'porpoise' or b == 'puma' or b == 'pussycat' or b == 'raccoon' or b == 'reindeer' or
                  b == 'seal' or b ==  'sealion' or b == 'squirrel' or b == 'vampire' or b == 'vole' or b == 'wallaby' or 
                  b == 'wolf'):
        y_class[i] = 'c1'
        
    elif(b == 'chicken' or b == 'crow' or b == 'dove' or b == 'duck' or b == 'flamingo' or b == 'gull' or
                  b == 'hawk' or b == 'kiwi' or b == 'lark' or b == 'ostrich' or b == 'parakeet' or b == 'penguin' 
                  or b == 'pheasant' or b == 'rhea' or b == 'skimmer' or b == 'skua' or b == 'sparrow' or b == 'swan' 
                  or b == 'vulture' or b == 'wren'):
        y_class[i] = 'c2'
        
    elif(b == 'pitviper' or b == 'seasnake' or b == 'slowworm' or b == 'tortoise' or b == 'tuatara'):
        y_class[i] = 'c3'
        
    elif(b == 'bass' or b == 'carp' or b == 'catfish' or b == 'chub' or b == 'dogfish' or b == 'haddock' or
                  b == 'herring' or b == 'pike' or b == 'piranha' or b == 'seahorse' or b == 'sole' or b == 'stingray' 
                  or b == 'tuna'):
        y_class[i] = 'c4'
        
    elif(b == 'frog' or b == 'frog' or b == 'newt' or b == 'toad'):
        y_class[i] = 'c5'
        
    elif(b == 'flea' or b == 'gnat' or b == 'honeybee' or b == 'housefly' or b == 'ladybird' or b == 'moth' or
                  b == 'termite' or b == 'wasp'):
        y_class[i] = 'c6'
        
    elif(b == 'clam' or b == 'crab' or b == 'crayfish' or b == 'lobster' or b == 'octopus' or b == 'scorpion' or
                  b == 'seawasp' or b == 'slug' or b == 'starfish' or b == 'worm'):
        y_class[i] = 'c7'
        
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
y_class = labelencoder.fit_transform(y_class)

from sklearn.preprocessing import label_binarize

# Use label_binarize to be multi-label like settings
Y = label_binarize(y_class, classes=[0, 1, 2, 3, 4, 5, 6])
n_classes = Y.shape[1]
    

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.5, random_state = 0)




# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


##################################################################
##################################################################
###################################################################

# Fitting SVM to the Training set using Linear kernel
#Using sklearn multiclass method


from sklearn.multiclass import OneVsRestClassifier
classifier_linear2 = OneVsRestClassifier(SVC(kernel = 'linear', random_state = 0))
classifier_linear2.fit(X_train, y_train)

#Model Evaluation using K-fold Cross Validation
from sklearn.model_selection import cross_val_score
accuracies_linear2 = cross_val_score(estimator = classifier_linear2, X = X_train, y = y_train, cv = 5)
accuracies_linear2.mean()
accuracies_linear2.std()

y_pred_linear2 = classifier_linear2.predict(X_test)
accuracy_linear2 = classifier_linear2.score(X_test, y_test)
y_score_linear2 = classifier_linear2.decision_function(X_test)


# For each class
precision_linear2 = dict()
recall_linear2 = dict()
average_precision_linear2 = dict()
for i in range(n_classes):
    precision_linear2[i], recall_linear2[i], _ = precision_recall_curve(y_test[:, i], y_score_linear2[:, i])
    average_precision_linear2[i] = average_precision_score(y_test[:, i], y_score_linear2[:, i])

# A "micro-average": quantifying score on all classes jointly
precision_linear2["micro"], recall_linear2["micro"], _ = precision_recall_curve(y_test.ravel(), y_score_linear2.ravel())
average_precision_linear2["micro"] = average_precision_score(y_test, y_score_linear2, average="micro")
print('Average precision score, micro-averaged over all classes: {0:0.2f} for linear kernel SVM'.format(average_precision_linear2["micro"]))

plt.figure()
plt.step(recall_linear2['micro'], precision_linear2['micro'], color='b', alpha=0.2, where='post')
plt.fill_between(recall_linear2["micro"], precision_linear2["micro"], alpha=0.2, color='b')

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.title('Average precision score, micro-averaged over all classes: AP={0:0.2f} for linear kernel SVM'.format(average_precision_linear2["micro"]))
plt.show()

###################################################################
###################################################################
###################################################################

# Fitting SVM to the Training set using Rbf kernel
#Using sklearn multiclass method

from sklearn.multiclass import OneVsRestClassifier
classifier_rbf2 = OneVsRestClassifier(SVC(kernel = 'rbf', random_state = 0, gamma = 'auto'))
classifier_rbf2.fit(X_train, y_train)

#Model Evaluation using K-fold Cross Validation
from sklearn.model_selection import cross_val_score
accuracies_rbf2 = cross_val_score(estimator = classifier_rbf2, X = X_train, y = y_train, cv = 5)
accuracies_rbf2.mean()
accuracies_rbf2.std()

y_pred_rbf2 = classifier_rbf2.predict(X_test)
accuracy_rbf2 = classifier_rbf2.score(X_test, y_test)
y_score_rbf2 = classifier_rbf2.decision_function(X_test)


# For each class
precision_rbf2 = dict()
recall_rbf2 = dict()
average_precision_rbf2 = dict()
for i in range(n_classes):
    precision_rbf2[i], recall_rbf2[i], _ = precision_recall_curve(y_test[:, i], y_score_rbf2[:, i])
    average_precision_rbf2[i] = average_precision_score(y_test[:, i], y_score_rbf2[:, i])

# A "micro-average": quantifying score on all classes jointly
precision_rbf2["micro"], recall_rbf2["micro"], _ = precision_recall_curve(y_test.ravel(), y_score_rbf2.ravel())
average_precision_rbf2["micro"] = average_precision_score(y_test, y_score_rbf2, average="micro")
print('Average precision score, micro-averaged over all classes: {0:0.2f} for rbf kernel SVM'.format(average_precision_rbf2["micro"]))

plt.figure()
plt.step(recall_rbf2['micro'], precision_rbf2['micro'], color='b', alpha=0.2, where='post')
plt.fill_between(recall_rbf2["micro"], precision_rbf2["micro"], alpha=0.2, color='b')

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.title('Average precision score, micro-averaged over all classes: AP={0:0.2f} for rbf kernel SVM'.format(average_precision_rbf2["micro"]))
plt.show()

###################################################################
###################################################################
###################################################################

# Fitting SVM to the Training set using Polynomial kernel

from sklearn.multiclass import OneVsRestClassifier
classifier_poly2 = OneVsRestClassifier(SVC(kernel = 'poly', random_state = 0, gamma = 'auto'))
classifier_poly2.fit(X_train, y_train)

#Model Evaluation using K-fold Cross Validation
from sklearn.model_selection import cross_val_score
accuracies_poly2 = cross_val_score(estimator = classifier_poly2, X = X_train, y = y_train, cv = 5)
accuracies_poly2.mean()
accuracies_poly2.std()

y_pred_poly2 = classifier_poly2.predict(X_test)
accuracy_poly2 = classifier_poly2.score(X_test, y_test)
y_score_poly2 = classifier_poly2.decision_function(X_test)


# For each class
precision_poly2 = dict()
recall_poly2 = dict()
average_precision_poly2 = dict()
for i in range(n_classes):
    precision_poly2[i], recall_poly2[i], _ = precision_recall_curve(y_test[:, i], y_score_poly2[:, i])
    average_precision_poly2[i] = average_precision_score(y_test[:, i], y_score_poly2[:, i])

# A "micro-average": quantifying score on all classes jointly
precision_poly2["micro"], recall_poly2["micro"], _ = precision_recall_curve(y_test.ravel(), y_score_poly2.ravel())
average_precision_poly2["micro"] = average_precision_score(y_test, y_score_poly2, average="micro")
print('Average precision score, micro-averaged over all classes: {0:0.2f} for polynomial kernel SVM'.format(average_precision_poly2["micro"]))

plt.figure()
plt.step(recall_poly2['micro'], precision_poly2['micro'], color='b', alpha=0.2, where='post')
plt.fill_between(recall_poly2["micro"], precision_poly2["micro"], alpha=0.2, color='b')

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.title('Average precision score, micro-averaged over all classes: AP={0:0.2f} for polynomial kernel SVM'.format(average_precision_poly2["micro"]))
plt.show()

###################################################################
###################################################################
###################################################################

# Fitting SVM to the Training set using Sigmoid kernel

from sklearn.multiclass import OneVsRestClassifier
classifier_sigmoid2 = OneVsRestClassifier(SVC(kernel = 'sigmoid', random_state = 0, gamma = 'auto'))
classifier_sigmoid2.fit(X_train, y_train)

#Model Evaluation using K-fold Cross Validation
from sklearn.model_selection import cross_val_score
accuracies_sigmoid2 = cross_val_score(estimator = classifier_sigmoid2, X = X_train, y = y_train, cv = 5)
accuracies_sigmoid2.mean()
accuracies_sigmoid2.std()

y_pred_sigmoid2 = classifier_sigmoid2.predict(X_test)
accuracy_sigmoid2 = classifier_sigmoid2.score(X_test, y_test)
y_score_sigmoid2 = classifier_sigmoid2.decision_function(X_test)


# For each class
precision_sigmoid2 = dict()
recall_sigmoid2 = dict()
average_precision_sigmoid2 = dict()
for i in range(n_classes):
    precision_sigmoid2[i], recall_sigmoid2[i], _ = precision_recall_curve(y_test[:, i], y_score_sigmoid2[:, i])
    average_precision_sigmoid2[i] = average_precision_score(y_test[:, i], y_score_sigmoid2[:, i])

# A "micro-average": quantifying score on all classes jointly
precision_sigmoid2["micro"], recall_sigmoid2["micro"], _ = precision_recall_curve(y_test.ravel(), y_score_sigmoid2.ravel())
average_precision_sigmoid2["micro"] = average_precision_score(y_test, y_score_sigmoid2, average="micro")
print('Average precision score, micro-averaged over all classes: {0:0.2f} for sigmoid kernel SVM'.format(average_precision_sigmoid2["micro"]))

plt.figure()
plt.step(recall_sigmoid2['micro'], precision_sigmoid2['micro'], color='b', alpha=0.2, where='post')
plt.fill_between(recall_sigmoid2["micro"], precision_sigmoid2["micro"], alpha=0.2, color='b')

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.title('Average precision score, micro-averaged over all classes: AP={0:0.2f} for Sigmoid kernel SVM'.format(average_precision_sigmoid2["micro"]))
plt.show()



##################################################################
##################################################################
##################################################################
##################################################################
#Making the ANN
import keras
from keras.models import Sequential
from keras.layers import Dense


# Initialising the ANN
classifier_ann = Sequential()

# Adding the input layer and the first hidden layer
classifier_ann.add(Dense(output_dim = 12, init = 'uniform', activation = 'relu', input_dim = 17))

# Adding the second hidden layer
classifier_ann.add(Dense(output_dim = 12, init = 'uniform', activation = 'relu'))

# Adding the output layer
classifier_ann.add(Dense(output_dim = 7, init = 'uniform', activation = 'softmax'))

# Compiling the ANN
classifier_ann.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

# Fitting the ANN to the Training set
classifier_ann.fit(X_train, y_train, batch_size = 2, nb_epoch = 100)

# Predicting the Test set results
y_pred = classifier_ann.predict(X_test)
scores = classifier_ann.evaluate(X_test, y_test)
print("ACCURACY ON TEST SET USING NEURAL NETS")
print("%s: %.2f%%" % (classifier_ann.metrics_names[1], scores[1]*100))

#For Each Class, The average precision and recall and f1 scores
from sklearn.metrics import classification_report
Y_test_ann = np.argmax(y_test, axis=1) # Convert one-hot to index
y_pred_classes = classifier_ann.predict_classes(X_test)
print("PRECISION REALL TABLE using ANN")
classi_report = classification_report(Y_test_ann, y_pred_classes)
print(classification_report(Y_test_ann, y_pred_classes))























