from django.shortcuts import render
from .models import Diabetesdata
import joblib
import os
from django.conf import settings
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd 



filename = os.path.join(settings.STATIC_ROOT, 'static/files/random_forest_model.pkl')
# filename = 'C:/xampp/htdocs/Django/Bigdata/mlproject/mlapp/static/files/random_forest_model.pkl'
loaded_model_v2 = joblib.load(filename)
print(f"File path: {filename}")

dictsdia = {0: "without diabetes", 1: "with diabetes"}

# Create your views here.
def diabetestTest(request):

    # get the value from the user
    pregtext = request.GET.get('preg', 'default')
    gluctext = request.GET.get('gluc', 'default')
    bloodtext = request.GET.get('blood', 'default')
    skintext = request.GET.get('skin', 'default')
    instext = request.GET.get('ins', 'default')
    bmitext = request.GET.get('bmi', 'default')
    dbftext = request.GET.get('dbf', 'default')
    agetext = request.GET.get('age', 'default')
    
    preg = float(pregtext)
    gluc = float(gluctext)
    blood = float(bloodtext)
    skin = float(skintext)
    ins = float(instext)
    bmi = float(bmitext)
    dbf = float(dbftext)
    age = float(agetext)

    sampletest = [[preg, gluc, blood, skin, ins, bmi, dbf, age]]
    predict = loaded_model_v2.predict(sampletest)
    predicted = dictsdia[predict[0]]
    params = {'Category': predicted}

    # Extract the numeric value from the parentheses
    numeric_value = int(predict[0])
      # Save the input values and prediction to the database
    prediction_instance = Diabetesdata(
        preg=preg, gluc=gluc, blood=blood, skin=skin, ins=ins, bmi=bmi, dbf=dbf, age=age,
        prediction=numeric_value
    )

    prediction_instance.save()


    return render(request, 'sample.html', params)

def ClassifyTrainModel(request):
    
    if request.method == 'POST':
        # Load data from MySQL database
      queryset = Diabetesdata.objects.values('preg', 'gluc', 'blood', 'skin', 'ins', 'bmi', 'dbf', 'age', 'prediction')
      dataframe = pd.DataFrame.from_records(queryset)
      array = dataframe.values
      X = array[:, :8]  # Adjust 'n' based on the number of features
      Y = array[:, 8]   # Adjust 'n' based on the target column index

          # Set the test size and random seed for reproducibility
      test_size = 0.20
      random_seed = 50
      X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=random_seed)

          # Initialize and train the RandomForestClassifier
      rfmodel = RandomForestClassifier(n_estimators=100, random_state=random_seed, max_depth=None, min_samples_split=2, min_samples_leaf=1)
      rfmodel.fit(X_train, Y_train)

      result = rfmodel.score(X_test, Y_test)
      resulting = ("Accuracy: %.3f%%" % (result * 100.0))
          # Now, 'rfmodel' is trained on your MySQL data
      params = {'Category': resulting}


      model_path = os.path.join(settings.STATIC_ROOT, 'static/files', 'rf_model.pkl')
    
# Check if the button was clicked
      if 'save_model' in request.POST:
            # Check if the old file exists and remove it
        
            # Save the new model file
            joblib.dump(rfmodel, model_path)

            message = ('the model is now being use')
            text = {'message': message}

            return render(request, 'index.html', text)
      
      return render(request, 'index.html', params)
  # Handle the case when it's a GET request
    return render(request, 'index.html')