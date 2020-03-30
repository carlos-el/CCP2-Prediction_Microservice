import falcon
import json

class PredictorResource(object):
    def __init__(self, predictor_hum, predictor_temp):
        self._predictor_hum = predictor_hum
        self._predictor_temp = predictor_temp

    def on_get(self, req, resp, period):
        print("On GET")
        if period not in ['24', '48', '72']:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = json.dumps(
                {"error": "Only can return forecasting for 24, 48 and 72h"})
            return resp

        forecast_hum = self._predictor_hum.predict(int(period))
        forecast_temp = self._predictor_temp.predict(int(period))
        
        result = []
        for i in range(len(forecast_hum)):
            result.append({"hum": forecast_hum[i], "temp": forecast_temp[i]})

        resp.body = json.dumps({"forecast": result})
        return resp