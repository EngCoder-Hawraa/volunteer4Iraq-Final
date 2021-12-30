from typing import Any
from django.http.response import Http404
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileIntities,AddMemberForm,AddPosterForm,VolunteerForm
from django.contrib import messages
# from django.contrib.auth.models import User,Group
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.db.models import Q # new
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.views.generic import TemplateView, ListView ,CreateView
from django.urls import reverse
from django.template import loader




# # ========Views for Admin=================#

@login_required(login_url='doLogin')
def dashboard(request):
    members=Member.objects.all()
    intitys=Intity.objects.all()
    context = {
        'members':members,
        'intitys':intitys,
        'title':'dashboard',
    }
    return render(request, 'hod_template/dashboard.html', context)


@login_required(login_url='doLogin')
def admin_home(request):
    context = {
        'title':'الرئيسية',
    }
    return render(request,"hod_template/home_content.html",context)


@login_required(login_url='doLogin')
def details(request):
    context = {
    'title':'قراءة المزيد',
    }
    return render(request, 'hod_template/details.html', context)







@login_required(login_url='doLogin')
def profile_intities(request):
    context = {
        'title':'معلومات المؤسسة',
        'intitys': Intity.objects.all(),
        'regions': Region.objects.all(),
        'classification': Classification.objects.all(),
    }
    return render(request,"hod_template/profile_intities_template.html", context)










@login_required(login_url='doLogin')
def update_intities(request,intity_id):
    intity=Intity.objects.get(id=intity_id)
    form = ProfileIntities(instance=intity)
    if request.method == 'POST':
        form = ProfileIntities(request.POST,request.FILES,instance=intity)
        if form.is_valid():
            form.save()
            messages.success(request,"تم التحديث بنجاح")
            return HttpResponseRedirect("/profile_intities")
    context = {
        'form':form,
        'title':'معلومات المؤسسة',
        }
    return render(request, "hod_template/update_intities_template.html", context)




  


@login_required(login_url='doLogin')
def intities(request):
    region = Region.objects.all()
    classification= Classification.objects.all()
    intitys = Intity.objects.all().order_by('-created_at')
    paginator = Paginator(intitys, 12)
    page = request.GET.get('page')
    try:
        intitys = paginator.page(page)
    except PageNotAnInteger:
        intitys = paginator.page(1)
    except EmptyPage:
        intitys = paginator.page(paginator.num_page)
    context = {
        'num_intity': Intity.objects.filter().count(),
        'intitys' : intitys,
        'page': page,
        'region': region,
        'classification': classification,
        'title':'المؤسسات'
    }
    return render(request, 'hod_template/intities.html', context)


@login_required(login_url='doLogin')
def delete_intities(request, intity_id):
    intity=Intity.objects.get(id=intity_id)
    intity.delete()
    messages.error(request, "تم الحذف بنجاح")
    return HttpResponseRedirect("/profile_intities")


class SearchIntitiesResultsView(ListView):
    model = Intity
    template_name = 'hod_template/search_intities_results.html'

    ordering = ['id']
    paginate_by = 12
    paginate_orphans = 1
    def get_queryset(self,*args,**kwargs): # new
        query = self.request.GET.get('q')
        object_list = Intity.objects.filter(
            Q(name__icontains = query)| Q(classification__icontains=query)|Q(region__icontains=query)
        )
        try:
            return object_list
        except Http404:
            self['page'] =1
            return object_list









@login_required(login_url='doLogin')
def view_image(request):
    context = {
        'intitys' : Intity.objects.all(),
        'title':'الترخيص'
    }
    return render(request, 'hod_template/permission.html', context)


@login_required(login_url='doLogin')
def more_read_intities(request,intity_id):
    intity=Intity.objects.get(id=intity_id)
    context = {
        'intity' : intity,
        'region': Region.objects.all(),
        'classification': Classification.objects.all(),
        'title':'معلومات المؤسسة'
    }
    return render(request, 'hod_template/more_read_intities.html', context)








  
@login_required(login_url='doLogin')
def manage_members(request,member_id):
    adminhod=CustomUser.objects.get(id=member_id)
    members=adminhod.member_set.all()
    form = AddMemberForm()
    # members = Member.objects.order_by('-created_at').filter()
    paginator = Paginator(members, 10)
    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_page)
    context = {
        'form':form,
        'adminhod':adminhod,
        'members': members,
        'regions': Region.objects.all(),
        'page': page,
        'title':'الاعضاء'
    }
    return render(request,"hod_template/manage_member.html", context)




