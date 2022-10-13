from django.urls import include, path

from . import views

urlpatterns = [
    # user management
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup', views.signup_form, name="signup"),
    # main pages
    path('', views.index, name='index'),
    #path('student/', views.student_index, name="student"),
    #path('teacher/', views.teacher_index, name="teacher"),
    # courses management
    path('courses/', views.CourseListView.as_view(), name="courses"),
    path('course/<int:pk>', views.CourseDetailView.as_view(), name="course-detail"),
    path('course/create/', views.CourseCreate.as_view(), name="course-create"),
    path('course/<int:pk>/update/',
         views.CourseUpdate.as_view(), name='course-update'),
    path('author/<int:pk>/delete/',
         views.CourseDelete.as_view(), name='course-delete'),

]
