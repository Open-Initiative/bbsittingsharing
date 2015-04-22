from datetime import datetime, timedelta
from django.views.generic.list import ListView

from bbsittingsharing.models import BBSitting

class SearchView(ListView):
    """Searches all baby sittings close to a date"""
    model = BBSitting
    template_name = "bbsittingsharing/bbsitting_search.html"
    def get_queryset(self, *args, **kwargs):
        """Returns all BBSittings in a +/- 3 days range"""
        date = datetime.strptime(self.kwargs['date'], "%Y%m%d")
        delta = timedelta(days=3)
        return BBSitting.objects.filter(date__range=[date-delta, date+delta])
