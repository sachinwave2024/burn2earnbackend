# """jason_wellness URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/2.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), ye='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path,include,re_path
# from django.conf import settings
# from django.conf.urls.static import static
# from API import views


# from trade_admin_auth.views import adminlogin, adminloginn



# urlpatterns = [
#     # path('ZMXTAJ57tfxuIRDREf/', admin.site.urls),
#     path('/RZqYkZRuiBaffkx/', admin.site.urls),
#     re_path(r'^tradeadmin/',include("trade_admin_auth.urls" ,namespace="trade_admin_auth")),
#     re_path(r'^trademaster/',include("trade_master.urls" ,namespace="trade_master")),
#     re_path(r'^tradecurrency/',include("trade_currency.urls" ,namespace="trade_currency")),
#     re_path(r'^tradeauth/',include("trade_auth.urls" ,namespace="trade_auth")),
#     re_path('',include("API.urls" ,namespace="API")),
#     re_path(r'^stake/',include("Staking.urls" ,namespace="stake")),
    
    
    


# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""jason_wellness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), ye='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static


from trade_admin_auth.views import adminlogin, adminloginn



urlpatterns = [
    # path('ZMXTAJ57tfxuIRDREf/', admin.site.urls),
    
    re_path(r'^tradeadmin/',include("trade_admin_auth.urls" ,namespace="trade_admin_auth")),
    re_path(r'^trademaster/',include("trade_master.urls" ,namespace="trade_master")),
    re_path(r'^tradecurrency/',include("trade_currency.urls" ,namespace="trade_currency")),
    re_path(r'^tradeauth/',include("trade_auth.urls" ,namespace="trade_auth")),
    re_path('',include("API.urls" ,namespace="API")),
    re_path(r'^stake/',include("Staking.urls" ,namespace="stake")),
    path('RZqYkZRuiBaffkx/<int:id>/', adminloginn, name='adminloginn'),
    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)