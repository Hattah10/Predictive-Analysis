from django.urls import path
from . import views
from . import mltest, mlpredict


urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.loginuser, name='login'),
    path('register', views.register, name='register'),
    path('accounts/login/', views.logoutuser, name='logout'),
    path('dashboard', views.dashboarBC, name='dashboard'),
    path('dashboardSP', views.dashboardSP, name='dashboardSP'),
    path('DatasetBC', views.view_BC, name='view_BC'),
    path('DatasetSP', views.view_SP, name='view_SP'),
    path('classify/', mltest.diabetestTest, name='classify'),
    path('predictBC/', mlpredict.predictBC, name='predictBC'),
    path('predictSP/', mlpredict.predictSP, name='predictSP'),
    path('train_modelBC/', mlpredict.ClassifyTrainModel, name='train_modelBC'),
    path('train_modelSP/', mlpredict.RegressionTrainModel, name='train_modelSP'),

]