@login_required(login_url='doLogin')
def add_member_save(request):
    form = AddMemberForm()
    if request.method == 'POST':
        form = AddMemberForm(request.POST,request.FILES)
        if form.is_valid():
            member_id=request.POST.get('id')
            region=Region.objects.get(id=request.POST.get('region',''))
            member=Member(name = form.cleaned_data['name'],phone = form.cleaned_data['phone'],
            region=region,employee = form.cleaned_data['employee'],gender = form.cleaned_data['gender'],
            email = form.cleaned_data['email'],member_image = form.cleaned_data['member_image'],
            admin=request.user)
            member.save()
            messages.success(request,"تم الاضافة بنجاح")
            return HttpResponseRedirect(reverse("manage_members",kwargs={"member_id":member_id}))
    else:
        form = AddMemberForm()
    context = {
        'form':form,
        'title':'معلومات المؤسسة',
        }
    return render(request, "hod_template/manage_members.html", context)


@login_required(login_url='doLogin')
def update_member(request,member_id):
    intity=Member.objects.get(id=member_id)
    member=Member.objects.get(id=member_id)
    form = AddMemberForm(instance=intity)
    if member==None:
        return HttpResponse("Member Not Found")
    else:
        context = {
        'form': form, 
        'regions': Region.objects.all(),
        'intitys':Intity.objects.all(),
        'member':member,
        }
        return render(request,"hod_template/edit_member.html", context)



@login_required(login_url='doLogin')
def delete_member(request,member_id):
    member=Member.objects.get(id=member_id)
    if member==None:
        return HttpResponse("Member Not Found")
    else:
        context = {
        'regions': Region.objects.all(),
        'intitys':Intity.objects.all(),
        'member':member,
        }
        return render(request,"hod_template/delete_member.html", context)

   
