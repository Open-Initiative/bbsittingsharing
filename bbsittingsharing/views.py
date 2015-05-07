from datetime import datetime, timedelta
from django.views import generic

from bbsittingsharing.models import BBSitting
from bbsittingsharing.forms import BBSittingForm

class SearchView(generic.ListView):
    """Searches all baby sittings close to a date"""
    model = BBSitting
    template_name = "bbsittingsharing/bbsitting_search.html"
    def get_queryset(self, *args, **kwargs):
        """Returns all BBSittings in a +/- 3 days range"""
        date = datetime.strptime(self.kwargs['date'], "%Y%m%d")
        delta = timedelta(days=3)
        return BBSitting.objects.filter(date__range=[date-delta, date+delta])

class CreateView(generic.CreateView):
    model = BBSitting
    form_class = BBSittingForm
    def form_valid(self, form):
        """If the form is valid, save the associated models"""
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)
