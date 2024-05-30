from django.urls import path
from .views import RequisitionListView, RequisitionCreateView, RequisitionDetailView, RequisitionShareView, AdminDashboardView

urlpatterns = [
    path('', RequisitionListView.as_view(), name='requisition_list'),
    path('create/', RequisitionCreateView.as_view(), name='requisition_create'),
    path('<int:requisition_id>/', RequisitionDetailView.as_view(), name='requisition_detail'),
    path('<int:requisition_id>/share/', RequisitionShareView.as_view(), name='requisition_share'),
    path('admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
]
