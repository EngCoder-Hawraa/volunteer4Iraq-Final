
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import UUIDField
import uuid
# from django.db.models.fields import SlugField
from django.db.models.signals import post_save,post_delete
# from notifications.models import Notification
from django.utils.text import slugify
import uuid
from django.dispatch import receiver
from django.urls import reverse
#import image from pillow desktop
from PIL import Image
from django.template.defaultfilters import date, slugify, title

# Create your models here.


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user_type_data=((1,"HOD"),(2,"people"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)




class Classification(models.Model):
    Ed = 'تعليم'
    Ev = 'بيئة'
    H = 'صحة'
    A = 'فنون'
    O = 'أخرى'
    classification = [
        (Ed , 'تعليم'),(Ev , 'بيئة'),(H, 'صحة'),(A, 'فنون'),(O, 'أخرى')
    ]
    classification = models.CharField(
        max_length=255,choices= classification,default= Ed)
    def __str__(self):
        return self.classification


class Region(models.Model):
    E = 'اربيل'
    AN = 'الانبار'
    BA = 'بابل'
    B = 'بغداد'
    Bs = 'البصرة'
    Du = 'دهوك'
    Q = 'القادسية'
    D = 'ديالى'
    Dh = 'ذي قار'
    S ='السليمانية'
    Sa ='صلاح الدين'
    K ='كركوك'
    Ka ='كربلاء'
    Mu ='المثنى'
    M ='ميسان'
    Na ='النجف'
    N ='نينوى'
    W ='واسط'
    region = [
        (E,'Erbil' ),(AN, 'Al-Anbar'),(BA, 'Babil'),(B, 'Baghdad'),
        (Bs, 'Basrah'),(Du, 'Dohuk'),(Q, 'Al-Qadisyah'),(D, 'Diyala'),
        (Dh,'Dhi Qar'),(S,'Sulymaniah'),(Sa, 'Salah Din'),(K, 'Kirkuk'),
        (Ka, 'Karbala'),(Mu,'Muthana'),(M, 'Maysan'),(Na,'Najaf'),
        (N, 'Nineveh'),(W, 'Wasit')
    ]
    region = models.CharField(
        max_length=255,choices= region,default=E)
    def __str__(self):
        return self.region




class Intity(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=255,null=True)
    facebook=models.URLField(max_length=255,default='https://www.facebook.com/')
    email = models.CharField(max_length=255,null=False)
    region=models.CharField(max_length=255,null=False)
    created=models.DateField(null=False)
    classification=models.CharField(max_length=255,null=False)
    works=models.TextField(default="",null=False)
    abstract=models.TextField(default="",null=False)
    intities_pic=models.ImageField(default='building.png',upload_to='images',null=False) 
    permission=models.FileField(upload_to='images',null=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    class Meta:
      verbose_name_plural = "intities"
    def __str__(self):
        return self.admin.username
    
    
    
   
    


class People(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    phone=models.CharField(max_length=255,null=True)
    birth=models.DateField(max_length=255, null=True, default="1994-10-07")
    facebook=models.URLField(max_length=255,default='https://www.facebook.com/')
    gender=models.CharField(max_length=255)
    employee=models.CharField(max_length=255, null=True)
    region=models.CharField(max_length=255,null=True)
    profile_pic=models.ImageField(default='default.png', upload_to='profile_pics')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects=models.Manager()
    def __str__(self):
        return self.admin.username
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        profile_pic =Image.open(self.profile_pic.path)
        if profile_pic.width > 300 or profile_pic.height > 300:
            output_size =(300, 300)
            profile_pic.thumbnail(output_size)
            profile_pic.save(self.profile_pic.path)
    




@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            Intity.objects.create(admin=instance,email="volunteer4iraq@gmail.com",region="غير معروف",created="1990-10-07",classification="غير معروف",works="لا يوجد",abstract="لايوجد")
        if instance.user_type==2:
            People.objects.create(admin=instance,phone="964000000000",birth="1994-10-07",facebook="https://facebook.com/",gender="غير معروف",employee="غير معروف",region="غير معروف")


@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type ==1:
        instance.intity.save()
    if instance.user_type ==2:
        instance.people.save()
    # if instance.user_type ==3:
    #     instance.people.save()





class Member(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    admin=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    gender=models.CharField(max_length=255)
    region=models.ForeignKey(Region,on_delete=models.CASCADE)
    employee=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    email=models.EmailField()
    member_image=models.FileField(null=True,blank=True,upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return self.name
   
   
class Poster(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    admin=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    region=models.ForeignKey(Region,on_delete=models.CASCADE)
    place=models.CharField(max_length=255)
    classification=models.CharField(max_length=255)
    posts=models.CharField(max_length=1000)
    poster_image=models.FileField(null=True,blank=True,upload_to='images')
    date_poster=models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    class Meta:
      verbose_name_plural = "posters"

    # def __str__(self):
    #     return self.admin

class NumVolunteer(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    n_intity=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    age=models.IntegerField()
    gender=models.CharField(max_length=255)
    region=models.CharField(max_length=255)
    employee=models.CharField(max_length=255)
    volunteer_image=models.FileField(null=True,blank=True,upload_to='images')
    date_Volunteer = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return self.name

class Comment(models.Model):
    comm_name = models.CharField(max_length=100, blank=True)
    comment_pic=models.ForeignKey(Intity, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    likes = models.ManyToManyField(CustomUser, related_name='blog_comment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    @property
    def total_like(self):
        return self.likes.all.count()


    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-" + str(self.author))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name + ' | ' + str(self.author)

    class Meta:
        ordering = ['created_at']


class Comment_User(models.Model):
    comm_name = models.CharField(max_length=100, blank=True)
    comment_pic=models.ForeignKey(People, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    likes = models.ManyToManyField(CustomUser, related_name='blog_comment_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    @property
    def total_like(self):
        return self.likes.all.count()


    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-" + str(self.author))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name + ' | ' + str(self.author)

    class Meta:
        ordering = ['created_at']




# class Reply(models.Model):
#     comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='replies')
#     reply_body = models.TextField(max_length=500)
#     author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     objects = models.Manager()

#     def __str__(self):
#         return "reply to " + str(self.comment_name.comm_name)


