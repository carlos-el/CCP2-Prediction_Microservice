from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm
import pandas as pd
from io import StringIO
from fbprophet import Prophet


class PredictorArima:
    def __init__(self, predictor_type, data_for_model=None, model=None):
        self._model = None
        self._data = None
        self._predictor_type = None
        self.set_predictor_type(predictor_type)

        if data_for_model is not None:
            self.set_data(data_for_model)

        if model is not None:
            self.set_model(model)


    def set_predictor_type(self, predictor_type):
        if predictor_type not in ['hum', 'temp']:
            raise ValueError("Parameter predictor_type must 'hum' or 'temp'")

        self._predictor_type = predictor_type

    def set_model(self, model):
        self._model = model 

    def set_data(self, data):
        if not isinstance(data, dict):
            raise AttributeError("Parameter data must be of type dict")

        self._data = data 

    def is_model_set(self):
        if self._model is None:
            return False
        else:
            return True

    def is_data_set(self):
        if self._data is None:
            return False
        else:
            return True

    def create_model_from_data(self):
        if self._data is None:
            raise TypeError("Data is not set, can not create model.")

        try:
            text = StringIO(self._data.get("content"))
            df = pd.read_csv(text, header=0)
            df.set_index('date', inplace=True)
            df = df.dropna()

            if(self._predictor_type == "hum"):
                model_data = df.humidity
            else:
                model_data = df.temperature
            
            print("Creating model, this may take some time...")
            self._model = pm.auto_arima(model_data, start_p=1, start_q=1,
                        test='adf',       # use adftest to find optimal 'd'
                        max_p=3, max_q=3, # maximum p and q
                        m=1,              # frequency of series
                        d=None,           # let model determine 'd'
                        seasonal=False,   # No Seasonality
                        start_P=0, 
                        D=0, 
                        trace=True,
                        error_action='ignore',  
                        suppress_warnings=True, 
                        stepwise=True)
            print("Model created successfully.")
        except:
            raise AttributeError("Wrong data provided for the model")
        
    def return_model(self):
        if self._model is None:
            raise TypeError("Model is not set, can not return model.")

        return self._model

    def return_data(self):
        if self._data is None:
            raise TypeError("Data is not set, can not return model.")

        return self._data

    def return_predictor_type(self):
        return self._predictor_type

    def return_predictor_class(self):
        return "arima"

    def predict(self, n_periods):
        if self._model is None:
            raise TypeError("Model is not set, can not predict anything.")

        return self._model.predict(n_periods=n_periods, return_conf_int=False)



##########
class PredictorProphet(PredictorArima):
    def __init__(self, predictor_type, data_for_model=None, model=None):
        super(PredictorProphet, self).__init__(predictor_type, data_for_model, model)

    def return_predictor_class(self):
        return "prophet"

    def create_model_from_data(self):
        if self._data is None:
            raise TypeError("Data is not set, can not create model.")

        try:
            if(self._predictor_type == "hum"):
                sel = "humidity"
                neg = "temperature"
            else:
                sel = "temperature"
                neg = "humidity"

            text = StringIO(self._data.get("content"))
            df = pd.read_csv(text, header=0)
            df = df[["date", "temperature", "humidity"]]
            df.drop([neg], 1, inplace=True)
            df.rename(columns={"date": "ds", sel: "y"}, inplace=True)
            df = df.dropna()

            self._model = Prophet(interval_width=0.95)
            self._model.fit(df)
            print("Model created successfully.")
        except:
            raise AttributeError("Wrong data provided for the model")

    def predict(self, n_periods):
        if self._model is None:
            raise TypeError("Model is not set, can not predict anything.")

        forecast = self._model.make_future_dataframe(periods=n_periods, freq="H", include_history=False)
        forecast = self._model.predict(forecast)

        return forecast['yhat'].tolist()

    