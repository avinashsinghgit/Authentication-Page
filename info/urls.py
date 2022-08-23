from django.contrib import admin
from django.urls import path
from info import views

# For Password Reset
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name="Home"),
    path('signup', views.signup, name="SignUp"),
    path('signin', views.signin, name="SignIn"),
    path('signout', views.signout, name="SignOut"),

    # Password Reset Form

    path('password_reset/', views.password_reset, name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView .as_view(template_name='password_reset_complete.html'), name="password_reset_complete")

]


'''

1. Submit Email form                                      // PasswordResetView.as_view()                  name="password_reset"
2. Email Sent Success message                             // PasswordResetDoneView.as_view()              name="password_reset_done"
3. Link to Password Reset Email Form                      // PasswordResetConfirmView.as_view()           name="password_reset_confirm"
4. Password Successfully Changed message                  // PasswordResetConfirmView.as_view()           name="password_reset_complete"

'''
