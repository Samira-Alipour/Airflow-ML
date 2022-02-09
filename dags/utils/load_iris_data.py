import numpy as np
import pandas as pd
from utils.files_util import save_files
from sklearn import datasets 
    
def load_iris_data():
    iris = datasets.load_iris()
    n = len(iris.data)
    labels = np.reshape(iris.target, (n,1))
    df = pd.DataFrame(np.concatenate([iris.data, labels], axis=1))
    df.columns = np.append(iris.feature_names, 'label')
    df.name="df"
    save_files([df])

