from flask import Flask,render_template,url_for,request
import pandas as pd
import pickle


# load model
loaded_model=pickle.load(open("random_forest.pkl","rb"))

app=Flask(__name__)



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict",methods=["POST"])
def predict():
    df=pd.read_csv("/Users/mufseeramusthafa/Documents/machine_learning/airquality_index_predicton/Data/Real-Data/real_2013.csv")
    prediction=loaded_model.predict(df.iloc[:,:-1].values)
    prediction=prediction.tolist()
    return render_template("result.html",prediction=prediction)



if __name__=="__main__":
    app.run(debug=True)