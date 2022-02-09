import numpy as np
import pandas as pd
from datetime import datetime

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from utils.files_util import save_files, load_files
import utils.ml_pipeline_config as config


def experiment():

    x_train, x_test, y_train, y_test = load_files(['x_train', 'x_test', 'y_train', 'y_test'])
    
    cv_folds = config.params["cv_folds"] 
    logreg_maxiter = config.params["logreg_maxiter"]

    std_scaler = StandardScaler()
    log_reg = LogisticRegression(max_iter=logreg_maxiter)


    params = {'C': np.logspace(0.05, 0.1, 1)}

    # cross-validated training through grid search
    grid_search = GridSearchCV(log_reg, params, cv=cv_folds)
    grid_search.fit(x_train, y_train)

    best_c = round(grid_search.best_params_.get("C"),2)
    
    y_test_predicted = grid_search.best_estimator_.predict(x_test)
    test_set_accuracy = round(accuracy_score(y_test, y_test_predicted),3)

    now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

    exp_info = pd.DataFrame([[now,
                          cv_folds,
                          logreg_maxiter,
                          # max_pca_components,
                          best_c,
                          # best_princ_comp,
                          test_set_accuracy]],
                          columns=['experiment_datetime',
                                   'cv_folds',
                                   'logreg_maxiter',
                                   'best_logreg_c',
                                   'test_set_accuracy'
                                   ])
    exp_info.name = 'exp_info'

    save_files([exp_info])