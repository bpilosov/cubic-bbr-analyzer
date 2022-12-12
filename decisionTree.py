import csv
from io import StringIO

import pandas as pd
import pydotplus
from IPython.display import Image
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz

expName = "mean60sec27tests"
csvname_bt = expName + "-bwTree.csv"
csvname_lt = expName + "-lossTree.csv"

df = pd.read_csv(expName + ".csv", header=0)
# print(df)

bbrBw, cubicBw = {}, {}
bbrLoss, cubicLoss = {}, {}
bwTree, lossTree = {}, {}
bbrKeys, cubicKeys, commonKeys = set(), set(), set()

# Show the data size
rows, cols = df.shape
# print('Data size: ' + str(df.shape))

# Class Label: 0->bbr, 1->cubic
label = {'bbr': 0, 'cubic': 1}


# Bw/Loss decision map
def mapping():
    for index, rowData in df.iterrows():

        key = str(rowData["delay"]) + "-" + str(rowData['bandwidth']) + "-" + str(rowData['buffer_size'])

        if rowData['algorithm'] == 'bbr':
            bbrKeys.add(key)
            bbrBw[key], bbrLoss[key] = rowData['goodput'], 100 * rowData['loss_rate']
        elif rowData['algorithm'] == 'cubic':
            cubicKeys.add(key)
            cubicBw[key], cubicLoss[key] = rowData['goodput'], 100 * rowData['loss_rate']

    for key in bbrKeys:
        if key in cubicKeys:
            commonKeys.add(key)
            # bw decision
            if bbrBw[key] < cubicBw[key]:
                bwTree[key] = label['cubic']
            else:
                bwTree[key] = label['bbr']
            # loss decision
            if bbrLoss[key] < cubicLoss[key]:
                lossTree[key] = label['bbr']
            else:
                lossTree[key] = label['cubic']


def treeCSV():
    # Creating the bwTree/lossTree (csv)
    csvfile_bt = open(csvname_bt, 'w')
    csvfile_lt = open(csvname_lt, 'w')
    writer_bt = csv.writer(csvfile_bt)
    writer_lt = csv.writer(csvfile_lt)

    header = ['Delay', 'Bw', 'Buffer', 'Decision']
    writer_bt.writerow(header)
    writer_lt.writerow(header)

    for key in commonKeys:
        tokens = key.split('-')
        record_bt = [tokens[0], tokens[1], tokens[2], bwTree[key]]
        record_lt = [tokens[0], tokens[1], tokens[2], lossTree[key]]

        writer_bt.writerow(record_bt)
        writer_lt.writerow(record_lt)

    csvfile_bt.close()
    csvfile_lt.close()


# Creating the decision tree (model)
def dtModel(filename, metric):
    df_Dtree = pd.read_csv(filename, header=0)
    feature_cols = ['Delay', 'Bw', 'Buffer']
    X = df_Dtree[feature_cols]
    y = df_Dtree.Decision
    # print(X)
    # print(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

    clf = DecisionTreeClassifier()
    # Regression does not apply here
    # clf = DecisionTreeRegressor()
    clf = clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print("Model accuracy (" + metric + "): " + str(metrics.accuracy_score(y_test, y_pred)))
    return [clf, feature_cols]


# Plot
def plotTree(clf, feature_cols, metric):
    dot_data = StringIO()
    export_graphviz(clf, out_file=dot_data,
                    filled=True, rounded=True,
                    special_characters=True,
                    feature_names=feature_cols,
                    # max_depth=5,
                    class_names=['bbr', 'cubic']
                    )

    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_png(expName + "-" + metric + 'Tree.png')
    Image(graph.create_png())


if __name__ == "__main__":
    mapping()
    treeCSV()

    # Build decision tree and visualize
    [clf, feature_cols] = dtModel(csvname_bt, 'bw')
    plotTree(clf, feature_cols, 'bw')

    [clf, feature_cols] = dtModel(csvname_lt, 'loss')
    plotTree(clf, feature_cols, 'loss')
