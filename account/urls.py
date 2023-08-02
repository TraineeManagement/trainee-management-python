from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
     path('register/' , RegisterView.as_view(),name='register'),
    path('login/' , LoginView.as_view(),name='login'),
    path('user/' , UserView.as_view(),name='user'),
    path('logout/' , LogoutView.as_view(),name='logout'),
    # Branch
    path('branchinsertandgettingall/',BranchCreateListAPIView.as_view(),name="branchInsertandGettingall"),
     path('branchupdateanddeleteandretraivebyid/<int:pk>/',BranchRetrieveUpdateDeleteAPIView.as_view(),name="BranchupdateAndDeleteAndRetraiveByID"),
    #  Batch
    path('batchinsertandgettingall/',BatchInsertandGettingall.as_view(),name="batchInsertandGettingall"),
    path('batchupdateanddeleteandretraivebyid/<int:pk>/',BatchupdateAndDeleteAndRetraiveByID.as_view(),name="batchupdateAndDeleteAndRetraiveByID"),
     # Location
    path('locationinsertandgettingall/', LocationCreateListAPIView.as_view(),
         name="LocationInsertandGettingall"),
    path('locationupdateandDeleteandretraivebyid/<int:pk>/',
         LocationRetrieveUpdateDeleteAPIView.as_view(), name="LocationUpdateAndDeleteAndRetraiveByID"),
     # Course
    path('courseinsertandgettingall/', CourseInsertandGettingall.as_view(),
         name="courseInsertandGettingall"),
    path('courseupdateanddeleteandretraivebyid/<int:pk>/',
         CourseupdateAndDeleteAndRetraiveByID.as_view(), name="CourseupdateAndDeleteAndRetraiveByID"),
    # Subject
    path('subjectinsertandgettingall/',
         SubjectListCreateView.as_view(), name='trainer-list'),
    path('subjectupdateanddeleteandretrievebyid/<int:pk>/', SubjectRetrieveUpdateDestroyView.as_view(),
         name='subject-retrieve-update-destroy'),
    # Trainer
    path('trainerinsertandgettingall/', 
         TrainerListCreateView.as_view(), name='trainer-list-create'),
    path('trainerupdateanddeleteandretraivebyid/<int:pk>/', TrainerRetrieveUpdateDestroyView.as_view(),
         name='trainer-retrieve-update-destroy'),
    # Topics
    path('topicinsertandgettingall/', TopicInsertandGettingall.as_view(),
         name="TopicInsertandGettingall"),
    path('topicupdateAndDeleteAndRetraiveByID/<int:pk>/',
         TopicupdateAndDeleteAndRetraiveByID.as_view(), name="TopicupdateAndDeleteAndRetraiveByID"),
    # Address
    path('addressinsertandgettingall/', AddressInsertandGettingall.as_view(),
         name="AddressInsertandGettingall"),
    path('addressupdateanddeleteandretrievebyid/<int:pk>/',
         AddressUpdateAndDeleteAndRetrieveByID.as_view(), name=" AddressUpdateAndDeleteAndRetrieveByID"),
    # Traineee
    path('traineeinsertandgettingall/', TraineeInsertandGettingall.as_view(),
         name="TraineeInsertandGettingall"),
    path('traineeupdateanddeleteandretrievebyid/<int:pk>/',
         TraineeUpdateAndDeleteAndRetrieveByID.as_view(), name=" TraineeUpdateAndDeleteAndRetrieveByID"),

]