from sklearn.model_selection import GridSearchCV 
from sklearn.tree import DecisionTreeRegressor

import json
import numpy as np
import pandas as pd
import graphviz

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
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
        ['Lódź'],
        ['remote', 'zdalnie', 'remotely']
    ]

languages = ['python', 'java', 'javascript', 'sql', 'html', 'c#', 'typescript', 'c++', 'php', 'go', 'r', 'c', 'nosql', 'scala',     'rust', 'ruby', 'kotlin']

technologies = ['docker', 'agile', 'linux', 'aws', 'rest', 'angular', 'react','jira', 'azure', '.net', 'postgresql', 'hibernate', 'node', 'mongo', 'maven', 'postgre', 'django', 'laravel', 'express', 'vue', 'django', 'flask', 'spring', 'redux', 'mysql', 'kubernetes']



if __name__ == '__main__':

    df = pd.read_csv('cleaned.csv').drop(["Unnamed: 0"],axis=1)

    columns = languages.copy()
    columns.extend(technologies)

    df = pd.get_dummies(df, columns=columns.extend(['experience', 'city']), prefix='', prefix_sep='')

    print()
    print(df.shape)
    print()

    X_encoded = df.drop('salary', axis=1).copy()
    y = df['salary'].copy()

    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, random_state=42)


    # n_estimators = [200, 300]
    max_depths = [11,13,15,17,19,21, 23]
    min_samples_leaf = [1,2,3,4,5,6,7]
    min_samples_split = [3,4,5,6,7,8,9,10]

    grid_params = {
        # 'n_estimators': n_estimators,
        'max_depth': max_depths,
        'min_samples_leaf': min_samples_leaf,
        'min_samples_split': min_samples_split
    }

    regressor = DecisionTreeRegressor(ccp_alpha=0.140267)
    # regressor = RandomForestRegressor(ccp_alpha=0.437625)

    grid_src = GridSearchCV(
        estimator=regressor,
        param_grid=grid_params,
        cv=5,
        n_jobs=-1
    )

    grid_src.fit(X_train, y_train)

    best_params = grid_src.best_params_
    print(best_params)

    best_score = grid_src.best_score_
    print(best_score)