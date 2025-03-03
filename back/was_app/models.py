from django.db import models

#Описание всех таблиц
class Skills(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.BooleanField(default=0) # hard / soft
    skill_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    test = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'skills'

class AuthUser(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=255)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

class UserForm(models.Model):
    form_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    gender = models.BooleanField()
    city = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    dd_mm_yy = models.DateField()
    surname = models.CharField(max_length=128)
    middlename = models.CharField(max_length=128)

    class Meta:
        managed = True
        db_table = 'form'


class UserSkill(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skills, on_delete=models.CASCADE)
    level = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'user-skill'

class Cources(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)
    difficulty = models.IntegerField()
    description = models.CharField(max_length=255)
    duration_hrs = models.IntegerField()


    class Meta:
        managed = True
        db_table = 'cources'


class Messages(models.Model):
    id = models.AutoField(primary_key=True)
    parent_message_id = models.IntegerField(default=None)
    author = models.ForeignKey(AuthUser, on_delete=models.SET_NULL,  null=True)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=1023)


    class Meta:
        managed = True
        db_table = 'messages'