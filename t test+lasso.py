#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sklearn
from sklearn.utils import shuffle
from sklearn.linear_model import Lasso,LassoCV,LassoLarsCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,roc_auc_score,roc_curve,mean_squared_error,r2_score
from sklearn.model_selection import RepeatedKFold, train_test_split,LeaveOneOut,GridSearchCV,permutation_test_score,cross_val_score
from sklearn import svm
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from scipy.stats import pearsonr, ttest_ind, levene
import itertools
import time


# In[2]:


xlsx1_filePath = "C:\\Users\\45351\\Desktop\\ISCIENCE\\data_A.xlsx"
xlsx2_filePath = "C:\\Users\\45351\\Desktop\\ISCIENCE\\data_B.xlsx"
data_1 = pd.read_excel(xlsx1_filePath)
data_2 = pd.read_excel(xlsx2_filePath)
rows_1,__ = data_1.shape
rows_2,__ = data_2.shape
data_1.insert(0,'label',[0]*rows_1)
data_2.insert(0,'label',[1]*rows_2)
data = pd.concat([data_1,data_2])
#data = shuffle(data)
data = data.fillna(0)
X = data[data.columns[1:]]
y = data['label']
colNames = X.columns
X = X.astype(np.float64)
X = StandardScaler().fit_transform(X)
X = pd.DataFrame(X)
X.columns = colNames


# In[3]:


# T test
index = []
for colName in data.columns[1:]:
    if levene(data_1[colName],data_2[colName])[1] > 0.05:
        if ttest_ind(data_1[colName],data_2[colName])[1] < 0.05:
            index.append(colName)
    else:
        if ttest_ind(data_1[colName],data_2[colName],equal_var = False)[1] < 0.05:
            index.append(colName)
print(len(colName))


# In[4]:


if 'label' not in index:index = ['label']+index
data_1 = data_1[index]
data_2 = data_2[index]
data = pd.concat([data_1,data_2])
#data = shuffle(data)
data.index = range(len(data))#re-label after mixed
X = data[data.columns[1:]]
y = data['label']
X = X.apply(pd.to_numeric,errors = 'ignore') # transform the type of the data
colNames = X.columns # to read the name the feature
X = X.fillna(0) # replace 'nan' to '0'
X = X.astype(np.float64)
X = StandardScaler().fit_transform(X)
X = pd.DataFrame(X)
X.columns = colNames
sampleCounts = colNames
X_raw = X


# In[5]:


alphas = np.logspace(-3,1,50)
model_lassoCV = LassoCV(alphas = alphas, cv = 10, max_iter = 100000).fit(X,y)
# model_lassoCV.predict(X)


# In[6]:


print(model_lassoCV.alpha_)
coef = pd.Series(model_lassoCV.coef_,index = X.columns)
print(coef)
print("pick" + str(sum(coef !=0)) + "out" + str(sum(coef==0)))


# In[7]:


index = coef[coef != 0].index
X = X[index]
X.head()
print(coef[coef !=0])


# In[8]:


import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

MSEs = model_lassoCV.mse_path_
'''
MSEs_mean, MSE_std = [],[]
for i in range(len(MESs)):
    MSEs_mean.append(MSEs[i].mean())
    MSEs_std.append(MSEs[i].std())
'''

MSEs_mean = np.apply_along_axis(np.mean,1,MSEs)
MSEs_std = np.apply_along_axis(np.std,1,MSEs)

plt.figure(dpi = 600)  
plt.errorbar(model_lassoCV.alphas_,MSEs_mean
            ,yerr = MSEs_std
            ,fmt = 'o' 
            ,ms = 3 # dot size
            ,mfc = 'r' # dot color
            ,mec = 'r' # dot margin color
            ,ecolor = 'lightblue' 
            ,elinewidth = 2 # error bar width
            ,capsize = 4  # cap length of error bar 
            ,capthick = 1) 
plt.semilogx()
plt.axvline(model_lassoCV.alpha_,color = 'black',ls = '--')
plt.xlabel('Lamda')
plt.ylabel('MSE')
ax = plt.gca()
y_major_locator = ticker.MultipleLocator(0.05)
ax.yaxis.set_major_locator(y_major_locator)
plt.show()


# In[9]:


coefs = model_lassoCV.path(X_raw,y,alphas = alphas, cv = 10, max_iter = 100000)[1].T
plt.figure(dpi = 600)
plt.semilogx(model_lassoCV.alphas_,coefs,'-')
plt.axvline(model_lassoCV.alpha_,color = 'black',ls = '--')
plt.xlabel('Lamda')
plt.ylabel('Coefficient')
plt.show()


# In[10]:


not_zero = []
for coef in model_lassoCV.coef_:
    if coef !=0:
        not_zero.append(coef)
 
len(not_zero)
 
not_zero


# In[11]:


# X_train.columns[regr_cv.coef_ != 0].tolist()
X_raw.columns[model_lassoCV.coef_ != 0].tolist()


# In[13]:


# not_zero
# X_train.columns[regr_cv.coef_ != 0].tolist()
coef_table = {'features':X_raw.columns[model_lassoCV.coef_ != 0].tolist(),'coefficient':not_zero}
coef_table
 
coef_pd = pd.DataFrame.from_dict(coef_table)
coef_pd










