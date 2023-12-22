from django.shortcuts import render, redirect
from .models import BreastCancerData, Student_Performance_Data
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Avg 

# Create your views here.
def index(request):
     return render(request, 'index.html', {})

@login_required 

def dashboarBC(request):
     if request.user.is_authenticated:
        # User is authenticated, you can access user information
        username = request.user.username
        # Perform actions for authenticated users
        breast_cancer_data_count = BreastCancerData.objects.count()
        count_prediction_0 = BreastCancerData.objects.filter(prediction=0).count()
        count_prediction_1 = BreastCancerData.objects.filter(prediction=1).count()
        # Assuming 'clumpthickness' is the field in your model
        clumpthickness_sums = BreastCancerData.objects.values('clumpthickness').annotate(count=Count('clumpthickness'))
        cellsize_count = BreastCancerData.objects.values('cellsize').annotate(count=Count('cellsize'))

        # 'clumpthickness_sums' now contains a list of dictionaries, each with 'clumpthickness' and 'sum' keys
        for entry in clumpthickness_sums:
            print(f"Clumpthickness: {entry['clumpthickness']}, Sum: {entry['count']}")
               
        params = { "bc_data_count": breast_cancer_data_count, 
                "count_prediction_1":count_prediction_1,
                "count_prediction_0":count_prediction_0,
                "username": username, "clumpthickness_sums": clumpthickness_sums,
                "cellsize_count":cellsize_count, 
             }
        
        

        print("result", params)
        return render(request, 'dashboard.html', params)
     return render(request, 'dashboard.html', {})

def view_BC(request):
     Breast_Cancer_Data = BreastCancerData.objects.all().order_by('-id').values()
     param = {'Breast_Cancer_Data':Breast_Cancer_Data}
     return render(request, 'crud/classify_view.html', param)

def view_SP(request):
     SP_Data = Student_Performance_Data.objects.all().order_by('-id').values()
     param = {'SP_Data':SP_Data}
     return render(request, 'crud/reg_view.html', param)


def dashboardSP(request):
    
     Student_Performance_Data_count = Student_Performance_Data.objects.count()
     extra_act_counts = Student_Performance_Data.objects.values('extra_act').annotate(count=Count('extra_act'))
     hrs_study_counts = Student_Performance_Data.objects.values('hrs_study').annotate(count=Count('hrs_study'))
     average_hours = Student_Performance_Data.objects.aggregate(avg_hours=Avg('hrs_study'))['avg_hours']

     params = { "sp_data_count": Student_Performance_Data_count, 
                "extra_act_counts": extra_act_counts,
                "hrs_study_counts": hrs_study_counts,
                "average_hours": average_hours,

              }
     
     return render(request, 'dashboardSP.html', params)




def loginuser(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('dashboard')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("There is an error with username and password."))
            return redirect('login')
        
    else:
    
        return render(request, 'guest/login.html')

def register(request):
    if request.method == 'POST':
       
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        new_user = User.objects.create_user(name, email, password)
        new_user.save()
        return redirect('dashboard')
    else:
        return render(request, 'guest/register.html')


def logoutuser(request):
    logout(request)
    return redirect('login')

