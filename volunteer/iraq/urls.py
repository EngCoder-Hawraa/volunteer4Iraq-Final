from django.urls import path
from . import views, IntitiesViews ,UserViews
from volunteer import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authviews
from .IntitiesViews import intities, LikeViewUser,SearchIntitiesResultsView,SearchPosterEduResultsView,SearchPosterEnvResultsView,SearchPosterHeaResultsView,SearchPosterArtResultsView,SearchPosterOthResultsView,LikeView
from .UserViews import SearchIntitiesResultsView1,SearchPosterEduResultsView1,SearchPosterEnvResultsView1,SearchPosterHeaResultsView1,SearchPosterArtResultsView1,SearchPosterOthResultsView1,LikeView1,LikeViewUser1
# from django.contrib.auth.views import LogoutView

# # from .IntitiesViews import IntitiesCreateView,IntitiesUpdateView

urlpatterns = [

# url Path For Intities
    path('dashboard/', IntitiesViews.dashboard, name='dashboard'),
    path('admin_home',IntitiesViews.admin_home,name="admin_home"),
    path('details1/', IntitiesViews.details, name='details1'),
    
    path('profile_intities/', IntitiesViews.profile_intities,name="profile_intities"),
    path('update_intities/<str:intity_id>',IntitiesViews.update_intities,name='update_intities'),
    path('intities1/', IntitiesViews.intities, name='intities1'),
    path('search_Intities/', SearchIntitiesResultsView.as_view(), name='search_Intities_results'),
    path('delete_intities/<str:intity_id>',IntitiesViews.delete_intities,name='delete_intities'),
    path('view_imageP/', IntitiesViews.view_image, name='view_imageP'),
    path('more_read_intities/<str:intity_id>/', IntitiesViews.more_read_intities, name='more_read_intities'),
    
    path('manage_members/<str:member_id>',IntitiesViews.manage_members,name="manage_members"),
    path('add_member_save',IntitiesViews.add_member_save,name="add_member_save"),
    path('update_member/<str:member_id>' , IntitiesViews.update_member, name='update_member'),
    path('edit_member' , IntitiesViews.edit_member, name='edit_member'),
    path('delete_member/<str:member_id>' , IntitiesViews.delete_member, name='delete_member'),
    path('deletes' , IntitiesViews.deletes, name='deletes'),
    
    path('poster/', IntitiesViews.declaration, name='poster'),
    path('my_poster/<str:poster_id>', IntitiesViews.my_declaration, name='my_poster'),
    path('save_poster', IntitiesViews.save_poster, name='save_poster'),
    path('delete_poster/<str:poster_id>', IntitiesViews.DeletePoster, name='delete_poster'),
    path('update_poster/<str:poster_id>', IntitiesViews.update_poster, name='update_poster'),
    path('edit_poster' , IntitiesViews.edit_poster, name='edit_poster'),
    path('search_PosterEdu_results/', SearchPosterEduResultsView.as_view(), name='search_PosterEdu_results'),
    path('search_PosterEnv_results/', SearchPosterEnvResultsView.as_view(), name='search_PosterEnv_results'),
    path('search_PosterHea_results/', SearchPosterHeaResultsView.as_view(), name='search_PosterHea_results'),
    path('search_PosterArt_results/', SearchPosterArtResultsView.as_view(), name='search_PosterArt_results'),
    path('search_PosterOth_results/', SearchPosterOthResultsView.as_view(), name='search_PosterOth_results'),
    
    path('notification/', IntitiesViews.notification, name='notification'),
    path('add_volunteer', IntitiesViews.add_volunteer, name='add_volunteer'),
    path('delete_volunteer/<str:notification_id>', IntitiesViews.delete_volunteer, name='delete_volunteer'),
  
    path('comments/',IntitiesViews.comments, name='comments'),
    path('like/<int:pk>',LikeView,name='like_comment'),
    path('like_user/<int:pk>',LikeViewUser,name='like_comment_user'),
    path('add_comment_save', IntitiesViews.Add_Comment_Save , name='add_comment_save'),
    path('delete_comment/<str:comment_id>' ,IntitiesViews.delete_comment, name='delete_comment'),
    path('delete_comment_user/<str:comment_user_id>' ,IntitiesViews.delete_comment_user, name='delete_comment_user'),
  
    path('about1/', IntitiesViews.about, name='about1'),
  
   
    









# # url Path For user
    path('user_home',UserViews.user_home,name="user_home"),
    path('profile1',UserViews.profile,name="profile1"),
    path('profile_update/<str:people_id>', UserViews.profile_update, name='profile_update'),
    # path('profile_edit_user', UserViews.ProfileEdit1, name='profile_edit_user'),
    path('details2/', UserViews.details2, name='details2'),
    
    path('intities2/', UserViews.intities2, name='intities2'),
    path('more_read_intities1/<str:intity_id>', UserViews.more_read_intities1, name='more_read_intities1'),
    path('search_Intities1/', SearchIntitiesResultsView1.as_view(), name='search_Intities_results1'),

    path('poster1/', UserViews.declaration1, name='poster1'),
    path('search_PosterEdu_results1/', SearchPosterEduResultsView1.as_view(), name='search_PosterEdu_results1'),
    path('search_PosterEnv_results1/', SearchPosterEnvResultsView1.as_view(), name='search_PosterEnv_results1'),
    path('search_PosterHea_results1/', SearchPosterHeaResultsView1.as_view(), name='search_PosterHea_results1'),
    path('search_PosterArt_results1/', SearchPosterArtResultsView1.as_view(), name='search_PosterArt_results1'),
    path('search_PosterOth_results1/', SearchPosterOthResultsView1.as_view(), name='search_PosterOth_results1'),

    path('add_notification/', UserViews.add_notification, name='add_notification'),
    path('send_notification', UserViews.send_notification, name='send_notification'),
   
    path('comments1/',UserViews.comments1, name='comments1'),
    path('like1/<int:pk>',LikeView1,name='like_comment1'),
    path('like_user1/<int:pk>',LikeViewUser1,name='like_comment_user1'),
    path('add_comment_save1', UserViews.add_commentsave_user , name='add_comment_save1'),
    path('delete_comment_user1/<str:comment_user_id>' ,UserViews.delete_comment_user1, name='delete_comment_user1'),
   
    path('about2/', UserViews.about2, name='about2'),    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


