# CCP2-Prediction_Microservice
Time series forecasting python microservice for the Could Computing 2 course at UGR. It is part of the second practical assignment.

The framework used for creating the service has been [Falcon](https://falconframework.org/). We have also used [gunicorn](https://gunicorn.org/) as server.

The requirements stablished creating 2 versions of the API so each one cloud use a different predictor. The libraries used for creating the predictors had been [pmdarima](http://alkaline-ml.com/pmdarima/) and [fbprophet](https://facebook.github.io/prophet/docs/quick_start.html).

In the 'trained_models' folder there are ready-to-use models for the predictor, however, is those are not present, the service creates the models before starting and saves their names and routes to a database for later use. It is needed to uncompressed the models before using the service.

The service is supposed to connect to a mongobd docker instance to get the data it needs. The host and port of the mongodb container to connect must be set as enviromental variables when running the container (MONGO_HOST, MONGO_PORT) or in a docker-compose file.

Test for the microservice can be run using [pytest](https://docs.pytest.org/en/latest/).


