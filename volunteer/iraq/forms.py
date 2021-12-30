from typing import ValuesView
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Intity, NumVolunteer,Member, Poster,Region, Classification
from django.core import validators




class CreateNewUser(forms.ModelForm):
    user = forms.CharField(label='اسم المستخدم', max_length=255,help_text='اسم الستخدم يجب الايحتوي على مسافات',
                        widget= forms.TextInput(attrs={'class': 'fa pr-3 Borders7 Boxshadow Borders4 Color2 H', 'placeholder': ''}))
    email = forms.EmailField(label='البريد الإلكتروني',
                        widget= forms.EmailInput(attrs={'class': 'fa pr-3 Borders7 Boxshadow Borders4 Color2 H'}),required=True)
    password1 = forms.CharField(label='كلمة المرور',
                        widget=forms.PasswordInput(attrs={'class': 'fa pr-3 Borders7 Boxshadow Borders4 Color2 H'}), min_length=8,required=True)
    password2 = forms.CharField(label='تأكيد كلمة المرور', 
                        widget=forms.PasswordInput(attrs={'class': 'fa pr-3 Borders7 Boxshadow Borders4 Color2 H'}), min_length=8,required=True)
    class Meta:
            model = CustomUser
            fields = ('user', 'email', 'password1', 'password2')

class CreateNewIntity(forms.ModelForm):
    user = forms.CharField(label='اسم المستخدم', max_length=255,help_text='اسم الستخدم يجب الايحتوي على مسافات',
                        widget= forms.TextInput(attrs={'class': 'fa pr-3 Borders7 Boxshadow Borders4 Color2 H', 'placeholder': ''}))
    email = forms.EmailField(label='البريد الإلكتروني',
                        widget= forms.EmailInput(attrs={'class': 'fa pr-3 Borders7 Boxshadow Borders4 Color2 H'}),required=True)
    password1 = forms.CharField(label='كلمة المرور',
                        widget=forms.PasswordInput(attrs={'class': 'fa pr-3 Borders7 Boxshadow Borders4 Color2 H'}), min_length=8,required=True)
    password2 = forms.CharField(label='تأكيد كلمة المرور', 
                        widget=forms.PasswordInput(attrs={'class': 'fa pr-3 Borders7 Boxshadow Borders4 Color2 H'}), min_length=8,required=True)
    name = forms.CharField(label='اسم المؤسسة', max_length=255,help_text='اسم الستخدم يجب الايحتوي على مسافات',
                        widget= forms.TextInput(attrs={'class': 'fa pr-3 Borders7 Boxshadow Borders4 Color2 H', 'placeholder': ''}))  
    class Meta:
            model = Intity
            model = CustomUser
            fields = ('user','name', 'email', 'password1', 'password2')


class ProfileIntities(forms.ModelForm):
    
    regions=Region.objects.all()
    regions_list=[]
    for region in regions:
        small_region=(region,region.region)
        regions_list.append(small_region)
        
    classifications=Classification.objects.all()
    classifications_list=[]
    for classification in classifications:
        small_classification=(classification,classification.classification)
        classifications_list.append(small_classification)
        
    name = forms.CharField(label='اسم المؤسسة',max_length=255,help_text='',
                        widget= forms.TextInput(attrs={'class': '', 'placeholder': '' }))
    region = forms.ChoiceField(label='المحافظة',help_text='',choices=regions_list,
                        widget= forms.Select({'class': '', 'placeholder': ''}))
    created = forms.DateField(label='تأريخ التاسيس',help_text='',
                        widget= forms.DateInput(attrs={'class': '', 'placeholder': ''}))
    classification = forms.ChoiceField(label='التصنيف',help_text='',choices=classifications_list,
                        widget= forms.Select(attrs={'class': '', 'placeholder': ''}))
    abstract = forms.CharField(label='الملخص',max_length=255,help_text='',
                        widget= forms.Textarea(attrs={'class': '','rows': 3,'placeholder': ''}))
    works = forms.CharField(label='اعمالها',max_length=255,help_text='',
                        widget= forms.Textarea(attrs={'class': '','rows': 3,'placeholder': ''}))
    permission = forms.FileField(label='الترخيص',max_length=255,help_text='',
                        widget= forms.FileInput(attrs={'class': '', 'placeholder': ''}))
    intities_pic = forms.FileField(label='صورة المؤسسة',max_length=255,help_text='',
                        widget= forms.FileInput(attrs={'class': '', 'placeholder': ''}))
    facebook = forms.URLField(label='فيسبوك',max_length=255,help_text='',
                        widget= forms.URLInput(attrs={'class': '', 'placeholder': ''}))
    email=forms.EmailField(label='البريد الالكتروني',max_length=255, widget= forms.TextInput(attrs={'class': 'form-control  mb-3'}))
    class Meta:
            model = Intity
            fields =  fields = ('name','region','created','classification','abstract','works','permission','intities_pic','email','facebook')


