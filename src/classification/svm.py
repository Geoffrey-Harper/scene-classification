import numpy as np
from sklearn import svm
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
import cv2
import matplotlib.pyplot as plt
import itertools
import time
from sklearn.neighbors import KNeighborsClassifier

# can pass in pre-trained models
def SVM(data, C, model=None):
    
    if model is None:
        model = svm.LinearSVC(C = C)
        model.fit(data['Z_train'], data['Y_train'])
    
    return generate_results(data['Z_train'], data['Y_train'], model, save=False), generate_results(data['Z_test'], data['Y_test'], model, save=True)

def kernel_SVM(data, C=1, gamma='auto', kernel='rbf', model=None):
    
    if model is None:
        model = SVC(gamma='auto', C=C, kernel=kernel)
        model.fit(data['Z_train'], data['Y_train'])
    
    return generate_results(data['Z_train'], data['Y_train'], model, save=False), generate_results(data['Z_test'], data['Y_test'], model, save=True)


def KNN(data, N, model=None):

    if model is None:
        model = KNeighborsClassifier(n_neighbors=N)
        model.fit(data['Z_train'], data['Y_train'])
    
    return generate_results(data['Z_train'], data['Y_train'], model, save=False), generate_results(data['Z_test'], data['Y_test'], model, save=True)


# taken from a3
def generate_results(X, y, model, save=False):
    results = {"accuracy" : 0,
               "recall" : 0,
               "precision" : 0,
               "avg_recall" : 0,
               "avg_precision" : 0,
               "fscore" : 0}

    pred = model.predict(X)
    cm = confusion_matrix(y,pred).astype(np.float32)
    # epsilon for non zero entries
    EPS=1e-6

    #From the confusion matrix, calculate precision/recall/f1-measure
    results['recall'] = np.diag(cm) / (np.sum(cm, axis=1) + EPS)
    results['avg_recall'] = np.mean(results['recall'])

    results['precision'] = np.diag(cm) / (np.sum(cm, axis=0) + EPS)
    results['avg_precision'] = np.mean(results['precision'])

    results["fscore"] = 2 * ( results['avg_precision'] * results['avg_recall'] ) / (results['avg_precision'] + results['avg_recall'] + EPS)

    results["accuracy"] = np.mean(pred == y)

    plot_confusion_matrix(cm, save=save)

    return results


def plot_confusion_matrix(cm, title="Confusion Matrix", save=True):
    plt.figure()
    classes = np.arange(cm.shape[0])
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], '.2f'),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

    if save:
        plt.savefig(title.format(title), bbox_inches='tight')
        return


