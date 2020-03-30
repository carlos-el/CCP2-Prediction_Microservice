import sys
import os
import pytest

sys.path.append(os.path.abspath('./'))

from prediction_microservice.models.predictor import PredictorArima

data = "dummy text"
model = "dummy model"

def test_set_predictor():
    with pytest.raises(ValueError):
        _ = PredictorArima(predictor_type='test', data_for_model=1)

def test_set_data():
    with pytest.raises(AttributeError):
        _ = PredictorArima(predictor_type='hum',data_for_model=1)
    
def test_is_model_set():
    p = PredictorArima(predictor_type='hum', data_for_model={"data":"test"}, model=model)
    assert p.is_model_set() == True, "Error in is_model_set"

    p2 = PredictorArima(predictor_type='hum',data_for_model={"data":"test"})
    assert p2.is_model_set() == False, "Error in is_model_set"
        
def test_is_data_set():
    p = PredictorArima(predictor_type='hum',data_for_model={"data":"test"}, model=model)
    assert p.is_data_set() == True, "Error in is_data_set"

    p2 = PredictorArima(predictor_type='hum')
    assert p2.is_data_set() == False, "Error in is_data_set"

def test_create_model_from_data():
    p = PredictorArima(predictor_type='hum')
    with pytest.raises(TypeError):
        p.create_model_from_data()

    p2 = PredictorArima(predictor_type='hum',data_for_model={"data":"test"})
    with pytest.raises(AttributeError):
        p2.create_model_from_data()

def test_return_model():
    p = PredictorArima(predictor_type='hum')
    with pytest.raises(TypeError):
        p.return_model()

def test_return_data():
    p = PredictorArima(predictor_type='hum')
    with pytest.raises(TypeError):
        p.return_data()

def predict():
    p = PredictorArima(predictor_type='hum',)
    with pytest.raises(TypeError):
        p.predict()