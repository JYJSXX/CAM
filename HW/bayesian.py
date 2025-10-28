import sklearn.naive_bayes as nb
import csv

if __name__ == "__main__":
    with open("Bayesian_Dataset_train.csv", "r") as f:
        reader = csv.reader(f)
        raw_data = []
        for row in reader:
            raw_data.append(row)

    data = [row[0:7] + row[8:-1] for row in raw_data]
    clf = nb.GaussianNB()
    clf.fit(data, [row[-1] for row in raw_data])
    with open("Bayesian_Dataset_test.csv", "r") as f:
        reader = csv.reader(f)
        test_data = []
        for row in reader:
            test_data.append(row)
    test_data = [row[0:7] + row[8:-1] for row in test_data]
    predictions = clf.predict(test_data)
    print(predictions)