import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import ipywidgets as widgets
from scipy.linalg import lstsq
from sklearn.metrics import mean_squared_error as mse
from IPython.display import display,clear_output
from sklearn.model_selection import train_test_split

def make_X(df, var_names):
    """Given a DataFrame and a list of explanatory variables, one-hot encodes
    variables if they are categorical and returns a dataframe with 
    all the given explanatory variables."""
    categorical = ["month", "week day", "season"]
    boolean = ["is holiday", "is work day"]
    X = pd.DataFrame({"intercept":np.ones(df.shape[0], dtype='int')}, index = df.index)
    for var in var_names:
        if var in categorical:
            dummies = pd.get_dummies(df[var])
            formatted = dummies.drop(dummies.columns[-1], axis=1)
        elif var in boolean:
            formatted = (df[var] == "yes") * 1
        else:
            formatted = df.loc[:, var]
        X = X.join(formatted)
      
    return X

def predict(response_var, fit_intercept, **kwargs):
    plt.close()
    # select and format X and y
    y_train = bike_train[response_var]
    y_val = bike_val[response_var]
    
    expl_vars = [var for var in kwargs if kwargs[var]]
    
    # bounce if there's no variables for the model
    if len(expl_vars) == 0 and not fit_intercept:
        print("Please select at least one explanatory variable to include in the model.")
        return
    
    X_train = make_X(bike_train, expl_vars)
    X_val = make_X(bike_val, expl_vars)
    
    if not fit_intercept:
        X_train.drop("intercept", axis=1, inplace=True)
        X_val.drop("intercept", axis=1, inplace=True)
    
    # calculate beta
    beta = lstsq(X_train, y_train)[0]
    
    # make predictions
    pred_train = X_train @ beta
    pred_val = X_val @ beta
    
    # generate plots 
    f, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=(12, 12))

    sns.regplot(x=y_train, y=pred_train, ax=ax1, color="#003262") 
    ax1.set_xlabel(response_var)
    ax1.set_ylabel("predicted {}".format(response_var))
    ax1.set_title("Predicted vs. Actual Values (Training Data)")
    
    sns.regplot(x=y_val, y=pred_val, ax=ax2, color="#FDB515")
    ax2.set_xlabel(response_var)
    ax2.set_ylabel("predicted {}".format(response_var))
    ax2.set_title("Predicted vs. Actual Values (Validation Data)")
    
    sns.regplot(x=y_train, y=y_train - pred_train, ax=ax3, color="#003262") 
    ax3.set_xlabel(response_var)
    ax3.set_ylabel("error ({} - predicted {})".format(response_var, response_var))
    ax3.set_title("Error (Training Data)")
    
    sns.regplot(x=y_val, y=y_val - pred_val, ax=ax4, color="#FDB515")
    ax4.set_xlabel(response_var)
    ax4.set_ylabel("error ({} - predicted {})".format(response_var, response_var))
    ax4.set_title("Error (Validation Data)")
            
    
    # calculate rmse
    print("Training data RMSE = {}".format(np.sqrt(mse(pred_train, y_train))))
    print("Validation data RMSE = {}".format(np.sqrt(mse(pred_val, y_val))))
    
    print("\u03B2: {}".format(beta))
    
np.random.seed(28)
bikes = pd.read_csv("../data/day_renamed_dso.csv", index_col=0)
bike_train, rest_of_bikes = train_test_split(bikes, test_size=0.2)
bike_val, bike_test = train_test_split(rest_of_bikes, test_size=0.5)

        
expl_vars = [widgets.ToggleButton(description=var) for var in bikes.columns[1:13]]
expl_buttons = widgets.Box(expl_vars)

response_radio = widgets.RadioButtons(
    options=['total riders', 'casual riders', 'registered riders'],
    description='Response variable:'
)

intercept = widgets.ToggleButton(description="intercept")

kwargs = {bike_train.columns[1:12][i]: expl_vars[i] for i in range(11)}
kwargs['fit_intercept'] = intercept
kwargs['response_var'] = response_radio
out = widgets.interactive_output(predict, kwargs)
out.layout.height = '800px'