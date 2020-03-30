import falcon

from prediction_microservice.resources.predictor_resource import PredictorResource
from prediction_microservice.models.predictor import PredictorArima
from prediction_microservice.models.predictor_dator import PredictorMongoDator

api = application = falcon.API()

dator = PredictorMongoDator() # host y puerto correctos

# Crear Predictores Arima
predictor_arima_hum = dator.get_by_data_name("data_model_1", "hum", "arima")
predictor_arima_temp = dator.get_by_data_name("data_model_1", "temp", "arima")
# Si no hay modelos crearlos y guardarlos usando el dator
if not predictor_arima_hum.is_model_set():
    print("Creating arima predictor model for humidity...")
    predictor_arima_hum.create_model_from_data()
    dator.save_predictor_model(predictor_arima_hum)
    print("Predictor arima model for humidity created and saved")
if not predictor_arima_temp.is_model_set():
    print("Creating arima predictor model for temperature...")
    predictor_arima_temp.create_model_from_data()
    dator.save_predictor_model(predictor_arima_temp)
    print("Predictor arima model for temperature created and saved")
# Si hay, ya deberian estar cargados por el dator en los predictores

# Crear Predictores Prophet
predictor_prophet_hum = dator.get_by_data_name("data_model_1", "hum", "prophet")
predictor_prophet_temp = dator.get_by_data_name("data_model_1", "temp", "prophet")
# Si no hay modelos crearlos y guardarlos usando el dator
if not predictor_prophet_hum.is_model_set():
    print("Creating prophet predictor model for humidity...")
    predictor_prophet_hum.create_model_from_data()
    dator.save_predictor_model(predictor_prophet_hum)
    print("Predictor prophet model for humidity created and saved")
if not predictor_prophet_temp.is_model_set():
    print("Creating prophet predictor model for temperature...")
    predictor_prophet_temp.create_model_from_data()
    dator.save_predictor_model(predictor_prophet_temp)
    print("Predictor prophet model for temperature created and saved")
# Si hay, ya deberian estar cargados por el dator en los predictores

## Para que funcione se le deberan adosar volumenes con los modelos al contenedor a la hora de levantarlo

api.add_route('/servicio/v1/prediccion/{period}', PredictorResource(predictor_arima_hum, predictor_arima_temp))
api.add_route('/servicio/v2/prediccion/{period}', PredictorResource(predictor_prophet_hum, predictor_prophet_temp))

## gunicorn -w 1 -b 0.0.0.0:8080 -t 6000 prediction_microservice.app

# docker run --rm -it -p 27017:27017 --env MONGO_INITDB_DATABASE=practica2 mongo_p2
# docker build -t mongo_p2 --build-arg MONGO_INITDB_DATABASE=practica2 .

# docker build -t prediction_p2 .

