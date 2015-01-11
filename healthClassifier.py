from sklearn.linear_model import LinearRegression
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.cross_validation import KFold
from sklearn.metrics import mean_absolute_error
import pandas as pd
import numpy as np

#--------- Concatenation of everything we have
health = pd.io.pickle.read_pickle("oven.500.health")
nothealth = pd.io.pickle.read_pickle("oven.500.nothealth")

health["Health"] = 1
nothealth["Health"] = 0
data = pd.concat([health, nothealth])

#--------- Get col names
cols = set(data.columns.values)
cols =  np.array( list(cols - set(['Name', 'Rating', 'Health'])) )

#--------- Remove empty rows and duplicates
data.drop_duplicates(cols)

#--------- Get col names
X = data[sorted(cols)].astype(float).values
y = data["Health"].astype(int).values

#print cols[x[-2].astype(bool)]

kf = KFold(n=X.shape[0], n_folds=5, shuffle=True, random_state=42)
for train_index, test_index in kf:
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    #model = LinearRegression()
    #model = ExtraTreesRegressor(n_estimators=50)
    #model.fit(X_train,y_train)
    #predicted = model.predict(X_test)
    #print mean_absolute_error(y_test, predicted)


# Test Model:
model = LinearRegression()
#model = ExtraTreesRegressor(n_estimators=50)
model.fit(X,y)

import cPickle
with open("hclf.pickle", "wb") as f:
    cPickle.dump(model,f)

#model.predict(x[0])