class ProfilePeople(forms.ModelForm):
    
    regions=Region.objects.all()
    regions_list=[]
    for region in regions:
        small_region=(region,region.region)
        regions_list.append(small_region)
        
    user = forms.CharField(label='اسم الستخدم',max_length=255,help_text='',
                        widget= forms.TextInput(attrs={'class': '', 'placeholder': '' }))
    email = forms.EmailField(label='البريد الإلكتروني',
                        widget= forms.EmailInput(attrs={'class': ''}))
    phone = forms.CharField(label='رقم الهاتف',max_length=255,help_text='',
                        widget= forms.NumberInput(attrs={'class': '', 'placeholder': '' }))
    region = forms.ChoiceField(label='المحافظة',help_text='',choices=regions_list,
                        widget= forms.Select({'class': '', 'placeholder': ''}))
    birth = forms.DateField(label='تأريخ الميلاد',help_text='',
                        widget= forms.DateInput(attrs={'class': '', 'placeholder': ''}))
    gender_choice=(
        ("ذكر","ذكر"),
        ("انثى","انثى")
        )
    gender=forms.ChoiceField(label='الجنس',choices=gender_choice,required=True,widget=forms.Select(attrs={"class":"form-control  mb-3"}))
    employee=forms.CharField(label='الوظيفة', widget= forms.TextInput(attrs={'class': 'form-control  mb-3'}))
    profile_pic = forms.FileField(label='الصورة الشخصية',max_length=255,help_text='',
                        widget= forms.FileInput(attrs={'class': '', 'placeholder': ''}))
    facebook = forms.URLField(label='فيسبوك',max_length=255,help_text='',
                        widget= forms.URLInput(attrs={'class': '', 'placeholder': ''}))
    class Meta:
            model = Intity
            model = CustomUser
            fields =  fields = ('user','email','phone','region','birth','gender','employee','profile_pic','facebook')



class AddMemberForm(forms.ModelForm):
    name=forms.CharField(label='اسم العضو',max_length=255,required=True, widget= forms.TextInput(attrs={'class': 'form-control mb-3'}))
    gender_choice=(
        ("ذكر","ذكر"),
        ("انثى","انثى")
    )
    gender=forms.ChoiceField(label='الجنس',choices=gender_choice,required=True,widget=forms.Select(attrs={"class":"form-control  mb-3"}))
    regions=Region.objects.all()
    regions_list=[]
    for region in regions:
        small_region=(region.id,region.region)
        regions_list.append(small_region)  
    region=forms.ChoiceField(label='المحافظة',choices=regions_list,widget=forms.Select(attrs={'class':'form-control mb-3 .float-right'}))
    employee=forms.CharField(label='الوظيفة', widget= forms.TextInput(attrs={'class': 'form-control  mb-3'}))
    phone=forms.CharField(label='رقم الهاتف',max_length=255,widget= forms.NumberInput(attrs={'class': 'form-control  mb-3'}))
    email=forms.EmailField(label='البريد الالكتروني',max_length=255, widget= forms.TextInput(attrs={'class': 'form-control  mb-3'}))
    member_image=forms.FileField(label='صورة العضو',widget=forms.FileInput(attrs={'class':'form-control mb-3'}))
    class Meta:
        model = Intity
        fields =  fields = ('name','gender','region','employee','phone','email','member_image')






class AddPosterForm(forms.ModelForm):
    name = forms.CharField(label='اسم المؤسسة', max_length=255,help_text='اسم المستخدم يجب الا يحتوي على مسافات' ,
                        widget= forms.TextInput(attrs={'class': 'form-control  mb-3'}))
    regions=Region.objects.all()
    regions_list=[]
    for region in regions:
        small_region=(region.id,region.region)
        regions_list.append(small_region)  
    region=forms.ChoiceField(label='المحافظة',choices=regions_list,widget=forms.Select(attrs={'class':'form-control mb-3 .float-right'}))
    place = forms.CharField(label='المكان', max_length=255,help_text='اسم المستخدم يجب الا يحتوي على مسافات' ,
                        widget= forms.TextInput(attrs={'class': 'form-control  mb-3'}))
    classifications=Classification.objects.all()
    classifications_list=[]
    for classification in classifications:
        small_classification=(classification,classification.classification)
        classifications_list.append(small_classification)
    classification = forms.ChoiceField(label='التصنيف',help_text='',choices=classifications_list,
                        widget= forms.Select(attrs={'class': '', 'placeholder': ''}))
    posts = forms.CharField(label='الاعلان',max_length=255,help_text='',
                        widget= forms.Textarea(attrs={'class': '','rows': 3,'placeholder': ''}))
    poster_image=forms.FileField(label='صورة الاعلان',widget=forms.FileInput(attrs={'class':'form-control mb-3'}))
    date_poster = forms.DateField(label='تأريخ التاسيس',help_text='',
                        widget= forms.DateInput(attrs={'class': '', 'placeholder': ''}))
    class Meta:
        model = Poster
        fields = ('name','place','region','classification','posts','poster_image','date_poster')


class VolunteerForm(forms.ModelForm):
    regions=Region.objects.all()
    regions_list=[]
    for region in regions:
        small_region=(region,region.region)
        regions_list.append(small_region)
        name_intity = forms.CharField(label='اسم المؤسسة', max_length=255,help_text='',
                        widget= forms.TextInput(attrs={'class': '', 'placeholder': ''}))
        name = forms.CharField(label='الاسم', max_length=255,help_text='',
                        widget= forms.TextInput(attrs={'class': '', 'placeholder': ''}))
        age=forms.CharField(label='العمر',max_length=255,widget= forms.NumberInput(attrs={'class': 'form-control  mb-3'}))
        region=forms.ChoiceField(label='المحافظة',choices=regions_list,widget=forms.Select(attrs={'class':'form-control mb-3 .float-right'}))
        gender_choice=(
        ("ذكر","ذكر"),
        ("انثى","انثى")
        )
        gender=forms.ChoiceField(label='الجنس',choices=gender_choice,required=True,widget=forms.Select(attrs={"class":"form-control  mb-3"}))
        employee = forms.CharField(label='الوظيفة',max_length=255,help_text='',
                    widget= forms.TextInput(attrs={'class': '', 'placeholder': ''}))
        volunteer_image=forms.FileField(label='الصورة الشخصية',widget=forms.FileInput(attrs={'class':'form-control mb-3'}))
       
        class Meta:
                model = NumVolunteer
                # model = Intity
                fields = ('name_intity','name','age','region','gender','employee','volunteer_image')





