# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 18:44:35 2020

@author: seanj
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score
#import statsmodels.api as sm


from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error


df = pd.read_csv('C:/Users/seanj/Documents/GitHub/ds_salary_proj/eda_data.csv')
print(df.columns)

# Choose relevant columns
#df_model = df[['avg_salary', 'Rating', 'Size','Type of ownership', 'Industry', 'Sector', 'Revenue', 'num_comp',
#       'hourly', 'employer_provided', 'min_salary', 'max_salary',
#       'company_txt', 'job_state', 'same_state', 'age',
#       'python_yn', 'R_yn', 'spark', 'aws', 'excel', 'tableau', 'jmp',
#       'power_bi']]

df_model = df[['avg_salary', 'Rating', 'Size','Type of ownership', 'Industry', 'Sector', 'Revenue', 'num_comp',
       'hourly', 'employer_provided', 'min_salary', 'max_salary',
       'company_txt', 'job_state', 'same_state', 'age',
       'python_yn', 'R_yn', 'spark', 'aws', 'excel']]


# Get dummy data
df_dum = pd.get_dummies(df_model)

# Train test split
X = df_dum.drop('avg_salary', axis=1)
y = df_dum.avg_salary.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Multiple linear regression

# X_sm = sm.add_constant(X)
# model = sm.OLS(y,X_sm)

# f = open("Coefficients for Regression.txt", "a")
# f.write(str(model.fit().summary()))
# f.close()

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

lm = LinearRegression()
lm.fit(X_train, y_train)

y_pred = lm.predict(X_test)
print(r2_score(y_test, y_pred))

print(np.mean(cross_val_score(lm,X_train,y_train, scoring='neg_mean_squared_error', cv=3)))


print('Lasso Regression')

# Lasso Regression

lm_l = Lasso()
lm_l.fit(X_train, y_train)

y_pred = lm_l.predict(X_test)
print(r2_score(y_test, y_pred))

print(np.mean(cross_val_score(lm_l,X_train,y_train, scoring='neg_mean_squared_error', cv=3)))

alpha = []
error = []

# for i in range(1,100):
#     alpha.append(i/100)
#     lml = Lasso(alpha=(i/100))
#     error.append(np.mean(cross_val_score(lml,X_train,y_train, scoring='r2', cv=3)))

# plt.plot(alpha, error)
# plt.show()

# err = tuple(zip(alpha, error))
# #print(error)

# df_err = pd.DataFrame(err, columns=['alpha', 'error'])
# print(df_err[df_err.error == max(df_err.error)])


# Random Forest
from sklearn.ensemble import RandomForestRegressor
print('Random forest')
rf = RandomForestRegressor()

rf.fit(X_train, y_train)
y_pred = lm.predict(X_test)

print(np.mean(cross_val_score(rf,X_train,y_train, scoring='neg_mean_squared_error', cv=3)))

# Tune models GridsxearchCV

from sklearn.model_selection import GridSearchCV

parameters = {'n_estimators'}


# Test ensable

