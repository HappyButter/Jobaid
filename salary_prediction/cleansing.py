import json
import numpy as np
import pandas as pd
import graphviz
import copy
import csv


# from sklearn import preprocessing
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.ensemble import RandomForestRegressor
# from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import export_graphviz
import matplotlib.pyplot as plt
# from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
# from sklearn.metrics import confusion_matrix
# from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import cross_val_score

cities = [
    ['warszawa', 'warsaw'],
    ['kraków', 'cracow'],
    ['wrocław', 'wroclaw'],
    ['gdańsk', 'gdansk'],
    ['szczecin'],
    ['katowice'],
    ['poznań', 'poznan'],
    ['gdynia'],
    ['gliwice'],
    ['łódź'],
    ['remote', 'zdalnie', 'remotely']
]

languages = ['python', 'java', 'javascript', 'sql', 'html', 'c#', 'typescript', 'c++', 'php', 'go', 'r', 'c', 'nosql', 'scala',     'rust', 'ruby', 'kotlin']

technologies = ['docker', 'agile', 'linux', 'aws', 'rest', 'angular', 'react','jira', 'azure', '.net', 'postgresql', 'hibernate', 'node', 'mongo', 'maven', 'postgre', 'django', 'laravel', 'express', 'vue', 'django', 'flask', 'spring', 'redux', 'mysql', 'kubernetes']


def load_training_dataset():
    with open('./salary_prediction/ml_uop.json', 'r') as f1, open('./salary_prediction/ml_b2b.json', 'r') as f2:
        data = json.load(f1)
        for offer in data:
            offer['uop'] = 1
            offer['b2b'] = 0
        rest = json.load(f2)
        for offer in rest:
            offer['uop'] = 0
            offer['b2b'] = 1
    data.extend(rest)
    return data


def extract_experience(user_data):
    for experience in ['mid', 'senior', 'junior', 'juniormid', 'midsenior']:
        if user_data['experience'][0] == experience:
            user_data[experience] = 1
        else:
            user_data[experience] = 0


def extract_city(user_data):
    for city_options in cities:
        for city in city_options:
            if city == user_data['city'].lower():
                user_data[city_options[0]] = 1
                break
            else:
                user_data[city_options[0]] = 0


# def extract_languages(user_data):
#     for language in languages:
#         for skill in user_data['technologies']:
#             if language == skill.lower():
#                 user_data[language] = 1
#                 print("JEST KURWWAA JEZYK")
#             else:
#                 user_data[language] = 0


# def extract_technologies(user_data):
#     for technology in technologies:
#         user_data[technology] = 0

#     for tech in user_data['technologies']:
#         user_data[tech] = 1 if tech in technologies else 0


def encode_skills(user_data):
    for technology in technologies:
        user_data[technology] = 1 if technology in user_data['technologies'] else 0

    for language in languages:
        user_data[language] = 1 if language in user_data['technologies'] else 0


def preprocess_loaded_data(data):
    cleaned = []
    for offer in data:
        cleaned_offer = {}
        for city_options in cities:
            for city in city_options:
                if city == offer['location'].lower():
                    cleaned_offer['city'] = city_options[0]
                    break
        
        for language in languages:
            for lang in offer['languages']:
                if language == lang.lower():
                    cleaned_offer[language] = language
        
        for technology in technologies:
            for tech in offer['technologies']:
                if technology == tech.lower():
                    cleaned_offer[technology] = technology

        if offer['experience_level'] is not None:
            cleaned_offer['experience'] = offer['experience_level']
        else: 
            cleaned_offer['experience'] = 'unspecified'

        cleaned_offer['size'] = offer['company_size'] if offer['company_size'] is not None else 'notgiven'
        cleaned_offer['salary'] = offer['salary']
        cleaned_offer['b2b'] = offer['b2b']
        cleaned_offer['uop'] = offer['uop']
        if len(cleaned_offer.keys()) < 10:
            continue
        cleaned.append(cleaned_offer)
    return cleaned


def create_dataframe_and_encode(data):
    columns = languages.copy()
    columns.extend(technologies)

    df = pd.DataFrame(data)
    df = pd.get_dummies(df, columns=columns.extend(['experience', 'city']), prefix='', prefix_sep='')

    df.to_csv('cleaned.csv')
    return df


def prepare_and_encode_record(user_input, features):
    record = copy.deepcopy(user_input)
    extract_city(record)
    extract_experience(record)

    record['uop'] = int(record['uop'])
    record['b2b'] = int(record['b2b'])
    record['size'] = 1007
    record['unspecified'] = 0
    encode_skills(record)
    del record['technologies']
    del record['city']
    del record['experience']
    df = pd.DataFrame(data=record, columns=features, index=[0]).drop('salary', axis=1).copy()

    return df


def split_training_data(dataframe, target):
    X_encoded = dataframe.drop('salary', axis=1).copy()
    y = dataframe[target].copy()
    return train_test_split(X_encoded, y, random_state=42)


