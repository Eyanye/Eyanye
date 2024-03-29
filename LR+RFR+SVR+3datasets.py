{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Eyanye/Eyanye/blob/main/LR%2BRFR%2BSVR%2B3datasets.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "background_save": true
        },
        "id": "yt0NTtYuxZpM"
      },
      "outputs": [],
      "source": [
        "import numpy as np\n",
        "import pandas as pd\n",
        "from sklearn.preprocessing import StandardScaler\n",
        "from sklearn.model_selection import GridSearchCV\n",
        "from sklearn.linear_model import SGDRegressor\n",
        "import plotly.graph_objs as go\n",
        "import plotly.figure_factory as ff\n",
        "\n",
        "# Importing dataset and examining it\n",
        "dataset = pd.read_csv(\"/content/CarResale.csv\")\n",
        "pd.set_option('display.max_columns', None) # to make sure you can see all the columns in output window\n",
        "print(dataset.head())\n",
        "print(dataset.shape)\n",
        "print(dataset.info())\n",
        "print(dataset.describe())\n",
        "\n",
        "# Converting Categorical features into Numerical features\n",
        "dataset['fuel'] = dataset['fuel'].map({'Diesel': 1, 'Petrol':0})\n",
        "dataset['seller_type'] = dataset['seller_type'].map({'Dealer': 1, 'Individual':0})\n",
        "dataset['transmission'] = dataset['transmission'].map({'Automatic': 1, 'Manual':0})\n",
        "dataset['owner'] = dataset['owner'].map({'Fourth & Above Owner': 4, 'Third Owner': 3, 'Second Owner': 2, 'First Owner':1, 'Test Drive Car':0})\n",
        "print(dataset.info())\n",
        "\n",
        "# Plotting Correlation Heatmap\n",
        "corrs = dataset.corr()\n",
        "figure = ff.create_annotated_heatmap(\n",
        "    z=corrs.values,\n",
        "    x=list(corrs.columns),\n",
        "    y=list(corrs.index),\n",
        "    annotation_text=corrs.round(2).values,\n",
        "    showscale=True)\n",
        "figure.show()\n",
        "\n",
        "# # Dividing dataset into label and feature sets\n",
        "X = dataset.drop('engine_size', axis = 1) # Features\n",
        "Y = dataset['selling_price'] # Labels\n",
        "print(type(X))\n",
        "print(type(Y))\n",
        "print(X.shape)\n",
        "print(Y.shape)\n",
        "\n",
        "# Normalizing numerical features so that each feature has mean 0 and variance 1\n",
        "feature_scaler = StandardScaler()\n",
        "X_scaled = feature_scaler.fit_transform(X)\n",
        "\n",
        "# Linear Regression with Regularization\n",
        "# Tuning the SGDRegressor parameters 'eta0' (learning rate) and 'max_iter', along with the regularization parameter alpha using Grid Search\n",
        "sgdr = SGDRegressor(random_state = 1, penalty = 'elasticnet')\n",
        "grid_param = {'eta0': [.0001, .001, .01, .1, 1], 'max_iter':[10000, 20000, 30000, 40000],'alpha': [.001, .01, .1, 1,10, 100], 'l1_ratio': [0,0.25,0.5,0.75,1]}\n",
        "\n",
        "gd_sr = GridSearchCV(estimator=sgdr, param_grid=grid_param, scoring='r2', cv=5)\n",
        "\n",
        "gd_sr.fit(X_scaled, Y)\n",
        "\n",
        "best_parameters = gd_sr.best_params_\n",
        "print(\"Best parameters: \", best_parameters)\n",
        "\n",
        "best_result = gd_sr.best_score_ # Mean cross-validated score of the best_estimator\n",
        "print(\"r2: \", best_result)\n",
        "\n",
        "Adj_r2 = 1-(1-best_result)*(6240-1)/(6240-9-1)\n",
        "print(\"Adjusted r2: \", Adj_r2)\n",
        "\n",
        "# '''\n",
        "# Adj_r2 = 1-(1-r2)*(n-1)/(n-p-1)\n",
        "\n",
        "# where, n = number of observations, p = number of features\n",
        "# '''\n",
        "\n",
        "best_model = gd_sr.best_estimator_\n",
        "print(\"Intercept: \", best_model.intercept_)\n",
        "\n",
        "print(pd.DataFrame(zip(X.columns, best_model.coef_), columns=['Features','Coefficients']).sort_values(by=['Coefficients'],ascending=False))"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "75cr_OkTxaHZ"
      },
      "source": []
    },
    {
      "cell_type": "code",
      "source": [
        "import numpy as np\n",
        "import pandas as pd\n",
        "from sklearn.preprocessing import StandardScaler\n",
        "from sklearn.model_selection import GridSearchCV\n",
        "from sklearn.ensemble import RandomForestRegressor\n",
        "from sklearn.linear_model import SGDRegressor\n",
        "import plotly.graph_objs as go\n",
        "import plotly.figure_factory as ff\n",
        "\n",
        "# Importing dataset and examining it\n",
        "dataset = pd.read_csv(\"/content/LimitPrediction.csv\")\n",
        "pd.set_option('display.max_columns', None) # to make sure you can see all the columns in output window\n",
        "print(dataset.head())\n",
        "print(dataset.shape)\n",
        "print(dataset.info())\n",
        "print(dataset.describe())\n",
        "\n",
        "# Converting Categorical features into Numerical features\n",
        "dataset['Gender'] = dataset['Gender'].map({' Male': 1, 'Female':0})\n",
        "dataset['Student'] = dataset['Student'].map({'Yes': 1, 'No':0})\n",
        "dataset['Married'] = dataset['Married'].map({'Yes': 1, 'No':0})\n",
        "print(dataset.info())\n",
        "\n",
        "categorical_features = ['Ethnicity']\n",
        "final_data = pd.get_dummies(dataset, columns = categorical_features, drop_first= True)\n",
        "print(final_data.info())\n",
        "print(final_data.head(2))\n",
        "\n",
        "# Plotting Correlation Heatmap\n",
        "corrs = dataset.corr()\n",
        "figure = ff.create_annotated_heatmap(\n",
        "    z=corrs.values,\n",
        "    x=list(corrs.columns),\n",
        "    y=list(corrs.index),\n",
        "    annotation_text=corrs.round(2).values,\n",
        "    showscale=True)\n",
        "figure.show()\n",
        "\n",
        "# Dividing dataset into label and feature sets\n",
        "X = final_data.drop(['Customer Id', 'Limit'], axis = 1) # Features\n",
        "Y = dataset['Limit'] # Labels\n",
        "print(type(X))\n",
        "print(type(Y))\n",
        "print(X.shape)\n",
        "print(Y.shape)\n",
        "\n",
        "# Normalizing numerical features so that each feature has mean 0 and variance 1\n",
        "feature_scaler = StandardScaler()\n",
        "X_scaled = feature_scaler.fit_transform(X)\n",
        "\n",
        "# Linear Regression with Regularization\n",
        "# Tuning the SGDRegressor parameters 'eta0' (learning rate) and 'max_iter', along with the regularization parameter alpha using Grid Search\n",
        "sgdr = SGDRegressor(random_state = 1, penalty = 'elasticnet')\n",
        "grid_param = {'eta0': [.0001, .001, .01, .1, 1], 'max_iter':[10000, 20000, 30000, 40000],'alpha': [.001, .01, .1, 1,10, 100], 'l1_ratio': [0.25,0.5,0.75]}\n",
        "\n",
        "gd_sr = GridSearchCV(estimator=sgdr, param_grid=grid_param, scoring='r2', cv=5)\n",
        "\n",
        "gd_sr.fit(X_scaled, Y)\n",
        "\n",
        "best_parameters = gd_sr.best_params_\n",
        "print(\"Best parameters: \", best_parameters)\n",
        "\n",
        "best_result = gd_sr.best_score_ # Mean cross-validated score of the best_estimator\n",
        "print(\"r2: \", best_result)\n",
        "\n",
        "Adj_r2 = 1-(1-best_result)*(320-1)/(320-11-1)\n",
        "print(\"Adjusted r2: \", Adj_r2)\n",
        "\n",
        "# '''\n",
        "# Adj_r2 = 1-(1-r2)*(n-1)/(n-p-1)\n",
        "\n",
        "# where, n = number of observations in training data, p = number of features\n",
        "# '''\n",
        "\n",
        "best_model = gd_sr.best_estimator_\n",
        "print(\"Intercept: \", best_model.intercept_)\n",
        "\n",
        "print(pd.DataFrame(zip(X.columns, best_model.coef_), columns=['Features','Coefficients']).sort_values(by=['Coefficients'],ascending=False))\n",
        "\n",
        "##################################################################################\n",
        "# Implementing Random Forest Regression\n",
        "# Tuning the random forest parameter 'n_estimators' and implementing cross-validation using Grid Search\n",
        "rfr = RandomForestRegressor(criterion='squared_error', max_features='sqrt', random_state=1)\n",
        "grid_param = {'n_estimators': [10,20,30,40,50,100]}\n",
        "\n",
        "gd_sr = GridSearchCV(estimator=rfr, param_grid=grid_param, scoring='r2', cv=5)\n",
        "\n",
        "gd_sr.fit(X_scaled, Y)\n",
        "\n",
        "best_parameters = gd_sr.best_params_\n",
        "print(\"Best parameters: \", best_parameters)\n",
        "\n",
        "best_result = gd_sr.best_score_ # Mean cross-validated score of the best_estimator\n",
        "print(\"r2: \", best_result)\n",
        "\n",
        "Adj_r2 = 1-(1-best_result)*(320-1)/(320-11-1)\n",
        "print(\"Adjusted r2: \", Adj_r2)\n",
        "\n",
        "# '''\n",
        "# Adj_r2 = 1-(1-r2)*(n-1)/(n-p-1)\n",
        "\n",
        "# where, n = number of observations in training data, p = number of features\n",
        "# '''\n",
        "\n",
        "featimp = pd.Series(gd_sr.best_estimator_.feature_importances_, index=list(X)).sort_values(ascending=False) # Getting feature importances list for the best model\n",
        "print(featimp)\n",
        "\n",
        "# Selecting features with higher sifnificance and redefining feature set\n",
        "X_ = dataset[['Rating', 'Balance', 'Income']]\n",
        "\n",
        "feature_scaler = StandardScaler()\n",
        "X_scaled_ = feature_scaler.fit_transform(X_)\n",
        "\n",
        "# Tuning the random forest parameter 'n_estimators' and implementing cross-validation using Grid Search\n",
        "rfr = RandomForestRegressor(criterion='squared_error', max_features='sqrt', random_state=1)\n",
        "grid_param = {'n_estimators': [50,100,150,200,250]}\n",
        "\n",
        "gd_sr = GridSearchCV(estimator=rfr, param_grid=grid_param, scoring='r2', cv=5)\n",
        "\n",
        "gd_sr.fit(X_scaled_, Y)\n",
        "\n",
        "best_parameters = gd_sr.best_params_\n",
        "print(\"Best parameters: \", best_parameters)\n",
        "\n",
        "best_result = gd_sr.best_score_ # Mean cross-validated score of the best_estimator\n",
        "print(\"r2: \", best_result)\n",
        "\n",
        "Adj_r2 = 1-(1-best_result)*(320-1)/(320-11-1)\n",
        "print(\"Adjusted r2: \", Adj_r2)"
      ],
      "metadata": {
        "id": "4ZalCDQKwraw"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "import numpy as np\n",
        "import pandas as pd\n",
        "from sklearn.preprocessing import StandardScaler\n",
        "from sklearn.model_selection import GridSearchCV\n",
        "from sklearn.ensemble import RandomForestRegressor\n",
        "from sklearn.linear_model import SGDRegressor\n",
        "from sklearn.svm import SVR\n",
        "import plotly.graph_objs as go\n",
        "import plotly.figure_factory as ff\n",
        "\n",
        "# Importing dataset and examining it\n",
        "dataset = pd.read_csv(\"/content/CompletionRates.csv\")\n",
        "pd.set_option('display.max_columns', None) # to make sure you can see all the columns in output window\n",
        "print(dataset.head())\n",
        "print(dataset.shape)\n",
        "print(dataset.info())\n",
        "print(dataset.describe())\n",
        "\n",
        "# # Converting Categorical features into Numerical features\n",
        "# dataset['CentralAir'] = dataset['CentralAir'].map({'Y': 1, 'N':0})\n",
        "# dataset['PavedDrive'] = dataset['PavedDrive'].map({'Y': 1, 'N':0})\n",
        "# print(dataset.info())\n",
        "\n",
        "categorical_features = ['INST_TYPE']\n",
        "final_data = pd.get_dummies(dataset, columns = categorical_features, drop_first= True)\n",
        "print(final_data.info())\n",
        "print(final_data.head(2))\n",
        "\n",
        "# Plotting Correlation Heatmap\n",
        "corrs = dataset.corr()\n",
        "figure = ff.create_annotated_heatmap(\n",
        "    z=corrs.values,\n",
        "    x=list(corrs.columns),\n",
        "    y=list(corrs.index),\n",
        "    annotation_text=corrs.round(2).values,\n",
        "    showscale=True)\n",
        "figure.show()\n",
        "\n",
        "# Dividing dataset into label and feature sets\n",
        "X = dataset.drop(['AVG_FAC_SAL_PM','TS_MEN','TS_MAR','ST_FI_LO','ST_FI_M1','ST_FI_M2','ST_FI_H1','ST_FI_H2','HECR', 'HL_ED_P_PS'], axis = 1) # Features\n",
        "Y = dataset['HECR'] # Labels\n",
        "print(type(X))\n",
        "print(type(Y))\n",
        "print(X.shape)\n",
        "print(Y.shape)\n",
        "\n",
        "# # Plotting Correlation Heatmap\n",
        "# corrs = X.corr()\n",
        "# figure = ff.create_annotated_heatmap(\n",
        "#     z=corrs.values,\n",
        "#     x=list(corrs.columns),\n",
        "#     y=list(corrs.index),\n",
        "#     annotation_text=corrs.round(2).values,\n",
        "#     showscale=True)\n",
        "# figure.show()\n",
        "\n",
        "# Normalizing numerical features so that each feature has mean 0 and variance 1\n",
        "feature_scaler = StandardScaler()\n",
        "X_scaled = feature_scaler.fit_transform(X)\n",
        "\n",
        "# Linear Regression with Regularization\n",
        "# Tuning the SGDRegressor parameters 'eta0' (learning rate) and 'max_iter', along with the regularization parameter alpha using Grid Search\n",
        "sgdr = SGDRegressor(random_state = 1, penalty = 'elasticnet')\n",
        "grid_param = {'eta0': [.0001, .001, .01, .1, 1], 'max_iter':[10000, 20000, 30000, 40000],'alpha': [.001, .01, .1, 1,10, 100], 'l1_ratio': [0,0.25,0.5,0.75,1]}\n",
        "\n",
        "gd_sr = GridSearchCV(estimator=sgdr, param_grid=grid_param, scoring='r2', cv=5)\n",
        "\n",
        "gd_sr.fit(X_scaled, Y)\n",
        "\n",
        "best_parameters = gd_sr.best_params_\n",
        "print(\"Best parameters: \", best_parameters)\n",
        "\n",
        "best_result = gd_sr.best_score_ # Mean cross-validated score of the best_estimator\n",
        "print(\"r2: \", best_result)\n",
        "\n",
        "Adj_r2 = 1-(1-best_result)*(11440-1)/(11440-11-1)\n",
        "print(\"Adjusted r2: \", Adj_r2)\n",
        "\n",
        "'''\n",
        "Adj_r2 = 1-(1-r2)*(n-1)/(n-p-1)\n",
        "\n",
        "where, n = number of observations in training data, p = number of features\n",
        "'''\n",
        "\n",
        "best_model = gd_sr.best_estimator_\n",
        "print(\"Intercept: \", best_model.intercept_)\n",
        "\n",
        "print(pd.DataFrame(zip(X.columns, best_model.coef_), columns=['Features','Coefficients']).sort_values(by=['Coefficients'],ascending=False))\n",
        "\n",
        "##################################################################################\n",
        "# Implementing Random Forest Regression\n",
        "# Tuning the random forest parameter 'n_estimators' and implementing cross-validation using Grid Search\n",
        "rfr = RandomForestRegressor(criterion='squared_error', max_features='sqrt', random_state=1)\n",
        "grid_param = {'n_estimators': [10,20,30,40,50,100]}\n",
        "\n",
        "gd_sr = GridSearchCV(estimator=rfr, param_grid=grid_param, scoring='r2', cv=5)\n",
        "\n",
        "gd_sr.fit(X_scaled, Y)\n",
        "\n",
        "best_parameters = gd_sr.best_params_\n",
        "print(\"Best parameters: \", best_parameters)\n",
        "\n",
        "best_result = gd_sr.best_score_ # Mean cross-validated score of the best_estimator\n",
        "print(\"r2: \", best_result)\n",
        "\n",
        "Adj_r2 = 1-(1-best_result)*(11440-1)/(11440-11-1)\n",
        "print(\"Adjusted r2: \", Adj_r2)\n",
        "\n",
        "'''\n",
        "Adj_r2 = 1-(1-r2)*(n-1)/(n-p-1)\n",
        "\n",
        "where, n = number of observations in training data, p = number of features\n",
        "'''\n",
        "\n",
        "featimp = pd.Series(gd_sr.best_estimator_.feature_importances_, index=list(X)).sort_values(ascending=False) # Getting feature importances list for the best model\n",
        "print(featimp)\n",
        "\n",
        "# Selecting features with higher sifnificance and redefining feature set\n",
        "X_ = dataset[['HL_ED_P_HS', 'PER_PT', 'INST_EXP_PS', 'TS', 'S_DPEN']]\n",
        "\n",
        "feature_scaler = StandardScaler()\n",
        "X_scaled_ = feature_scaler.fit_transform(X_)\n",
        "\n",
        "# Tuning the random forest parameter 'n_estimators' and implementing cross-validation using Grid Search\n",
        "rfr = RandomForestRegressor(criterion='squared_error', max_features='sqrt', random_state=1)\n",
        "grid_param = {'n_estimators': [10,20,30,50,100]}\n",
        "\n",
        "gd_sr = GridSearchCV(estimator=rfr, param_grid=grid_param, scoring='r2', cv=5)\n",
        "\n",
        "gd_sr.fit(X_scaled_, Y)\n",
        "\n",
        "best_parameters = gd_sr.best_params_\n",
        "print(\"Best parameters: \", best_parameters)\n",
        "\n",
        "best_result = gd_sr.best_score_ # Mean cross-validated score of the best_estimator\n",
        "print(\"r2: \", best_result)\n",
        "\n",
        "Adj_r2 = 1-(1-best_result)*(11440-1)/(11440-11-1)\n",
        "print(\"Adjusted r2: \", Adj_r2)\n",
        "\n",
        "'''\n",
        "Adj_r2 = 1-(1-r2)*(n-1)/(n-p-1)\n",
        "\n",
        "where, n = number of observations in training data, p = number of features\n",
        "'''\n",
        "####################################################################################\n",
        "# Implementing Support Vector Regression\n",
        "# Tuning the SVR parameters 'kernel', 'C', 'epsilon' and implementing cross-validation using Grid Search\n",
        "svr = SVR()\n",
        "grid_param = {'kernel': ['linear', 'poly', 'rbf', 'sigmoid'], 'C': [.001,.01, 0.1, 1, 10,100]}\n",
        "\n",
        "gd_sr = GridSearchCV(estimator=svr, param_grid=grid_param, scoring='r2', cv=5)\n",
        "\n",
        "gd_sr.fit(X_scaled, Y)\n",
        "\n",
        "best_parameters = gd_sr.best_params_\n",
        "print(\"Best parameters: \", best_parameters)\n",
        "\n",
        "best_result = gd_sr.best_score_ # Mean cross-validated score of the best_estimator\n",
        "print(\"r2: \", best_result)\n",
        "\n",
        "Adj_r2 = 1-(1-best_result)*(11440-1)/(11440-11-1)\n",
        "print(\"Adjusted r2: \", Adj_r2)"
      ],
      "metadata": {
        "id": "T5aARhX8k1W8"
      },
      "execution_count": null,
      "outputs": []
    }
  ],
  "metadata": {
    "colab": {
      "provenance": [],
      "mount_file_id": "1eRjHfxNFAnIu4Z-ujGu9GavVicNuHtZ9",
      "authorship_tag": "ABX9TyNhlnTf6ex56M+XEVGpxcKY",
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}