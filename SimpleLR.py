import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

class SimpleLR:
    def __init__(self, data_points):
        self.data_points = data_points
    
    def preprocessing(self):
        self.X = np.array([point[0] for point in self.data_points]).reshape(-1, 1)
        self.y = np.array([point[1] for point in self.data_points]).reshape(-1, 1)
    
    def train_model(self):
        self.preprocessing()
        self.model = LinearRegression()
        self.model.fit(self.X, self.y)
        
    def predict(self):
        first_point = (min(self.X)[0], round(self.model.predict([min(self.X)])[0][0]))
        second_point = (max(self.X)[0], round(self.model.predict([max(self.X)])[0][0]))
        points = [first_point, second_point]
        return points
    
    def mae(self):
        self.y_pred = self.model.predict(self.X)
        return round(mean_absolute_error(self.y, self.y_pred), 2)
    