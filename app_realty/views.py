from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import House, HouseFoto
from .forms import FotoForm


class HouseList(generic.ListView):

    queryset = House.objects.filter(actual=True).select_related('rooms').prefetch_related('foto')
    template_name = 'app_realty/main.html'


class MyHouseList(LoginRequiredMixin, generic.ListView):

    template_name = 'app_realty/my_house.html'

    def get_queryset(self):
        queryset = House.objects.filter(owner=self.request.user).select_related('rooms').prefetch_related('foto')
        return queryset


class HouseDetail(generic.DetailView):

    queryset = House.objects.filter(actual=True).select_related().prefetch_related('foto')
    template_name = 'app_realty/house_detail.html'


class HouseEditCreateMixin:

    model = House
    fields = ['title', 'type', 'rooms', 'description', 'price', 'actual']

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['foto_form'] = FotoForm()
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        files = self.request.FILES.getlist('files')
        with transaction.atomic():
            self.object = form.save()
            if files:
                img_lst = [HouseFoto(house=self.object, foto=file) for file in files]
                HouseFoto.objects.bulk_create(img_lst)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('my_house')


class HouseCreate(LoginRequiredMixin, HouseEditCreateMixin, generic.CreateView):

    template_name = 'app_realty/house_create.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class HouseEdit(LoginRequiredMixin, HouseEditCreateMixin, generic.UpdateView):

    template_name = 'app_realty/house_edit.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        owner = get_object_or_404(House, id=kwargs['pk']).owner
        if owner != request.user:
            return HttpResponseForbidden(request)
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class HouseFotoDelete(LoginRequiredMixin, generic.DeleteView):

    model = HouseFoto
    template_name = 'app_realty/delete_foto.html'

    def get_object(self):
        foto = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        if foto.house.owner != self.request.user:
            raise PermissionDenied
        return foto

    def get_success_url(self):
        return reverse('house_edit', args=[self.object.house.id])


class HouseDelete(LoginRequiredMixin, generic.DeleteView):

    model = House
    template_name = 'app_realty/house_delete.html'

    def get_object(self):
        house = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        if house.owner != self.request.user:
            raise PermissionDenied
        return house

    def get_success_url(self):
        return reverse('my_house')
