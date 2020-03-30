import os
import pymongo
import pickle
from datetime import datetime

from prediction_microservice.utils.singleton import Singleton
from prediction_microservice.models.predictor import PredictorArima, PredictorProphet
from bson.objectid import ObjectId


class PredictorMongoDator(metaclass=Singleton):
    def __init__(self, host=os.environ['MONGO_HOST'], port=os.environ['MONGO_PORT']):
        print("Connecting to database...")
        self.__model_data = None

        try:
            client = pymongo.MongoClient(host, port, serverSelectionTimeoutMS=5000)
            client.server_info()
        except:
            print("Connection error to the Mongo database.")
        else:
            print("Connection established.")

        db = client.practica2
        self.__model_data = db.model_data

    def get_by_data_id(self, id, pred_type, pred_class):
        if not isinstance(id, str):
            raise AttributeError("Parameter id must be of type str")

        data = self.__model_data.find_one({"_id": ObjectId(id)})
        if data is None:
            raise ValueError("Could not find specified id.")
        else:
            # Cargar el modelo
            filename = data.get(pred_class + "_" + pred_type + "_model_filename")
            if filename != "":
                with open('prediction_microservice/trained_models/' + filename, 'rb') as pkl:
                    model = pickle.load(pkl)
                print("Loading " + pred_type + " model for predictor " + pred_class)
                
                if pred_class == "arima":
                    return PredictorArima(pred_type, data, model)
                elif pred_class == "prophet":
                    return PredictorProphet(pred_type, data, model)
            else:
                if pred_class == "arima":
                    return PredictorArima(pred_type, data)
                elif pred_class == "prophet":
                    return PredictorProphet(pred_type, data)

    def get_by_data_name(self, data_name, pred_type, pred_class):
        if not isinstance(data_name, str):
            raise AttributeError("Parameter data_name must be of type str")

        data = self.__model_data.find_one({"data_name": data_name})
        if data is None:
            raise ValueError("Could not find specified data_name.")
        else:
            # Cargar el modelo
            filename = data.get(pred_class + "_" + pred_type + "_model_filename")
            if filename != "":
                with open('prediction_microservice/trained_models/' + filename, 'rb') as pkl:
                    model = pickle.load(pkl)
                print("Loading " + pred_type + " model for predictor " + pred_class)

                if pred_class == "arima":
                    return PredictorArima(pred_type, data, model)
                elif pred_class == "prophet":
                    return PredictorProphet(pred_type, data, model)
            else:
                if pred_class == "arima":
                    return PredictorArima(pred_type, data)
                elif pred_class == "prophet":
                    return PredictorProphet(pred_type, data)

    def save_predictor_model(self, predictor):
        # Crear fichero para guardar modelo
        filename = predictor.return_predictor_class() + '-' + predictor.return_predictor_type() + '-' + datetime.now().strftime("%m:%d:%Y-%H:%M:%S") + '.pkl'
        f = open('prediction_microservice/trained_models/' + filename,"x")
        f.close()

        # Guardar modelo
        m = predictor.return_model()
        m.stan_backend.logger = None
        with open('prediction_microservice/trained_models/' + filename, 'wb') as pkl:
            pickle.dump(m, pkl)

        #Actualizar base de datos
        query = {"_id": predictor.return_data().get("_id")}
        update = { "$set": { predictor.return_predictor_class() + "_" + predictor.return_predictor_type() + "_model_filename": filename }}
        self.__model_data.update_one(query, update)

        print("Saved " + filename + " model.")
