import numpy as np
import sklearn.naive_bayes as nb
from sklearn.preprocessing import LabelEncoder
import csv
from sklearn.metrics import precision_score, recall_score, f1_score


if __name__ == "__main__":
    with open("Bayesian_Dataset_train.csv", "r") as f:
        reader = csv.reader(f)
        data = []
        for row in reader:
            data.append(row[0:7] + row[8:])
    with open("Bayesian_Dataset_test.csv", "r") as f:
        reader = csv.reader(f)
        test_data = []
        for row in reader:
            test_data.append(row[0:7] + row[8:])
    data = np.array(data)
    test_data = np.array(test_data)
    all_data = np.concatenate((data, test_data), axis=0).transpose()
    les = []
    for i in range(10):
        le = LabelEncoder()
        le.fit(all_data[i])
        les.append(le)

    encoded_data = np.array([les[i].transform(data.transpose()[i]) for i in range(10)]).transpose()
    print(encoded_data.shape)
    x = encoded_data[:, :-1]
    y = encoded_data[:, -1]
    clf = nb.GaussianNB()
    clf.fit(x, y)
    encoded_test_data = np.array([les[i].transform(test_data.transpose()[i]) for i in range(10)]).transpose()
    x_test = encoded_test_data[:, :-1]
    y_test = encoded_test_data[:, -1]
    predictions = clf.predict(x_test)
    print(predictions.shape)
    print(predictions[:-10])

    #recall
    recall = recall_score(y_test, predictions, pos_label=1)
    print("recall:", recall)
    precision = precision_score(y_test, predictions, pos_label=1)
    print("precision:", precision)
    # f1 score
    f1 = f1_score(y_test, predictions, pos_label=1)
    print("f1 score:", f1)

    data = []
    with open("bayesian_result.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Prediction", "Actual"])
        for i in range(len(predictions)):
            writer.writerow([">50K" if predictions[i] == 1 else "<=50K"])
        