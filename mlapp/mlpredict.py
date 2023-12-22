from django.shortcuts import render
from .models import BreastCancerData, Student_Performance_Data
import joblib
import os
from django.conf import settings
from sklearn.model_selection import KFold, cross_val_score
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from django.http import JsonResponse
import pandas as pd 
from django.contrib.auth.decorators import login_required



filename = os.path.join(settings.STATIC_ROOT, 'static/files/SVM_model_classification.pkl')
# filename = 'C:/xampp/htdocs/Django/Bigdata/mlproject/mlapp/static/files/random_forest_model.pkl'
loaded_model_v2 = joblib.load(filename)
print(f"File path: {filename}")

dictsdia = {0: "Benign", 1: "Malignant"}

@login_required 

# Create your views here.
def predictBC(request):

    if request.method == 'POST':
        # get the value from the user
        clumpthicknesstxt = request.POST.get('clumpthickness', 'default')
        cellsizetxt = request.POST.get('cellsize', 'default')
        cellshapetxt = request.POST.get('cellshape', 'default')
        marginaltxt = request.POST.get('marginal', 'default')
        singlesizetxt = request.POST.get('singlesize', 'default')
        barenucleitxt = request.POST.get('barenuclei', 'default')
        blandchromatintxt = request.POST.get('blandchromatin', 'default')
        nucleolitxt = request.POST.get('nucleoli', 'default')
        mitosestxt = request.POST.get('mitoses', 'default')

        ct = int(clumpthicknesstxt)
        csize = int(cellsizetxt)
        cshape = int(cellshapetxt)
        margin = int(marginaltxt)
        ssize = int(singlesizetxt)
        bn = int(barenucleitxt)
        bc = int(blandchromatintxt)
        nuc = int(nucleolitxt)
        mitos = int(mitosestxt)

        sampletest = [[ct, csize, cshape, margin, ssize, bn, bc, nuc, mitos]]
        predict = loaded_model_v2.predict(sampletest)
        predicted = dictsdia[predict[0]]
        params = {'Prediction': predicted}

        # Extract the numeric value from the parentheses
        Result = int(predict[0])
        # Save the input values and prediction to the database
        prediction_instance = BreastCancerData(
            clumpthickness=ct, cellsize=csize, cellshape=cshape, marginal=margin, singlesize=ssize, 
            barenuclei=bn, blandchromatin=bc, nucleoli=nuc, mitoses =mitos,
            prediction=Result
        )

        prediction_instance.save()

        return render(request, 'prediction/class_BC.html', params)

    return render(request, 'prediction/class_BC.html')

def ClassifyTrainModel(request):
    
    if request.method == 'POST':
        # Load data from MySQL database
      queryset = BreastCancerData.objects.values('clumpthickness', 'cellsize', 'cellshape', 'marginal',
                                                  'singlesize', 'barenuclei', 'blandchromatin', 'nucleoli', 'mitoses', 'prediction')
      dataframe = pd.DataFrame.from_records(queryset)
      array = dataframe.values
      X = array[:, 0:9]  # Adjust 'n' based on the number of features
      Y = array[:, 9]   # Adjust 'n' based on the target column index

      # Set k or the number of folds
      num_folds = 5

      kfold = KFold(n_splits=num_folds, shuffle=False, random_state=None)

      model = SVC(kernel='linear', C=1.0)

    # Fit the model on the entire dataset
      model.fit(X, Y)
    
    # Evaluate the score of a kfold cross validation splitting strategy
      results = cross_val_score(model, X, Y, cv=kfold)
      Results = (("%.3f%% (%.3f%%)") % (results.mean()*100.0, results.std()*100.0))

      model_path = os.path.join(settings.STATIC_ROOT, 'static/files', 'svm_model.pkl')
      joblib.dump(model, model_path)

      return JsonResponse({'success': True, 'Accuracy': Results})  # Handle the case when it's a GET request
    return render(request, 'model/Model_BC.html')


# regression

regfilename = os.path.join(settings.STATIC_ROOT, 'static/files/LR_model_regression.pkl')
# filename = 'C:/xampp/htdocs/Django/Bigdata/mlproject/mlapp/static/files/random_forest_model.pkl'
lr_loaded_model = joblib.load(regfilename)

# Create your views here.
def predictSP(request):

    if request.method == 'POST':
        # get the value from the user
        hrs_study = int(request.POST.get('hrs_study', 'default')) 
        prev_score = int(request.POST.get('prev_score', 'default')) 
        extra_act = int(request.POST.get('extra_act', 'default')) 
        sleep_hrs = int(request.POST.get('sleep_hrs', 'default')) 
        question_papers = int(request.POST.get('question_papers', 'default')) 
   


        sampletest = [[hrs_study, prev_score, extra_act, sleep_hrs, question_papers]]
        predict = lr_loaded_model.predict(sampletest)

        Result = int(predict)
        params = {'Prediction': Result}

       
        # Save the input values and prediction to the database
        prediction_instance = Student_Performance_Data(
            hrs_study=hrs_study, prev_score=prev_score, extra_act=extra_act, sleep_hrs=sleep_hrs, 
           question_papers =question_papers, Performance=Result
        )

        prediction_instance.save()

        return render(request, 'prediction/reg_studentperformance.html', params)

    return render(request, 'prediction/reg_studentperformance.html')


def RegressionTrainModel(request):
    if request.method == 'POST':
        queryset = Student_Performance_Data.objects.values('hrs_study', 'prev_score', 'extra_act', 'sleep_hrs',
                                                    'question_papers', 'Performance')
        dataframe = pd.DataFrame.from_records(queryset)
        array = dataframe.values
        X = array[:, 0:5]  
        Y = array[:, 5]   

        num_folds = 10

        kfold = KFold(n_splits=num_folds, random_state=None)

        model = LinearRegression()

        # Fit the model on the entire dataset
        model.fit(X, Y)
        
        scoring = 'neg_mean_absolute_error'

        results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
        Accuracy = ("(MAE): %.3f (%.3f)" % (-results.mean(), results.std()))

        model_path = os.path.join(settings.STATIC_ROOT, 'static/files', 'lr_model.pkl')
        joblib.dump(model, model_path)

        return JsonResponse({'success': True, 'Accuracy': Accuracy})
    return render(request, 'model/Model_SP.html')
