from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect
from django.template import RequestContext
from django.views import generic
from registration.backends.default.views import RegistrationView

from helpers import notify, send_email
from models import BBSitting, Booking, Parent
from forms import BBSittingForm, ReferForm, ParentForm

class LoginRequiredMixin(object):
    """Ensures the user is logged in to access the view"""
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class RegisterView(RegistrationView):
    """Override of the default backend to take the referer into account"""
    form_class = ParentForm
    def get_initial(self):
        return {'referer': self.request.GET.get('referer')}
    def form_valid(self, request, form):
        """Adds the referer as a friend"""
        new_user = self.register(request, form)
        if form.cleaned_data.get('referer'):
            new_user.friends.add(form.cleaned_data['referer'])
        return redirect(self.get_success_url())

class SearchView(LoginRequiredMixin, generic.ListView):
    """Searches all baby sittings close to a date"""
    model = BBSitting
    template_name = "bbsittingsharing/bbsitting_search.html"
    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('date'):
            self.bbsitting = None
            self.date = datetime.strptime(self.request.GET['date'], "%Y%m%d")
        elif kwargs.get('pk'):
            self.bbsitting = BBSitting.objects.get(pk=kwargs['pk'])
            self.date = self.bbsitting.date
        else:
            raise ValueError
        return super(SearchView, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        """Returns all BBSittings in a +/- 3 days range"""
        delta = timedelta(days=3)
        return BBSitting.objects.filter(date__range=[self.date-delta, self.date+delta])
    
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context["selected_bbsitting"] = self.bbsitting
        return context

class CreateView(LoginRequiredMixin, generic.CreateView):
    """BBSitting creation view, saving the author"""
    model = BBSitting
    form_class = BBSittingForm
    def form_valid(self, form):
        """If the form is valid, save the associated models"""
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

class BookView(LoginRequiredMixin, generic.TemplateView):
    """Creates a booking for the bbsitting and the user"""
    template_name="bbsittingsharing/book_confirm.html"
    def get(self, request, pk):
        bbsitting = BBSitting.objects.get(pk=pk)
        if bbsitting.author==request.user:
            HttpResponseForbidden
        booking = Booking.objects.create(bbsitting=bbsitting, parent=request.user)
        notify(request, booking, 'book_request')
        return super(BookView, self).get(request, recipient=bbsitting.author.get_full_name())

class ValidateView(LoginRequiredMixin, generic.TemplateView):
    """Validates the booking"""
    template_name="bbsittingsharing/book_validate.html"
    def get(self, request, pk, booking_pk):
        booking = Booking.objects.get(pk=booking_pk)
        #check the bbsitting id and author
        if booking.bbsitting.pk != pk or booking.bbsitting.author != request.user:
            raise Http404
        booking.validated = True
        booking.save()
        notify(request, booking, 'book_validated')
        return super(ValidateView, self).get(request, booking=booking)

class FriendsView(LoginRequiredMixin, generic.ListView):
    """Shows the list of referers, referees, and members of the same group"""
    template_name = "bbsittingsharing/friends_list.html"
    context_object_name = 'friends'
    def get(self, request, *args, **kwargs):
        self.queryset = request.user.friends.all()
        return super(FriendsView, self).get(request, *args, **kwargs)

class ReferView(LoginRequiredMixin, generic.edit.FormView):
    """Shows the list of referees, and members of the same group"""
    template_name = "bbsittingsharing/refer.html"
    form_class = ReferForm
    success_url = reverse_lazy("refer_confirm")
    def get_context_data(self, **kwargs):
        context = super(ReferView, self).get_context_data(**kwargs)
        context['referees'] = self.request.user.referees.all()
        return context
    def form_valid(self, form):
        email_context = RequestContext(self.request, {'referer': self.request.user})
        recipient = form.cleaned_data['referee']
        send_email([recipient], 'hello', 'refer_request', email_context)
        return super(ReferView, self).form_valid(form)
