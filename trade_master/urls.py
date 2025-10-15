from django.urls import  re_path,path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
app_name = 'trade_master'

from . import views
from .views import AddCategoryTicket, DeleteSupportCategory, ListSupportCategory, UpdateCategoryTicket, UpdateCms_StaticContent,Liststaticcontent,DetailStaticcontent, UserRequestManagement
from .views import UpdateCms_Content,Listcontent,Detailcontent
from .views import ListFaq,AddFaq,UpdateFaq,Detailfaq
from .views import Listcontactus,UpdateContactus,Detailcontactus
from .views import Listemailcontent,Updateemailcontent
from .views import UpdateRoadmap,ListRoadmap,AddRoadmap,DetailRoadmap
from .views import Updatecurrency,ListCurrencyDetails,Detailcurrency

loginurl='/RZqYkZRuiBaffkx/'

urlpatterns = [

	
	 re_path(r'^cms_page/(?P<pk>[-\w]+)/$', login_required(UpdateCms_StaticContent.as_view(),login_url=loginurl), name='cms_page'),
	 re_path(r'^cmspagelist/$', login_required(Liststaticcontent.as_view(),login_url=loginurl), name='cmspagelist'),
	 re_path(r'^cms_page_detail/(?P<pk>[-\w]+)/$', login_required(DetailStaticcontent.as_view(),login_url=loginurl), name='cms_page_detail'),

	 re_path(r'^cms_content/(?P<pk>[-\w]+)/$', login_required(UpdateCms_Content.as_view(),login_url=loginurl), name='cms_content'),
	 re_path(r'^cmspagecontentlist/$', login_required(Listcontent.as_view(),login_url=loginurl), name='cmspagecontentlist'),
	 re_path(r'^cms_page_contentdetail/(?P<pk>[-\w]+)/$', login_required(Detailcontent.as_view(),login_url=loginurl), name='cms_page_contentdetail'),


	 re_path(r'^updatefaq/(?P<pk>[-\w]+)/$', login_required(UpdateFaq.as_view(),login_url=loginurl), name='updatefaq'),
	 re_path(r'^faqlist/$', login_required(ListFaq.as_view(),login_url=loginurl), name='faqlist'),
	 re_path(r'^addfaq/$', login_required(AddFaq.as_view(),login_url=loginurl), name='addfaq'),
	 re_path(r'^detail_faq/(?P<pk>[-\w]+)/$', login_required(Detailfaq.as_view(),login_url=loginurl), name='detail_faq'),

	 re_path(r'^updateroadmap/(?P<pk>[-\w]+)/$', login_required(UpdateRoadmap.as_view(),login_url=loginurl), name='updateroadmap'),
	 re_path(r'^roadmaplist/$', login_required(ListRoadmap.as_view(),login_url=loginurl), name='roadmaplist'),
	 re_path(r'^addroadmap/$', login_required(AddRoadmap.as_view(),login_url=loginurl), name='addroadmap'),
	 re_path(r'^roadmapdetail/(?P<pk>[-\w]+)/$', login_required(DetailRoadmap.as_view(),login_url=loginurl), name='roadmapdetail'),

	 re_path(r'^contactus_update/(?P<pk>[-\w]+)/$', login_required(UpdateContactus.as_view(),login_url=loginurl), name='contactus_update'),
	 re_path(r'^contactlist/$', login_required(Listcontactus.as_view(),login_url=loginurl), name='contactlist'),
	 re_path(r'^contactusdetail/(?P<pk>[-\w]+)/$', login_required(Detailcontactus.as_view(),login_url=loginurl), name='contactusdetail'),

	 re_path(r'^emailcontent_update/(?P<pk>[-\w]+)/$', login_required(Updateemailcontent.as_view(),login_url=loginurl), name='emailcontent_update'),
	 re_path(r'^emailcontactlist/$', login_required(Listemailcontent.as_view(),login_url=loginurl), name='emailcontactlist'),

	 re_path(r'^updatecurrency/(?P<pk>[-\w]+)/$', login_required(Updatecurrency.as_view(),login_url=loginurl), name='updatecurrency'),
	 re_path(r'^currencydetail/(?P<pk>[-\w]+)/$', login_required(Detailcurrency.as_view(),login_url=loginurl), name='currencydetail'),
	 re_path(r'^currencylist/$', login_required(ListCurrencyDetails.as_view(),login_url=loginurl), name='currencylist'),

	 re_path('read_dir_log', views.read_dir_log, name='read_dir_log'),
	 re_path('read_log', views.read_log, name='read_log'),
	 re_path('delete_log', views.delete_log, name='delete_log'),


	#  Support category urls

	 re_path(r'^updatesupportcategory/(?P<pk>[-\w]+)/$', login_required(UpdateCategoryTicket.as_view(),login_url=loginurl), name='updatesupportcategory'),
	 re_path(r'^supportcategorylist/$', login_required(ListSupportCategory.as_view(),login_url=loginurl), name='supportcategorylist'),
	 re_path(r'^addsupportcategory/$', login_required(AddCategoryTicket.as_view(),login_url=loginurl), name='addsupportcategory'),
	 re_path(r'^delete_support_category/(?P<pk>[-\w]+)/$', login_required(DeleteSupportCategory.as_view(),login_url=loginurl), name='delete_support_category'),

	 path('User_request_list/', login_required(UserRequestManagement.as_view(),login_url=loginurl), name='User_request_list'),
	 path('update_user_request/<int:id>/', login_required(views.UpdateUserRequest), name='update_user_request'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)