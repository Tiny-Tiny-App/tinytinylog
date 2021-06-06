from django.views.generic import TemplateView


class CollectionsView(TemplateView):
    template_name = 'collections.html'