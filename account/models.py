from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.BigIntegerField()
    role = models.CharField(max_length=45, default="admin")
    status = models.CharField(max_length=45)
    branch_id = models.ForeignKey('Branch', on_delete=models.CASCADE,default=None,null=True,related_name='branch',db_column='branch_id')
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'phone_number', 'role']

class Location(models.Model):
    class Meta:
        db_table = 'location'
    location_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=100)



class Branch(models.Model):
    class Meta:
        db_table = 'branch'
    
    branch_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=45)
    status = models.CharField(max_length=45,default="Active")
    created_by = models.CharField(max_length=45,default="sharath")
    created_on = models.DateField(default=date.today)
    updated_by = models.CharField(max_length=45,default="sharath")
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='branches',default="1")
    updated_on = models.DateField(default=date.today)
    
class Batch(models.Model):
    batch_id=models.AutoField(primary_key=True)
    batch_name=models.CharField(max_length=100)
    branch = models.ForeignKey('Branch',on_delete=models.CASCADE,null=True,blank=True, related_name='batches')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        db_table = 'batch'

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    course_duration = models.CharField(max_length=100)
    course_fee = models.IntegerField(default=35000)  # Add default value here
    subjects = models.ManyToManyField('Subjects', related_name='courses')
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, editable=False)

    class Meta:
        db_table = 'course'

class Trainer(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    trainer_name = models.CharField(max_length=100)
    trainer_phonenumber = models.CharField(max_length=10)
    triner_email = models.EmailField(max_length=254)
    trainer_age = models.IntegerField()
    trainer_gender = models.CharField(max_length=10)
    created_by = models.CharField(max_length=100, default="siva")
    created_on = models.DateField(default=date.today)
    updated_by = models.CharField(max_length=100, default="siva")
    updated_on = models.DateField(default=date.today)
    address_id = models.OneToOneField(
        'Address', on_delete=models.CASCADE, null=True, blank=True)

class Subjects(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=100,)
    created_by = models.CharField(max_length=100, default="siva")
    created_on = models.DateField(default=date.today)
    updated_by = models.CharField(max_length=100, default="siva")
    updated_on = models.DateField(default=date.today)
    trainer = models.ManyToManyField(Trainer, related_name='subjects')

    class Meta:
        db_table = 'subjects'



class Topics(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic_name = models.CharField(max_length=100)
    subject_Id = models.ForeignKey(Subjects, on_delete=models.CASCADE)

    class Meta:
        db_table = 'topics'


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    door_no = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    state = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
   

    class Meta:
        db_table = 'address'


class Trainee(models.Model):
    trainee_id = models.AutoField(primary_key=True)
    trainee_name = models.CharField(max_length=100)
    trainee_age = models.IntegerField()
    trainee_gender = models.CharField(max_length=20)
    trainee_phonenumber = models.CharField(max_length=10)
    trainee_email = models.EmailField(max_length=254)
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE)
    address_id = models.OneToOneField(Address, on_delete=models.CASCADE)

    class Meta:
        db_table = 'trainee'
