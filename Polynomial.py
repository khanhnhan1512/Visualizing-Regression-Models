import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class PolynomialRegression:
    def __init__(self, data_points):
        self.data_points = data_points
        
    def preprocessing(self):
        self.X = np.array([point[0] for point in self.data_points]).reshape(-1, 1)
        self.y = np.array([point[1] for point in self.data_points]).reshape(-1, 1)
    
    def train_model(self):
        self.preprocessing()
        self.poly = PolynomialFeatures(degree = 4)
        self.model = LinearRegression()
        self.X_poly = self.poly.fit_transform(self.X)
        self.model.fit(self.X_poly, self.y)
        
    def predict(self):
        min_x = min(self.X)[0] - 20
        max_x = max(self.X)[0] + 20
        points = [(x, round(self.model.predict(self.poly.transform([[x]]))[0][0])) for x in range(min_x, max_x)]
        return points
    
    def mae(self):
        self.y_pred = self.model.predict(self.X_poly)
        return round(mean_squared_error(self.y, self.y_pred), 2)