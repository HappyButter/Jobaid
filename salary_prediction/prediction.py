import json
import numpy as np
import pandas as pd
import graphviz

from sklearn import preprocessing
from sklearn.tree import DecisionTreeRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import export_graphviz

with open('./ml-ready.json', 'r') as f:
    data = json.load(f)

# for record in data:
#     print(record)

# dataframe = pd.DataFrame(data)

for record in data:
    if record['experience_level'] is None:
        record['experience_level'] = "ndeclared"
    for num, language in enumerate(record['languages']):
        if num > 15: continue
        record[language] = language
    del record['languages']
    # for tech in record['technologies']:
    #     record[tech] = tech
    del record['technologies']
    # del record['company_size']


vec = DictVectorizer()
# # enc = preprocessing.OneHotEncoder()

preprocessed_data = vec.fit_transform(data).toarray()
print()
print(vec.get_feature_names()[:10])
print()


train = preprocessed_data[:-300]
test = preprocessed_data[-300:]

train_features = []
train_target = []

test_features = []
test_target = []

for record in train:
    train_features.append(record[:-1])
    train_target.append(record[-1])

for record in test:
    test_features.append(record[:-1])
    test_target.append(record[-1])


print() 
print(train_target[:10])
print()
print("Regression try:")
print()

regr = DecisionTreeRegressor(max_depth=11)
regr.fit(train_features, train_target)

# print(test_features)

predicted = regr.score(test_features, test_target)
print(test_target[:10])
# print(predicted[:10)
print(predicted)

print()
print()
importances = regr.feature_importances_

importances.sort()

print(importances[-10:])






# n_nodes = regr.tree_.node_count
# children_left = regr.tree_.children_left
# children_right = regr.tree_.children_right
# feature = regr.tree_.feature
# threshold = regr.tree_.threshold

# languages = ["Java", "Python", "JavaScript", "C++", "C#"]
# locations = ["Wrocław", "Warszawa", "Kraków"]
# experience = ["junior", "mid", "senior"]

# enc = preprocessing.OneHotEncoder(categories=[experience, locations, languages])

# train = [['language']]

# enc.fit(languages.reshape(1, -1))
# print(enc.transform(["Java", "C++"]).toarray())


# The tree structure can be traversed to compute various properties such
# as the depth of each node and whether or not it is a leaf.
# node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
# is_leaves = np.zeros(shape=n_nodes, dtype=bool)
# stack = [(0, -1)]  # seed is the root node id and its parent depth
# while len(stack) > 0:
#     node_id, parent_depth = stack.pop()
#     node_depth[node_id] = parent_depth + 1

#     # If we have a test node
#     if (children_left[node_id] != children_right[node_id]):
#         stack.append((children_left[node_id], parent_depth + 1))
#         stack.append((children_right[node_id], parent_depth + 1))
#     else:
#         is_leaves[node_id] = True

# print("The binary tree structure has %s nodes and has "
#       "the following tree structure:"
#       % n_nodes)
# for i in range(n_nodes):
#     if is_leaves[i]:
#         print("%snode=%s leaf node." % (node_depth[i] * "\t", i))
#     else:
#         print("%snode=%s test node: go to node %s if X[:, %s] <= %s else to "
#               "node %s."
#               % (node_depth[i] * "\t",
#                  i,
#                  children_left[i],
#                  feature[i],
#                  threshold[i],
#                  children_right[i],
#                  ))
# print()
# print()










def export_tree_to_file(tree_model, filename, format):
    dot_data = export_graphviz(tree_model, out_file=None,  # don't save to file yet
                           feature_names=vec.get_feature_names()[:-1], # fill this argument!
                        #    class_names=vec.get_feature_names(), # fill this argument!
                           filled=True, rounded=True,
                           special_characters=True)

    graph = graphviz.Source(dot_data)
    graph.render(filename, format="png")  # here we can choose from many formats


def display_tree_from_file(filename):
    display(Image(filename=filename))

export_tree_to_file(regr, "salary_prediction", "png")
# display_tree_from_file("breast_cancer_tree.png")