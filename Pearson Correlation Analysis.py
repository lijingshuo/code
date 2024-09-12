#!/usr/bin/env python
# coding: utf-8

# In[1]:


# The code below is modified from 
# https://www.machinelearningplus.com/plots/top-50-matplotlib-visualizations-the-master-plots-python/

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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


# In[4]:


xlsx1_filePath = "C:\\Users\\45351\\Desktop\\file.xlsx"
df = pd.read_excel(xlsx1_filePath)
print(df.head(5))
print(df.corr().head(5))
# method 参数默认计算 pearson相关系数，其它还可以计算“spearman”,"kendall"相关系数


# In[5]:


# Heatmap plot
plt.figure(figsize = (12,10),dpi = 600)
sns.heatmap(df.corr(),xticklabels = df.corr().columns, yticklabels = df.corr().columns,
            cmap = "RdYlGn",center = 0, annot = True)

# Decoration
plt.title('Correlogram of mtcars',fontsize = 22)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.show()


# In[ ]:





# In[ ]:




