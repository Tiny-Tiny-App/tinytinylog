from django import forms
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from .models import Collection, Item


PLUS_CIRCLE_ICON = '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
  <title>Save</title>
  <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0
  1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z"/>
</svg>'''

CHECKMARK_ICON = '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
fill="currentColor" class="bi bi-check-circle" viewBox="0 0 16 16">
  <title>Update</title>
  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
  <path d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06
  1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z"/>
</svg>
'''

ERROR_MESSAGES = {
    'collection_exists': _('Collection with that name already exists. Please try another one.'),
    'item_exists': _('Item with that name already exists. Please try another one.'),
    'name_required': _('Name required. Please provide one')
}


class CreateCollectionForm(forms.ModelForm):

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
                        placeholder='New collection name',
                        max_length=255
                    ),
                    StrictButton(
                        PLUS_CIRCLE_ICON,
                        css_class='btn-primary',
                        type='submit',
                        hx_post=reverse_lazy('log_collections'),
                        hx_target='#collections',
                        hx_indicator="#indicator",
                    ),
                ),
            )
        )

    class Meta:
        model = Collection
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            raise ValidationError(
                ERROR_MESSAGES['name_required'],
                code='name_required'
            )
        name = name.lower()
        collection = Collection.objects.filter(
            name=name,
            user=self.user
        )
        if collection:
            raise ValidationError(
                ERROR_MESSAGES['collection_exists'],
                code='collection_exists'
            )
        return name

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = self.cleaned_data.get('name')
        instance.slug = slugify(self.cleaned_data.get('name'))
        instance.user = self.user
        instance.save()
        return instance


class UpdateCollectionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('initial').get('user')
        self.collection = kwargs.get('initial').get('collection')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_id = 'updateCollectionForm'
        self.helper.layout = Layout(
            Div(
                FieldWithButtons(
                    Field(
                        'name',
                        placeholder='Update collection name',
                        max_length=255
                    ),
                    StrictButton(
                        CHECKMARK_ICON,
                        css_class='btn-success',
                        type='submit',
                        hx_post=reverse_lazy('log_collection_update', kwargs={'pk': self.collection.id, 'slug': self.collection.slug}),
                        hx_target='#collection-update',
                        hx_indicator="#indicator",
                    ),
                ),
            )
        )

    class Meta:
        model = Collection
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            raise ValidationError(
                ERROR_MESSAGES['name_required'],
                code='name_required'
            )
        name = name.lower()
        collection = Collection.objects.filter(
            name=name,
            user=self.user
        )
        if collection:
            raise ValidationError(
                ERROR_MESSAGES['collection_exists'],
                code='collection_exists'
            )
        return name

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = self.cleaned_data.get('name')
        instance.slug = slugify(self.cleaned_data.get('name'))
        instance.save()
        return instance


class CreateItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('initial').get('user')
        self.collection = kwargs.get('initial').get('collection')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_id = 'createItemForm'

        self.helper.layout = Layout(
            Div(
                Field('name', placeholder='Item name'),
                Field('description', placeholder='Item description (optional)'),
                Div(
                    StrictButton(
                        PLUS_CIRCLE_ICON,
                        css_class='btn-primary float-end',
                        type='submit',
                        hx_post=reverse_lazy('log_collection_item_create', kwargs={'pk': self.collection.id}),
                        hx_target='#item-create',
                        hx_indicator="#indicator",
                    ),
                    css_class='d-grid gap-2',
                ),
            ),
            Div(css_class='clearfix')
        )

    class Meta:
        model = Item
        fields = ['name', 'description']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError(
                ERROR_MESSAGES['name_required'],
                code='name_required'
            )
        name = name.lower()
        item = Item.objects.filter(
            name=name,
            collection=self.collection,
        )
        if item:
            raise ValidationError(
                ERROR_MESSAGES['item_exists'],
                code='item_exists'
            )
        return name

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = self.cleaned_data.get('name')
        instance.description = self.cleaned_data.get('description')
        instance.collection = self.collection
        instance.save()
        return instance


class UpdateItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('initial').get('user')
        self.item = kwargs.get('initial').get('item')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_id = 'updateItemForm'

        self.helper.layout = Layout(
            Div(
                Field('name', placeholder='Item name'),
                Field('description', placeholder='Item description (optional)'),
                Div(
                    StrictButton(
                        CHECKMARK_ICON,
                        css_class='btn-success float-end',
                        type='submit',
                        hx_post=reverse_lazy('log_collection_item_update', kwargs={'pk': self.item.id}),
                        hx_target='#item-update',
                        hx_indicator="#indicator",
                    ),
                    css_class='d-grid gap-2',
                ),
            ),
            Div(css_class='clearfix')
        )

    class Meta:
        model = Item
        fields = ['name', 'description']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError(
                ERROR_MESSAGES['name_required'],
                code='name_required'
            )
        name = name.lower()

        # name didn't change
        if self.item.name == name:
            return name

        item = Item.objects.filter(
            name=name,
            collection=self.item.collection,
        )
        if item:
            raise ValidationError(
                ERROR_MESSAGES['item_exists'],
                code='item_exists'
            )
        return name

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = self.cleaned_data.get('name')
        instance.description = self.cleaned_data.get('description')
        instance.collection = self.item.collection
        instance.save()
        return instance
