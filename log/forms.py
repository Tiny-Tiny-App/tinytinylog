from django import forms
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div
from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from .models import Collection


class CreateCollectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('initial').get('user')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'createCollectionForm'
        self.attrs = {} # pass htmx data attrs here
        self.helper.layout = Layout(
            Div(
                FieldWithButtons('name', StrictButton('''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
  <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z"/>
</svg>''', css_class='btn-primary', type='submit', hx_post=reverse_lazy('log_collections'), hx_swap='outerHTML', hx_target='#collections')),
            )
        )

    class Meta:
        model = Collection
        fields = ['name']

    def save(self, commit=True):
        # todo: need to add messages support
        instance = super().save(commit=False)

        collection = Collection.objects.filter(
            name=self.cleaned_data.get('name'),
            user=self.user).first()
        
        # show previosly archived version under same name
        if collection and collection.archived:
            collection.archived = False
            collection.save()
            return collection
        
        elif collection:
            return collection

        instance.name = self.cleaned_data.get('name')
        instance.user = user

        if commit:
            instance.save()

        return instance