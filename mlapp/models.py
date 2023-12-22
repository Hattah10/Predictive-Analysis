from django.db import models

# Create your models here.
class Diabetesdata(models.Model):
    preg = models.FloatField()
    gluc = models.FloatField()
    blood = models.FloatField()
    skin = models.FloatField()
    ins = models.FloatField()
    bmi = models.FloatField()
    dbf = models.FloatField()
    age = models.FloatField()
    prediction = models.CharField(max_length=255)

    def __str__(self):
        return f"Diabetesdata(id={self.id}, prediction={self.prediction})"
    
    class Meta:
        managed = False
        db_table = 'diabetes_data'

# Create your models here.
class BreastCancerData(models.Model):
    clumpthickness = models.FloatField()
    cellsize = models.FloatField()
    cellshape = models.FloatField()
    marginal = models.FloatField()
    singlesize = models.FloatField()
    barenuclei = models.FloatField()
    blandchromatin = models.FloatField()
    nucleoli = models.FloatField()
    mitoses = models.FloatField()
    prediction = models.FloatField(max_length=255)

    def __str__(self):
        return f"BreastCancerData(id={self.id}, prediction={self.prediction})"
    
    class Meta:
        managed = False
        db_table = 'breastcancer_dataset'

# Create your models here.
class Student_Performance_Data(models.Model):
    hrs_study = models.FloatField()
    prev_score = models.FloatField()
    extra_act = models.FloatField()
    sleep_hrs = models.FloatField()
    question_papers = models.FloatField()
    Performance = models.FloatField()
 
    def __str__(self):
        return f"Student_Performance_Data(id={self.id}, Performance={self.Performance})"
    
    class Meta:
        managed = False
        db_table = 'ml_student_performance'