@login_required(login_url='doLogin')
def deletes(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        member=Member.objects.get(id=request.POST.get('id',''))
        member.delete()
        members=CustomUser.objects.get(id=request.POST.get('user_id',''))
        messages.error(request, "تم الحذف بنجاح")
        return HttpResponseRedirect("manage_members/"+str(members.id)+"")
    
    
    





@login_required(login_url='doLogin')
def edit_member(request):
        members=CustomUser.objects.get(id=request.POST.get('user_id',''))
        member=Member.objects.get(id=request.POST.get('id',''))
        if member==None:
            return HttpResponse("<h2>Poster Not Found</h2>")
        else:
            # form = AddMemberForm(request.POST,request.FILES)
            # if request.method == 'POST':
                # form = AddMemberForm(request.POST,request.FILES)
                # if form.is_valid():
            try:
                if request.FILES.get('member_image')!=None:
                    file = request.FILES['member_image']
                    fs = FileSystemStorage()
                    member_img = fs.save(file.name, file)
                else:
                    member_img=None
                if member_img!=None:
                    member.member_image=member_img
                member.admin =request.user
                member.name=request.POST.get('name','')
                member.gender=request.POST.get('gender','')
                region=Region.objects.get(id=request.POST.get('region',''))
                member.region=region
                member.employee=request.POST.get('employee','')
                member.phone=request.POST.get('phone','')
                member.email=request.POST.get('email','')
                member.save()
                messages.success(request,"تم التعديل بنجاح")
                return HttpResponseRedirect("manage_members/"+str(members.id)+"")
            except Exception as e:
                print(e)
                messages.error(request,"فشل في التعديل")
                return HttpResponseRedirect("manage_members/"+str(members.id)+"")
                    


@login_required(login_url='doLogin')
def declaration(request):
    form = AddPosterForm()
    regions = Region.objects.all()
    posters=Poster.objects.order_by('-created_at')
    classifications= Classification.objects.all()
    paginator = Paginator(posters, 6)
    page = request.GET.get('page')
    try:
        posters = paginator.page(page)
    except PageNotAnInteger:
        posters = paginator.page(1)
    except EmptyPage:
        posters = paginator.page(paginator.num_page)
    context = {
        'form':form,
        'posters': posters,
        'regions': regions,
        'page': page,
        'num_poster': Poster.objects.filter().count(),
        'classifications': classifications,
        'title':'الاعلانات',
    }
    return render(request, 'hod_template/poster.html', context)



@login_required(login_url='doLogin')
def my_declaration(request,poster_id):
    adminhod=CustomUser.objects.get(id=poster_id)
    posters=adminhod.poster_set.all()
    regions = Region.objects.all()
    form = AddPosterForm()
    # posters=Poster.objects.order_by('-created_at')
    classifications= Classification.objects.all()
    paginator = Paginator(posters, 6)
    page = request.GET.get('page')
    try:
        posters = paginator.page(page)
    except PageNotAnInteger:
        posters = paginator.page(1)
    except EmptyPage:
        posters = paginator.page(paginator.num_page)
    context = {
        'form':form,
        'adminhod':adminhod,
        'posters': posters,
        'regions': regions,
        'page': page,
        'num_poster': Poster.objects.filter().count(),
        'classifications': classifications,
        'title':'الاعلانات',
    }
    return render(request, 'hod_template/my_poster.html', context)





@login_required(login_url='doLogin')
def save_poster(request):
    form = AddPosterForm()
    if request.method == 'POST':
        form = AddPosterForm(request.POST,request.FILES)
        # if form.is_valid():
        #     form.save()
        # poster_id=request.POST.get('id')
        region=Region.objects.get(id=request.POST.get('region',''))
            # classification=Classification.objects.get(id=request.POST.get('classification',''))
        poster = Poster(poster_image = request.FILES['poster_image'],name=request.POST.get('name',''),place=request.POST.get('place',''),posts=request.POST.get('posts',''),
                date_poster=request.POST.get('date_poster',''),region=region, classification=request.POST.get('classification',''),admin=request.user)
        poster.save()
        messages.success(request,"تم الاضافة بنجاح")
        return HttpResponseRedirect(reverse("poster"))
    else:
        form = AddPosterForm()
    context = {
        'form':form,
        'title':'اضافة اعلان',
        }
    return render(request, "hod_template/poster.html", context)
    





@login_required(login_url='doLogin')
def update_poster(request,poster_id):
    poster=Poster.objects.get(id=poster_id)
    form = AddPosterForm(instance=poster)
    if poster==None:
        return HttpResponse("Member Not Found")
    else:
        context = {
            'classifications': Classification.objects.all(),
            'regions': Region.objects.all(),
            'poster':poster,
            'form':form
        }
        return render(request,"hod_template/edit_poster.html", context)



@login_required(login_url='doLogin')
def edit_poster(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        poster=Poster.objects.get(id=request.POST.get('id',''))
        if poster==None:
            return HttpResponse("<h2>Poster Not Found</h2>")
        else:
            try:
                if request.FILES.get('poster_image')!=None:
                    file = request.FILES['poster_image']
                    fs = FileSystemStorage()
                    poster_img = fs.save(file.name, file)
                # else:
                #     poster_img=None
                if poster_img!=None:
                    poster.poster_image=poster_img
                poster.name=request.POST.get('name','')
                poster.place=request.POST.get('place','')
                poster.posts=request.POST.get('posts','')
                poster.date_poster=request.POST.get('date_poster','')
                poster.time_poster=request.POST.get('time_poster','')
                region=Region.objects.get(id=request.POST.get('region',''))
                poster.region=region
                poster.classification=request.POST.get('classification','')
                poster.save()
                messages.success(request,"تم التحديث بنجاح")
                return HttpResponseRedirect("/poster")
            except Exception as e:
                print(e)
                messages.error(request,"فشل في التعديل")
                return HttpResponseRedirect("/poster")
                



@login_required(login_url='doLogin')
def DeletePoster(request,poster_id):
    poster=Poster.objects.get(id=poster_id)
    poster.delete()
    messages.error(request, "تم الحذف بنجاح")
    return HttpResponseRedirect("/poster")



class SearchPosterEduResultsView(ListView):
    model = Poster
    template_name = 'hod_template/search_posterEdu_results.html'
    queryset = Poster.objects.filter(classification__icontains='تعليم')# new
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    def get_context_data(self, *args, **kwargs):
        try:
            return super(SearchPosterEduResultsView,self).get_context_data(*args,**kwargs)
        except Http404:
            self.kwargs['page'] =1
            return super(SearchPosterEduResultsView,self).get_context_data(*args,**kwargs)



class SearchPosterEnvResultsView(ListView):
    model = Poster
    template_name = 'hod_template/search_posterEnv_results.html'
    queryset = Poster.objects.filter(classification__icontains='بيئة') # new
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    def get_context_data(self, *args, **kwargs):
        try:
            return super(SearchPosterEnvResultsView,self).get_context_data(*args,**kwargs)
        except Http404:
            self.kwargs['page'] =1
            return super(SearchPosterEnvResultsView,self).get_context_data(*args,**kwargs)


class SearchPosterHeaResultsView(ListView):
    model = Poster
    template_name = 'hod_template/search_posterHea_results.html'
    queryset = Poster.objects.filter(classification__icontains='صحة') # new
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    def get_context_data(self, *args, **kwargs):
        try:
            return super(SearchPosterHeaResultsView,self).get_context_data(*args,**kwargs)
        except Http404:
            self.kwargs['page'] =1
            return super(SearchPosterHeaResultsView,self).get_context_data(*args,**kwargs)


class SearchPosterArtResultsView(ListView):
    model = Poster
    template_name = 'hod_template/search_posterArt_results.html'
    queryset = Poster.objects.filter(classification__icontains='فنون') # new
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    def get_context_data(self, *args, **kwargs):
        try:
            return super(SearchPosterArtResultsView,self).get_context_data(*args,**kwargs)
        except Http404:
            self.kwargs['page'] =1
            return super(SearchPosterArtResultsView,self).get_context_data(*args,**kwargs)


class SearchPosterOthResultsView(ListView):
    model = Poster
    template_name = 'hod_template/search_posterOth_results.html'
    queryset = Poster.objects.filter(classification__icontains='أخرى') # new
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    def get_context_data(self, *args, **kwargs):
        try:
            return super(SearchPosterOthResultsView,self).get_context_data(*args,**kwargs)
        except Http404:
            self.kwargs['page'] =1
            return super(SearchPosterOthResultsView,self).get_context_data(*args,**kwargs)




@login_required(login_url='doLogin')
def notification(request):
    # numvolunteers = NumVolunteer.objects.all()
    form = VolunteerForm()
    numvolunteers = NumVolunteer.objects.order_by('-created_at')
    paginator = Paginator(numvolunteers, 1)
    page = request.GET.get('page')
    try:
        numvolunteers = paginator.page(page)
    except PageNotAnInteger:
        numvolunteers = paginator.page(1)
    except EmptyPage:
        numvolunteers = paginator.page(paginator.num_page)
    context = {
        'num_volunteer':NumVolunteer.objects.filter().count(),
        'region': Region.objects.all(),
        'form': form,
        'numvolunteers': numvolunteers,
        'page': page,
        'title':'الاشعارات'
    }
    return render(request, 'hod_template/notification.html', context)




@login_required(login_url='doLogin')
def add_volunteer(request):
    form = VolunteerForm()
    if request.method == 'POST':
        form = VolunteerForm(request.POST,request.FILES)
        form.save()
        messages.success(request,"تم الاضافة بنجاح")
        return HttpResponseRedirect("/notification")
    else:
        form = VolunteerForm() 
    context = {
        'form':form,
        'title':'اضافة اشعار',
        }
    return render(request, "hod_template/add_volunteer.html", context)

 



@login_required(login_url='doLogin')
def delete_volunteer(request,notification_id):
    notification=NumVolunteer.objects.get(id=notification_id)
    notification.delete()
    messages.error(request, "تم الحذف بنجاح")
    return HttpResponseRedirect("/notification")



@login_required(login_url='doLogin')
def comments(request):
    comments=Comment.objects.order_by('-created_at')
    comments_user = Comment_User.objects.order_by('-created_at')
    customuser = CustomUser.objects.all()
    paginator = Paginator(comments, 4)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_page)
    context = {
        'customuser':customuser,
        'comments' : comments,
        'comments_user' : comments_user,
        'num_com': Comment.objects.filter().count() + Comment_User.objects.filter().count(),
        'page': page,
        'title':'التعليقات',
    }
    return render(request, 'hod_template/comments.html', context)








@login_required(login_url='doLogin')
def Add_Comment_Save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        try:
            intity = Intity.objects.all()
            people = People.objects.all()
            com = Comment(comm_name=request.POST.get('comm_name',''),author=request.user,body=request.POST.get('body',''), comment_pic=request.user.intity)
            com.save()
            messages.success(request,"تم الاضافة بنجاح")
            return redirect("/comments")
        except Exception as e:
            print(e)
            messages.error(request,"لم يتم الاضافة ")
            return redirect("/comments")



@login_required(login_url='doLogin')
def LikeView(request,pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    comment.likes.add(request.user)
    return HttpResponseRedirect(reverse('comments'))


@login_required(login_url='doLogin')
def LikeViewUser(request,pk):
    comment= get_object_or_404(Comment_User, id=request.POST.get('comment_user_id'))
    comment.likes.add(request.user)
    return HttpResponseRedirect(reverse('comments'))


@login_required(login_url='doLogin')
def delete_comment(request,comment_id):
    comment=Comment.objects.get(id=comment_id)
    comment.delete()
    messages.error(request, "تم الحذف بنجاح")
    return HttpResponseRedirect("/comments")


@login_required(login_url='doLogin')
def delete_comment_user(request,comment_user_id):
    comment=Comment_User.objects.get(id=comment_user_id)
    comment.delete()
    messages.error(request, "تم الحذف بنجاح")
    return HttpResponseRedirect("/comments")




@login_required(login_url='doLogin')
def about(request):
    context = {
    'title':'من نحن',
    }
    return render(request, 'hod_template/about.html', context)






