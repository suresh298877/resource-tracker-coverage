from django.urls import path
from . import views
urlpatterns = [
    path('', views.uploadDAta, name="upload-data"),
    path('export-to-excel/', views.exportToExcel, name="export-to-excel"),
    path('records/', views.records, name="records"),
    path("delete-record/<int:pk>/", views.deleteRecord, name="deleteRecord"),
    path("edit-record/<int:pk>/", views.editRecord, name="editRecord"),
]