def train_model():
    print('training model')
    data = load_training_dataset()
    preprocessed = preprocess_loaded_data(data)
    dataframe = create_dataframe_and_encode(preprocessed)
    X_train, X_test, y_train, y_test = split_training_data(dataframe, 'salary')

    best_alpha = 0.4377
    dt_regr = RandomForestRegressor(n_estimators=300, ccp_alpha=best_alpha, max_depth=19, min_samples_split=4, min_samples_leaf=2)
    dt_regr.fit(X_train, y_train)
    score = dt_regr.score(X_test, y_test)
    print(f'score: {score}')
    predicted = dt_regr.predict(X_test)
    print(calculate_accuracy(y_test, predicted, 10, 1000))
    # generate_accuracy_plot(y_test, predicted, 10, 1000)
    return dt_regr, dataframe.columns



# regr = DecisionTreeRegressor(random_state=20)
# regr.fit(X_train, y_train)


# print(X_test[:10])
# print(y_test[:10])
# predicted = regr.predict(X_test)

# path = regr.cost_complexity_pruning_path(X_train, y_train)
# ccp_alphas = path.ccp_alphas
# ccp_alphas = ccp_alphas[:-1]

# regr_list = []

# for ccp_alpha in ccp_alphas:
#     reg = DecisionTreeRegressor(random_state=0, ccp_alpha=ccp_alpha)
#     reg.fit(X_train, y_train)
#     regr_list.append(reg)


# train_scores = [reg.score(X_train, y_train) for reg in regr_list]
# test_scores = [reg.score(X_test, y_test) for reg in regr_list]


# fig, ax = plt.subplots()

# ax.set_xlabel('alpha')
# ax.set_ylabel('MSE')
# ax.set_title('MSE against alpha for training and testing sets')
# ax.plot(ccp_alphas, train_scores, marker='o', label='train', drawstyle='steps-post')
# ax.plot(ccp_alphas, test_scores, marker='o', label='test', drawstyle='steps-post')
# ax.legend()
# plt.show()



# alpha_loop_values = []
# for ccp_alpha in ccp_alphas:
#     reg = DecisionTreeRegressor(random_state=0, ccp_alpha=ccp_alpha)
#     scores = cross_val_score(reg, X_train, y_train, cv=3)
#     alpha_loop_values.append(scores)


# alpha_results = pd.DataFrame(alpha_loop_values, columns=['alpha', 'mse', 'std'])
# print(alpha_results)
# alpha_results.plot(x='alpha', y='mse', yerr='std', marker='o', linestyle='--')
# plt.errorbar(x=alpha_results['alpha'], y=alpha_results['mse'], yerr=alpha_results['std'], marker='o', linestyle='--')
# plt.show()

# best_alpha = alpha_results[(alpha_results['alpha'] > 0.208) & (alpha_results['alpha'] < 0.209)]
# print(best_alpha)
# best_alpha = 0.437625
# best_alpha = 0.4378

# pruned_regr = RandomForestRegressor(n_estimators=300, ccp_alpha=best_alpha, max_depth=19, min_samples_split=4, min_samples_leaf=2)
# # pruned_regr = RandomForestRegressor(n_estimators=300, ccp_alpha=best_alpha, max_depth=13, min_samples_split=3, min_samples_leaf=6)
# # pruned_regr = DecisionTreeRegressor(ccp_alpha=best_alpha, max_depth=17, min_samples_split=5, min_samples_leaf=2)
# pruned_regr.fit(X_train, y_train)
# score = pruned_regr.score(X_test, y_test)
# print(f'score: {score}')
# predicted = pruned_regr.predict(X_test)

def calculate_accuracy(target, pred, error_percent, error_fixed):
    accurate_count = 0
    for real, pred in zip(target, pred):
        if real*(1 - error_percent/100) - error_fixed <= pred <= real*(1 + error_percent/100) + error_fixed:
            accurate_count += 1
    print('accurate shots: ', accurate_count)
    print('total test count: ', len(target))
    return accurate_count/len(target)


def generate_accuracy_plot(target, pred, error_percent, error_fixed):
    target, pred = zip(*sorted(zip(target, pred)))
    target, pred = (list(t) for t in zip(*sorted(zip(target, pred))))

    lower_bound = [value*(1 - error_percent/100) - error_fixed for value in target]
    upper_bound = [value*(1 + error_percent/100) + error_fixed for value in target]

    plt.scatter(target, pred, s=5)
    plt.plot(target, target, '-r')
    plt.fill_between(target, lower_bound, upper_bound, color="gray", alpha=0.2)

    plt.show()

# print(calculate_accuracy(y_test, predicted, 10, 1000))
# generate_accuracy_plot(y_test, predicted, 10, 1000)


def export_tree_to_file(tree_model, filename, format):
    dot_data = export_graphviz(tree_model, out_file=None,  # don't save to file yet
                           feature_names=X_train.columns, # fill this argument!
                        #    class_names=vec.get_feature_names(), # fill this argument!
                           filled=True, rounded=True,
                           special_characters=True)

    graph = graphviz.Source(dot_data)
    graph.render(filename, format="png")  # here we can choose from many formats


# export_tree_to_file(pruned_regr, "alphaPruned_gridsearch", "png")

def initialize_learning():
    print('initialize learining')
    return train_model()