# Load libraries
import flask
import pandas as pd
import numpy as np
import json
#import tensorflow as tf
#import keras
#from keras.models import load_model

# instantiate flask 
app = flask.Flask(__name__)

# we need to redefine our metric function in order 
# to use it when loading the model 
#def auc(y_true, y_pred):
#    auc = tf.metrics.auc(y_true, y_pred)[1]
#   keras.backend.get_session().run(tf.local_variables_initializer())
#    return auc

# load the model, and pass in the custom metric function
#global graph
#graph = tf.get_default_graph()
#model = load_model('model.h5', custom_objects={})
#x = 0.0
# define a predict function as an endpoint 
#@app.route("/give", methods=["GET"])
#def give():
#    g = {}
#    g["prediction"]=x
#    print("got here")
#    return flask.jsonify(g)
    
@app.route("/predict", methods=["GET","POST"])
def predict():
    #global x
    data = {"success": False}

    params = flask.request.json
    if (params == None):
        params = flask.request.args

    # if parameters are found, return a prediction
    if (params != None):
#        print(params)
#        x=pd.DataFrame.from_dict(params, orient='index')
#        print(x)
#        x=np.array(x).transpose()
#        x = np.array(flask.request.args.get('a'),flask.request.args.get('b'),flask.request.args.get('c'),flask.request.args.get('d'))
        x= flask.request.args.get('x')
        print(x)
        with open(str(x)+'d.json') as json_file:
            data = json.load(json_file)
            return flask.jsonify(data)
        #data["prediction"]=x
        #b = flask.request.args.get('b')
        #c = flask.request.args.get('c')
        #d = flask.request.args.get('d')
        #y=np.array([[a,b,c,d]])
        #x.reshape(1,4)
        #print(y)
        #with graph.as_default():
        #    data["prediction"] = str(model.predict(y)[0][0])
        #    x = data["prediction"]
        #    print(x)
        #    data["success"] = True

    # return a response in json format 
    #return flask.jsonify(data)    

# start the flask app, allow remote connections 
app.run(host='0.0.0.0')
