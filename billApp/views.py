from bootstrap_datepicker_plus import DatePickerInput
from django.shortcuts import render, get_object_or_404
from billApp.models import Facture, LigneFacture, Client, Fournisseur
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
import django_tables2 as tables
from django_tables2.config import RequestConfig
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Button
from django.urls import reverse


# Create your views here.

def facture_detail_view(request, pk):
    facture = get_object_or_404(Facture, id=pk)
    context = {}
    context['facture'] = facture
    return render(request, 'bill/facture_detail.html', context)


class FactureUpdate(UpdateView):
    model = Facture
    fields = ['client', 'date']
    template_name = 'bill/update.html'


class LigneFactureTable(tables.Table):
    action = '<a href="{% url "lignefacture_update" pk=record.id facture_pk=record.facture.id %}" class="btn btn-warning">Modifier</a>\
            <a href="{% url "lignefacture_delete" pk=record.id facture_pk=record.facture.id %}" class="btn btn-danger">Supprimer</a>'
    edit = tables.TemplateColumn(action)

    class Meta:
        model = LigneFacture
        template_name = "django_tables2/bootstrap4.html"
        fields = ('produit__designation', 'produit__id', 'produit__prix', 'qte')


class FactureDetailView(DetailView):
    template_name = 'bill/facture_table_detail.html'
    model = Facture

    def get_context_data(self, **kwargs):
        context = super(FactureDetailView, self).get_context_data(**kwargs)

        table = LigneFactureTable(LigneFacture.objects.filter(facture=self.kwargs.get('pk')))
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
        context['table'] = table
        return context


class LigneFactureCreateView(CreateView):
    model = LigneFacture
    template_name = 'bill/create.html'
    fields = ['facture', 'produit', 'qte']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture'] = forms.ModelChoiceField(
            queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk': self.kwargs.get('facture_pk')})
        return form


class LigneFactureUpdateView(UpdateView):
    model = LigneFacture
    template_name = 'bill/update.html'
    fields = ['facture', 'produit', 'qte']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture'] = forms.ModelChoiceField(
            queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk': self.kwargs.get('facture_pk')})
        return form


class LigneFactureDeleteView(DeleteView):
    model = LigneFacture
    template_name = 'bill/delete.html'

    def get_success_url(self):
         return reverse('facture_table_detail', kwargs={'pk': self.kwargs.get('facture_pk')})


class ClientTable(tables.Table):
    action = '<a href="{% url "client_update" pk=record.id %}" class="btn btn-warning">Modifier</a>\
            <a href="{% url "client_delete" pk=record.id %}" class="btn btn-danger">Supprimer</a>\
             <a href="{% url "client_facture_list" pk=record.id %}" class="btn btn-primary">Lister</a>'

    edit = tables.TemplateColumn(action)
    chiffre_affaire = tables.Column(accessor='get_chiffre', verbose_name="Chiffre d'affaire")

    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap4.html"
        fields = ('nom', 'prenom', 'adresse', 'tel', 'sexe', "chiffre_affaire")


class ClientDetailView(TemplateView):
    template_name = 'bill/client_table_detail.html'
    model = Client

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)

        table = ClientTable(Client.objects.all())
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
        context['table'] = table
        return context


class ClientCreateView(CreateView):
    model = Client
    template_name = 'bill/create_client.html'
    fields = "__all__"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()


        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('client_table_detail')
        return form


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'bill/update_client.html'
    fields = ('nom', 'prenom', 'adresse', 'tel', 'sexe')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()


        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('client_table_detail')
        return form


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'bill/delete_client.html'

    def get_success_url(self):
        return reverse('client_table_detail')


class ClientFactureTable(tables.Table):
    total = tables.Column(accessor='get_total', verbose_name="Total")

    class Meta:
        model = Facture
        template_name = "django_tables2/bootstrap4.html"
        fields = ("pk", "date", "client", "total")


class ClientFactureList(TemplateView):
    template_name = 'bill/client_facture_list.html'
    model = Facture

    def get_context_data(self, **kwargs):
        context = super(ClientFactureList, self).get_context_data(**kwargs)

        list_facture = Facture.objects.filter(client=self.kwargs.get('pk'))
        table = ClientFactureTable(list_facture)
        print(list_facture)
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
        context['table'] = table
        return context


class FactureCreateView(CreateView):
    model = Facture
    template_name = 'bill/create_facture.html'
    fields =['client', 'date']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['client'] = forms.ModelChoiceField(
            queryset=Client.objects.filter(id=self.kwargs.get('client_pk')), initial=0)

        form.fields['date'] = forms.DateField(
            widget=DatePickerInput(format='%m/%d/%Y')
        )

        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('client_facture_list', kwargs={'pk': self.kwargs.get('client_pk')})
        return form


class FournisseurTable(tables.Table):
    action = '<a href="{% url "fournisseur_update" pk=record.id %}" class="btn btn-warning">Modifier</a>\
            <a href="{% url "fournisseur_delete" pk=record.id %}" class="btn btn-danger">Supprimer</a>'

    edit = tables.TemplateColumn(action)

    class Meta:
        model = Fournisseur
        template_name = "django_tables2/bootstrap4.html"
        fields = ('nom', 'prenom', 'adresse', 'tel')


class FournisseurDetailView(TemplateView):
    template_name = 'bill/fournisseur_table_detail.html'
    model = Fournisseur

    def get_context_data(self, **kwargs):
        context = super(FournisseurDetailView, self).get_context_data(**kwargs)

        table = FournisseurTable(Fournisseur.objects.all())
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
        context['table'] = table
        return context


class FournisseurUpdateView(UpdateView):
    model = Fournisseur
    template_name = 'bill/update_client.html'
    fields = ('nom', 'prenom', 'adresse', 'tel')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('fournisseur_table_detail')
        return form


class FournisseurDeleteView(DeleteView):
    model = Fournisseur
    template_name = 'bill/delete_client.html'

    def get_success_url(self):
        return reverse('fournisseur_table_detail')


class FournisseurCreateView(CreateView):
    model = Fournisseur
    template_name = 'bill/create_fournisseur.html'
    fields = "__all__"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('fournisseur_table_detail')
        return form

def Dashboard(request):
    return render(request, "bill/dashboard.html", {})