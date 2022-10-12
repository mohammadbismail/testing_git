from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_page),
    path("add_user/", views.add_user),
    path("login_user/", views.login_user),
    path("logout/", views.logout),
    path("dashboard_page/", views.dashboard_page),
    path("add_tree_page/",views.add_tree_page),
    path("plant_tree/",views.plant_tree),
    path("show/<int:tree_id>/", views.show_tree),
    path("user/account/", views.show_all_trees),
    path("delete/", views.delete_tree),
    path("edit/<int:tree_id>/", views.edit_tree),
    path("update/<int:tree_id>/", views.update_tree),
]
