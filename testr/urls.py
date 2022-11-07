from django.urls import include, path

from . import views

urlpatterns = [
    # user management
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup', views.signup_form, name="signup"),

    # main pages
    path('', views.index, name='index'),

    # courses management
    path('courses/', views.CourseListView.as_view(), name="courses"),
    path('course/<int:pk>', views.CourseDetailView.as_view(), name="course-detail"),
    path('course/create/', views.CourseCreate.as_view(), name="course-create"),
    path('course/<int:pk>/update/',
         views.CourseUpdate.as_view(), name='course-update'),
    path('course/<int:pk>/delete/',
         views.CourseDelete.as_view(), name='course-delete'),
    path('course/<int:pk>/toogle_visibility/',
         views.course_toogle_visibility, name='course-toogle-visibility'),

    # section management
    path('course/<int:course_id>/section/create/',
         views.SectionCreate.as_view(), name="section-create"),
    path('section/<int:pk>/update/',
         views.SectionUpdate.as_view(), name='section-update'),
    path('section/<int:pk>/delete/',
         views.SectionDelete.as_view(), name='section-delete'),
    path('section/<int:pk>/toogle_visibility/',
         views.section_toogle_visibility, name='section-toogle-visibility'),

    # question management
    path('section/<int:section_id>/question/create/',
         views.question_create, name="question-create"),
    path('question/<int:pk>/update/',
         views.QuestionUpdate.as_view(), name='question-update'),
    path('question/<int:pk>/delete/',
         views.QuestionDelete.as_view(), name='question-delete'),
    path('question/<int:pk>',
         views.QuestionDetailView.as_view(), name="question-detail"),
    path('question/<int:pk>/toogle_visibility/',
         views.question_toogle_visibility, name="question-toogle-visibility"),
    path('question/<int:pk>/report',
         views.question_report, name="question-report"),

    # course enrollment
    path('course/<int:course_id>/enroll/<uuid:enroll_password>',
         views.enroll_course, name="enroll-course"),
    path('course/<int:course_id>/unenroll/',
         views.unenroll_course, name='unenroll-course'),
    path('course/<int:course_id>/batch-enroll/',
         views.course_batch_enroll, name='course-batch-enroll'),

    # submission
    path('question/<int:question_id>/submission',
         views.perform_question_submission, name="question-submission"),
    path('submission/<int:pk>/',
         views.SubmissionDetailView.as_view(), name="submission-detail"),
    path('question/<int:pk>/rejudge',
         views.question_rejudge, name="question-rejudge"),
    path('question/<int:pk>/rejudge_all',
         views.question_rejudge_all, name="question-rejudge-all"),
    path('submission/<int:pk>/file',
         views.submission_get_file, name="submission-file"),

    # input/output tests management
    path('question/<int:question_id>/in_out/create',
         views.question_create_input_output_test,
         name="question-create-in_out-test"),
    path('in_out_test/<int:pk>/update',
         views.input_output_test_update,
         name="in_out-test-update"),
    path('in_out_test/<int:pk>/delete',
         views.input_output_test_delete,
         name="in_out-test-delete"),
    path('in_out_test/<int:pk>/toogle_visibility/',
         views.input_output_test_toogle_visibility,
         name="in_out-test-toogle-visibility"),
]
