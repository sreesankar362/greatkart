from django.urls import path
from accounts import views

urlpatterns=[
    path('register',views.register,name="register"),
    path('login',views.login,name="login"),
    path('logout',views.user_logout,name="logout"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('',views.dashboard,name="dashboard"),
    path('forgotPassword',views.forgotPassword,name="forgotPassword"),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name="resetpassword_validate"),
    path('resetPassword',views.resetPassword,name="resetPassword"),
   

]

    #  path('login',views.SignInView.as_view(),name="login"),
     # path('activate/<uidb64>/<token>/',views.activate,name="activate")