from sklearn.linear_model import LinearRegression
import numpy as np

def predict_expenses(monthly):

    X=np.array(range(len(monthly))).reshape(-1,1)

    y=monthly.values

    model=LinearRegression()

    model.fit(X,y)

    next_val=model.predict([[len(monthly)]])

    return next_val[0]