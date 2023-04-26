from django.urls import path

from my_ai.views import save_answer, delete_project, createProductDescription, create_product_copy, templates_View, \
    remove_not_committed_answer, productProjectListView, ProjectUpdateView, check_user_description, \
    delete_blank_projects

urlpatterns = [
    path('create_product_copy/', create_product_copy, name='create_product_copy'),
    path('save/', save_answer, name='save-answer'),
    path('project/<int:pk>/', ProjectUpdateView.as_view(), name='update-project'),
    path('delete<int:pk>/', delete_project, name='delete-project'),
    path('all_project/', productProjectListView, name='projects-list'),
    path('delete_blank_projects/', delete_blank_projects, name='delete_blank_projects'),
]

htmx_urlpatterns = [
    path('createProductDescription/', createProductDescription, name='createProductDescription'),
    path('all_templates/', templates_View, name="templates_View"),
    path('remove_not_commited_answer/', remove_not_committed_answer, name="remove_not_committed_answer"),
    path('check_user_description/', check_user_description, name="check_user_description"),
]
urlpatterns += htmx_urlpatterns
