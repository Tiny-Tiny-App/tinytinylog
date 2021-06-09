from django import forms
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field
from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from .models import Collection


class CreateCollectionForm(forms.ModelForm):
    icon = '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
  <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z"/>
</svg>'''

    error_messages = {
        'collection_exists': _('Collection with that name already exists. Please try another one.'),
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('initial').get('user')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_id = 'createCollectionForm'
        self.helper.layout = Layout(
            Div(
                FieldWithButtons(
                    Field(
                        'name',
                        placeholder='New collection name'
                    ),
                    StrictButton(
                        self.icon,
                        css_class='btn-primary',
                        type='submit',
                        hx_post=reverse_lazy('log_collections'),
                        hx_swap='outerHTML',
                        hx_target='#collections'
                    ),
                ), 
            )
        )

    class Meta:
        model = Collection
        fields = ['name']

    def clean_name(self):
        collection = Collection.objects.filter(
            name=self.cleaned_data.get('name'),
            user=self.user)
        
        if collection:
            raise ValidationError(
                self.error_messages['collection_exists'],
                code='collection_exists'
            )
            
        return self.cleaned_data.get('name')

    def save(self, commit=True):
        # todo: need to add messages support
        instance = super().save(commit=False)

        collection = Collection.objects.filter(
            name=self.cleaned_data.get('name'),
            user=self.user).first()
        
        # todo: allow people to delete collection
        # and remove he ability to archive.
        # show previosly archived version under same name
        if collection and collection.archived:
            collection.archived = False
            collection.save()
            return collection

        elif collection:
            return collection

        instance.name = self.cleaned_data.get('name')
        instance.slug = slugify(self.cleaned_data.get('name'))
        instance.user = self.user
        instance.save()
        return instance