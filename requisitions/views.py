from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from .models import Requisition
from .forms import RequisitionForm, ShareRequisitionForm

class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class RequisitionListView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            requisitions = Requisition.objects.all()
        else:
            requisitions = Requisition.objects.filter(requester=request.user) | request.user.shared_requisitions.all()
        return render(request, 'requisition_list.html', {'requisitions': requisitions})

class RequisitionCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = RequisitionForm()
        return render(request, 'requisition_form.html', {'form': form})

    def post(self, request):
        form = RequisitionForm(request.POST)
        if form.is_valid():
            requisition = form.save(commit=False)
            requisition.requester = request.user
            requisition.save()
            return redirect('requisition_list')
        return render(request, 'requisition_form.html', {'form': form})

class RequisitionDetailView(LoginRequiredMixin, View):
    def get(self, request, requisition_id):
        requisition = get_object_or_404(Requisition, pk=requisition_id)
        if requisition.requester == request.user or request.user in requisition.shared_with.all() or request.user.is_superuser:
            return render(request, 'requisition_detail.html', {'requisition': requisition})
        else:
            return render(request, 'unauthorized.html')

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from .models import Requisition
from .forms import ShareRequisitionForm

class RequisitionShareView(LoginRequiredMixin, View):
    def get(self, request, requisition_id):
        requisition = get_object_or_404(Requisition, pk=requisition_id)
        
        # Vérifier si l'utilisateur a le droit de partager cette réquisition
        if requisition.requester != request.user:
            return render(request, 'unauthorized.html')  # Rediriger si l'utilisateur n'est pas le propriétaire

        form = ShareRequisitionForm(initial={'users': requisition.shared_with.all()})  # Pré-remplir avec les utilisateurs déjà partagés
        return render(request, 'share_requisition.html', {'form': form, 'requisition': requisition})

    def post(self, request, requisition_id):
        requisition = get_object_or_404(Requisition, pk=requisition_id)
        
        # Vérifier à nouveau l'autorisation (au cas où l'URL serait manipulée)
        if requisition.requester != request.user:
            return render(request, 'unauthorized.html')

        form = ShareRequisitionForm(request.POST)
        if form.is_valid():
            requisition.shared_with.set(form.cleaned_data['users'])  # Mettre à jour les utilisateurs partagés
            return redirect('requisition_detail', pk=requisition.pk)  # Rediriger vers la page de détails
        
        return render(request, 'share_requisition.html', {'form': form, 'requisition': requisition})


class AdminDashboardView(IsAdminMixin, RequisitionListView):
    template_name = 'admin_dashboard.html'  # Utiliser un template spécifique pour l'admin
