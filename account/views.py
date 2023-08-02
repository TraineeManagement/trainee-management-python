from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import  ListModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from django.views.decorators.csrf import csrf_exempt
from rest_framework.mixins import CreateModelMixin
from rest_framework.exceptions import AuthenticationFailed
from account.serializers import *
from django.contrib.auth import authenticate
from .models import User
from rest_framework import status
import jwt, datetime
import logging
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.models import User
import random
from .serializers import BranchSerializer

User = get_user_model()
 
logger=logging.getLogger(__name__)

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class GetByEmail(generics.RetrieveAPIView):
      serializer_class = UserSerializer
      def get_object(self):
        email = self.kwargs['email']
        return User.objects.get(email=email)  

class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Incorrect email or password!')

        payload = {
            'id': user.email,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        user_details = User.objects.get(email=email)

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'user': UserSerializer(user_details).data  # Include serialized user details
        }
        return response
    
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(email=payload['id']).first()
        print(user)
        serializer = UserSerializer(user)
        return Response(serializer.data) 

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
# class ForgotPassword():
#     def post():

class GetAllUsersEmail(GenericAPIView, ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        try:
            response = self.list(request)
            user_emails = [user['email'] for user in response.data]
            return Response(user_emails)
        except Exception as e:
            logger.exception("An error occurred while getting all user emails")
            return Response(status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class GettingAllUsers(GenericAPIView,ListModelMixin):
     queryset = User.objects.all()
     serializer_class=UserSerializer
     def get(self,request):
        try:
           return self.list(request)
        except Exception as e:
            logger.exception("An error occurred while getting all users")
     
class UpdateUser(GenericAPIView,UpdateModelMixin):
      queryset = User.objects.all()
      serializer_class=UserSerializer
      def put(self,request,**kwargs):
          try:
            return self.update(request,**kwargs)
          except Exception as e:
              logger.exception("An error occurred while update a user: %s", str(e))
      
class DeleteUser(GenericAPIView,DestroyModelMixin):
       queryset = User.objects.all()
       serializer_class=UserSerializer
       def delete(self,request,**kwargs):
          try:
            return self.destroy(request,**kwargs)
          except Exception as e:
              logger.exception("An error occurred while delete the user: %s")
              print("id is not there")

class GetById(GenericAPIView,RetrieveModelMixin):
      queryset = User.objects.all()
      serializer_class=UserSerializer
      def get(self,request,**kwargs):
           try:
             return self.retrieve(request,**kwargs)  
           except Exception as e:
               logger.exception("An error occurred while getting a user By Id")         

class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist.'}, status=400)

        otp = random.randint(1000, 9999)
        logger.info(f'OTP: {otp}')  # Log the OTP value for debugging purposes

        # Send OTP to user's email
        subject = 'Password Reset OTP'
        message = f'Your OTP for password reset is: {otp}'
        from_email = 'exabc@gmail.com'
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            logger.info('OTP sent successfully')
            return Response({'message': 'OTP sent successfully.', 'otp': otp})
        except Exception as e:
            logger.error(f'Failed to send OTP: {e}')

        return Response({'message': 'Failed to send OTP.'}, status=500)


class BranchCreateListAPIView(APIView):
    def get(self, request):
        branches = Branch.objects.all()
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data)
    def post(self, request):
        data = {
            'location_id': request.data.get('location_id'),
            'branch_name': request.data.get('branch_name'),
            'status': request.data.get('status'),
            'created_by': request.data.get('created_by'),
            'updated_by': request.data.get('updated_by')
        }

        serializer = BranchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class BranchRetrieveUpdateDeleteAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    @csrf_exempt
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class LocationCreateListAPIView(GenericAPIView, CreateModelMixin, ListModelMixin):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    
    @csrf_exempt
    def post(self, request):
        return self.create(request)
    
    @csrf_exempt
    def get(self, request):
        return self.list(request)


class LocationRetrieveUpdateDeleteAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    @csrf_exempt
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


logger=logging.getLogger(__name__)


class CourseInsertandGettingall(GenericAPIView,CreateModelMixin,ListModelMixin):
    queryset = Course.objects.all()
    serializer_class=CourseSerializer
    #  def post(self,request):
    #       logging.info("Data inserted successfully..")
    #       return self.create(request)
    #  def get(self,request):
    #     return self.list(request)
    def get(self, request, format=None):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        subjects_ids = request.data.pop('subjects', [])  # Extract trainer IDs from request data
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.save()
            subject.subjects.set(subjects_ids)  # Assign trainers to the subject
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseupdateAndDeleteAndRetraiveByID(GenericAPIView,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin):
     queryset=Course.objects.all()
     serializer_class=CourseSerializer
     def put(self,request,**kwargs):
          logging.info("Data updated successfully")
          return self.update(request,**kwargs)
     def delete(self,request,**kwargs):
          logging.info("deleted successfully..")
          return self.destroy(request,**kwargs)
     def get(self,request,**kwargs):
          return self.retrieve(request,**kwargs)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Subjects, Trainer
from .serializers import SubjectSerializer, TrainerSerializer
# from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class SubjectListCreateView(APIView):
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
    def get(self, request, format=None):
        subjects = Subjects.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        trainer_ids = request.data.pop('trainer', [])  # Extract trainer IDs from request data
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.save()
            subject.trainer.set(trainer_ids)  # Assign trainers to the subject
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubjectRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk, format=None):
        subject = Subjects.objects.get(pk=pk)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        subject = Subjects.objects.get(pk=pk)
        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        subject = Subjects.objects.get(pk=pk)
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TrainerListCreateView(generics.ListCreateAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

    def post(self, request, format=None):
        subject_ids = request.data.pop('subjects', [])
        serializer = TrainerSerializer(data=request.data)
        if serializer.is_valid():
            trainer = serializer.save()
            trainer.subjects.set(subject_ids)  # Assign subjects to the trainer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TrainerRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk, format=None):
        trainer = Trainer.objects.get(pk=pk)
        serializer = TrainerSerializer(trainer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        trainer = Trainer.objects.get(pk=pk)
        serializer = TrainerSerializer(trainer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        trainer = Trainer.objects.get(pk=pk)
        trainer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TopicInsertandGettingall(GenericAPIView,CreateModelMixin,ListModelMixin):
     queryset = Topics.objects.all()
     serializer_class=TopicsSerializer
     def post(self,request):
          logger.info("Data inserted successfully")
          return self.create(request)
     def get(self,request):
        return self.list(request)
     
class TopicupdateAndDeleteAndRetraiveByID(GenericAPIView,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin):
     queryset=Topics.objects.all()
     serializer_class=TopicsSerializer
     def put(self,request,**kwargs):
          logger.info("data updated successfully")
          return self.update(request,**kwargs)
     def delete(self,request,**kwargs):
          logger.info("deleted successfully")
          return self.destroy(request,**kwargs)
     def get(self,request,**kwargs):
          return self.retrieve(request,**kwargs)
     


class  AddressInsertandGettingall(GenericAPIView,CreateModelMixin,ListModelMixin):
        queryset = Address.objects.all()
        serializer_class=AddressSerializer
        def post(self,request):
            logger.info("records inserted")
            return self.create(request)
        def get(self,request):
            logger.info("records fetched")
            return self.list(request)


# @csrf_exempt
class  AddressUpdateAndDeleteAndRetrieveByID(GenericAPIView,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin):
     queryset=Address.objects.all()
     serializer_class=AddressSerializer
     def put(self,request,**kwargs):
          logger.info("records updated")
          return self.update(request,**kwargs)
     def delete(self,request,**kwargs):
          logger.info("records deleted")
          return self.destroy(request,**kwargs)
     def get(self,request,**kwargs):
          return self.retrieve(request,**kwargs)
     

class TraineeInsertandGettingall(GenericAPIView,CreateModelMixin,ListModelMixin):
        queryset = Trainee.objects.all()
        serializer_class=TraineeSerializer
        def post(self,request):
            logger.info("records inserted")
            return self.create(request)
        def get(self,request):
            logger.info("records fetched")
            return self.list(request)


# @csrf_exempt
class  TraineeUpdateAndDeleteAndRetrieveByID(GenericAPIView,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin):
     queryset=Trainee.objects.all()
     serializer_class=TraineeSerializer
     def put(self,request,**kwargs):
          logger.info("records updated")
          return self.update(request,**kwargs)
     def delete(self,request,**kwargs):
          logger.info("records deleted")
          return self.destroy(request,**kwargs)
     def get(self,request,**kwargs):
          return self.retrieve(request,**kwargs)



class BatchInsertandGettingall(GenericAPIView, CreateModelMixin, ListModelMixin):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

    def post(self, request, *args, **kwargs):
        logger.info("Data inserted successfully")
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

     

class BatchupdateAndDeleteAndRetraiveByID(GenericAPIView,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin):
     queryset=Batch.objects.all()
     serializer_class=BatchSerializer
     def put(self,request,**kwargs):
          logger.info("data updated successfully")
          return self.update(request,**kwargs)
     def delete(self,request,**kwargs):
          logger.info("deleted successfully")
          return self.destroy(request,**kwargs)
     def get(self,request,**kwargs):
          return self.retrieve(request,**kwargs)
 
    
    
