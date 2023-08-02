from rest_framework import serializers
from .models import Batch, User, Branch, Location, Course, Topics, Trainee, Trainer, Address, Subjects
from datetime import *
from django.core.files.images import get_image_dimensions
from rest_framework import serializers
import logging
from django.utils.encoding import smart_str
from role_bases_auth import settings


class LocationSerializer(serializers.ModelSerializer):

    branch_ids = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ['location_id', 'branch_ids', 'city']

    def get_branch_ids(self, obj):
        branches = obj.branches.all()
        return [branch.branch_id for branch in branches]


class BranchSerializer(serializers.ModelSerializer):
    created_on = serializers.DateField(default=date.today)
    updated_on = serializers.DateField(default=date.today)
    # batches = BatchSerializer(many=True, read_only=True)
    location = LocationSerializer(source='location_id', read_only=True)
    # location_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), write_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all())

    class Meta:
        model = Branch
        # fields = ['branch_id', 'branch_name', 'created_on','updated_on', 'batches','location_id']
        fields = '__all__'

    # def get_trainees_ids(self, obj):
    #     trainees = obj.trainee_set.all()
    #     return [trainee.trainee_id for trainee in trainees]

    def to_representation(self, instance):
        request = self.context.get('request')
        if request and request.method == 'GET':
            self.fields.pop('branch', None)
            # self.fields.pop('course', None)
            # self.fields.pop('batches', None)
            # self.fields.pop('location_id', None)

        return super().to_representation(instance)

    # def get_batch_id(self, obj):
    #   batches = obj.batch_set.all()
    #   batch_data = []
    #   for batch in batches:
    #       batch_data.append({
    #           'batch_id': batch.batch_id,
    #           'batch_name': batch.batch_name,
    #           # Add other fields you want to include
    #       })
    #   return batch_data

    def create(self, validated_data):
        validated_data['created_on'] = date.today()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_on'] = date.today()
        return super().update(instance, validated_data)

    def get_location(self, obj):
        location_id = obj.location_id
        if location_id:
            try:
                location = Location.objects.get(id=location_id)
                return LocationSerializer(location).data
            except Location.DoesNotExist:
                pass
        return None

    # def get_subjects(self, obj):
    #     subjects = obj.subjects.all()
    #     subject_data = []
    #     for subject in subjects:
    #         subject_data.append({
    #             'subject_Id': subject.subject_Id,
    #             'subject_name': subject.subject_name,
    #             'created_by': subject.created_by,
    #             'created_on': subject.created_on,
    #             'updated_by': subject.updated_by,
    #             'updated_on': subject.updated_on
    #         })
    #     return subject_data
# class BatchSerializer(serializers.ModelSerializer):
#     course_id = serializers.IntegerField(write_only=True)
#     branch_id = serializers.IntegerField(write_only=True)
#     trainees_ids = serializers.SerializerMethodField()

#     class Meta:
#         model = Batch
#         fields = ['batch_id', 'batch_name', 'trainees_ids', 'branch_id', 'course_id']

#     def get_trainees_ids(self, obj):
#         trainees = obj.trainee_set.all()
#         return [trainee.trainee_id for trainee in trainees]

#     def create(self, validated_data):
#         course_id = validated_data.pop('course_id')
#         branch_id = validated_data.pop('branch_id')
#         batch = Batch.objects.create(course_id=course_id, branch_id=branch_id, **validated_data)
#         return batch

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         request = self.context.get('request')

#         if request and request.method == 'GET':
#             branch_id = representation.get('branch_id')
#             course_id = representation.get('course_id')

#             branch = Branch.objects.get(pk=branch_id)
#             course = Course.objects.get(pk=course_id)

#             representation['branch'] = BranchSerializer(branch).data
#             representation['course'] = CourseSerializer(course).data

#         return representation


class CourseSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()  # Use the SubjectSerializer
    batch_ids = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['course_id', 'course_name', 'course_duration',
                  'course_fee', 'subjects', 'created_at', 'batch_ids']

    def get_subjects(self, obj):
        subjects = obj.subjects.all()
        subjects_data = []
        for subject in subjects:
            subjects_data.append({
                'id': subject.subject_id,
                'name': subject.subject_name,
                'created_by': subject.created_by,
                'created_on': subject.created_on,
                'updated_by': subject.updated_by,
                'updated_on': subject.updated_on


            })
            print(subjects_data)
        return subjects_data

    def get_batch_ids(self, obj):
        batches = obj.batch_set.all()
        return [batch.batch_id for batch in batches]


class BatchSerializer(serializers.ModelSerializer):
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    trainees_ids = serializers.SerializerMethodField()
    branches = BranchSerializer(source='branch', read_only=True)
    courses = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = Batch
        fields = ['batch_id', 'batch_name', 'trainees_ids',
                  'branch', 'course', 'branches', 'courses']

    def get_trainees_ids(self, obj):
        trainees = obj.trainee_set.all()
        return [trainee.trainee_id for trainee in trainees]

    def to_representation(self, instance):
        request = self.context.get('request')
        if request and request.method == 'GET':
            self.fields.pop('branch', None)
            self.fields.pop('course', None)

        return super().to_representation(instance)

    def get_batches(self, obj):
        branches = obj.branches.all()
        branch_data = []
        for branch in branches:
            branch_data.append({
                'subject_Id': branch.branch_id,
                'subject_name': branch.branch_name,
                'created_by': branch.created_by,
                'created_on': branch.created_on,
                'updated_by': branch.updated_by,
                'updated_on': branch.updated_on,
                'subjects': branch.subjects
            })
            # print(subjects_data)
        return branch_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email',
                  'password', 'phone_number', 'role',  'branch_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        branch = validated_data.pop('branch_id', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        if branch is not None:
            instance.branch_id = branch

        instance.save()
        return instance


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs

        # def get_batches(self, obj):
        #     branches = obj.branches.all()
        #     branch_data=[]
        #     for branch in branches:
        #         branch_data.append({
        #             'subject_Id': branch.branch_id,
        #             'subject_name': branch.branch_name,
        #             'created_by':branch.created_by,
        #             'created_on':branch.created_on,
        #             'updated_by':branch.updated_by,
        #             'updated_on':branch.updated_on,
        #             'subjects':branch.subjects,

        #         })
        #         # print(subjects_data)
        #     return branch_data


class SubjectSerializer(serializers.ModelSerializer):
    trainer = serializers.SerializerMethodField()
    topic_ids = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()

    def get_trainer(self, obj):
        trainers = obj.trainer.all()
        trainer_data = []
        for trainer in trainers:
            trainer_data.append({
                'trainer_id': trainer.trainer_id,
                'trainer_name': trainer.trainer_name,
                'created_by': trainer.created_by,
                'created_on': trainer.created_on,
                'updated_by': trainer.updated_by,
                'updated_on': trainer.updated_on
            })
        return trainer_data

    def get_courses(self, obj):
        courses = obj.courses.all()
        course_data = []
        for course in courses:
            course_data.append({
                'course_id': course.course_id,
                'course_name': course.course_name,
                'course_duration': course.course_duration,
                'course_fee': course.course_fee,
                'created_at': course.created_at

            })
        return course_data

    def get_topic_ids(self, obj):
        topics = obj.topics_set.all()
        return [topic.topic_id for topic in topics]

    class Meta:
        model = Subjects
        fields = ['subject_id', 'subject_name', 'created_by', 'created_on',
                  'updated_by', 'updated_on', 'trainer', 'topic_ids', 'courses']


class TopicsSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(source='subject_id', read_only=True)

    class Meta:
        model = Topics
        fields = ['topic_id', 'topic_name', 'subject_Id', 'subjects']

    def get_subjects(self, obj):
        subject = obj.subject_id
        if subject:
            try:
                subject = Subjects.objects.get(id=subject.id)
                return SubjectSerializer(subject).data
            except Subjects.DoesNotExist:
                pass
        return None

    def to_representation(self, instance):
        request = self.context.get('request')
        if request and request.method == 'GET':
            self.fields.pop('subject_id', None)

        return super().to_representation(instance)


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"


class TraineeSerializer(serializers.ModelSerializer):
    address_id = AddressSerializer()
    batches = BatchSerializer(source='batch_id', read_only=True)

    class Meta:
        model = Trainee
        fields = ['trainee_id', 'trainee_name', 'trainee_age',
                  'trainee_gender', 'trainee_phonenumber', 'trainee_email', 'batch_id', 'address_id', 'batches']

    def create(self, validated_data):
        address_data = validated_data.pop('address_id')
        address = Address.objects.create(**address_data)
        trainee = Trainee.objects.create(address_id=address, **validated_data)
        return trainee

    def get_batches(self, obj):
        batch = obj.batch_id
        if batch:
            try:
                batch = Batch.objects.get(id=batch.id)
                return BatchSerializer(batch).data
            except Batch.DoesNotExist:
                pass
        return None

    def get_subjects(self, obj):
        subjects = obj.subjects.all()
        subjects_data = []
        for subject in subjects:
            subjects_data.append({
                'id': subject.subject_id,
                'name': subject.subject_name,
                'created_by': subject.created_by,
                'created_on': subject.created_on,
                'updated_by': subject.updated_by,
                'updated_on': subject.updated_on

                # Add any other desired trainer fields here
            })
            print(subjects_data)
        return subjects_data

    def to_representation(self, instance):
        request = self.context.get('request')
        if request and request.method == 'GET':
            self.fields.pop('batch_id', None)

        return super().to_representation(instance)

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address_id', None)
        if address_data:
            address_serializer = self.fields['address_id']
            address = instance.address_id
            updated_address = address_serializer.update(address, address_data)
            validated_data['address_id'] = updated_address

        return super().update(instance, validated_data)


class TrainerSerializer(serializers.ModelSerializer):
    subjects = serializers.PrimaryKeyRelatedField(
        queryset=Subjects.objects.all(), many=True, required=False, default=[])
    address_id = AddressSerializer()
    subject = serializers.SerializerMethodField()

    def get_subject(self, obj):
        subjects = obj.subjects.all()
        subjects_data = []
        for subject in subjects:
            subjects_data.append({
                'subject_id': subject.subject_id,
                'subject_name': subject.subject_name,
                'created_by': subject.created_by,
                'created_on': subject.created_on,
                'updated_by': subject.updated_by,
                'updated_on': subject.updated_on


            })
            print(subjects_data)
        return subjects_data

    def create(self, validated_data):
        address_data = validated_data.pop('address_id')
        address_serializer = AddressSerializer(data=address_data)
        address_serializer.is_valid(raise_exception=True)
        address = address_serializer.save()
        subjects = validated_data.pop('subjects')
        trainer = Trainer.objects.create(address_id=address, **validated_data)
        trainer.subjects.set(subjects)
        return trainer

    def update(self, instance, validated_data):

        address_data = validated_data.pop('address_id')
        address_serializer = AddressSerializer(
            instance.address_id, data=address_data)
        address_serializer.is_valid(raise_exception=True)
        address = address_serializer.save()
        instance.address_id = address

        subjects = validated_data.pop('subjects')
        instance.subjects.set(subjects)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        if request and request.method == 'GET':
            self.fields.pop('subjects', None)

        return super().to_representation(instance)

    class Meta:
        model = Trainer
        fields = ('trainer_id', 'trainer_name', 'trainer_phonenumber', 'triner_email',
                  'trainer_age', 'trainer_gender', 'created_by', 'created_on',
                  'updated_by', 'updated_on', 'subjects', 'address_id', 'subject')
