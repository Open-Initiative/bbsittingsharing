# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.db import IntegrityError
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect
from django.template import RequestContext
from django.views import generic
from registration.backends.default.views import RegistrationView

from helpers import notify, send_email
from models import BBSitting, Booking, Parent, School
from forms import BBSittingForm, ReferForm, ParentForm, UpdateProfileForm

class LoginRequiredMixin(object):
    """Ensures the user is logged in to access the view"""
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class RegisterView(RegistrationView):
    """Override of the default backend to take the referer into account"""
    form_class = ParentForm
    def get_form_kwargs(self, request=None, form_class=None):
        kwargs = super(RegisterView, self).get_form_kwargs()
        kwargs['group'] = self.request.GET.get('groups')
        return kwargs
    def get_initial(self):
        return dict(zip(self.request.GET.keys(), self.request.GET.values()))
    def form_valid(self, request, form):
        """Adds the referer as a friend"""
        new_user = self.register(request, form)
        if form.cleaned_data.get('referer'):
            new_user.friends.add(form.cleaned_data['referer'])
        return redirect(self.get_success_url())

class UpdateProfileView(LoginRequiredMixin, generic.UpdateView):
    model = Parent
    slug_field = 'email'
    form_class = UpdateProfileForm
    def get_form(self, form_class=None):
        form = super(UpdateProfileView, self).get_form(form_class)
        form.fields["school"].queryset = School.objects.filter(group=self.request.user.groups.first())
        return form

class SearchView(LoginRequiredMixin, generic.ListView):
    """Searches all baby sittings close to a date"""
    model = BBSitting
    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('date'):
            self.bbsitting = None
            self.date = datetime.strptime(self.request.GET['date'], "%Y-%m-%d")
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
        context["selected_date"] = self.date
        return context

class CreateView(LoginRequiredMixin, generic.CreateView):
    """BBSitting creation view, saving the author"""
    model = BBSitting
    form_class = BBSittingForm
    def form_valid(self, form):
        """If the form is valid, save the associated models"""
        form.instance.author = self.request.user
        if form.cleaned_data['bbsitter']:
            subject = "%s vous propose de réaliser un babysitting sur bbsitting sharing by Echos Kids"%self.request.user.get_full_name()
            notify(self.request, form.instance, subject, 'bbsitter_invite', form.cleaned_data['bbsitter'])
        return super(CreateView, self).form_valid(form)

class BookView(LoginRequiredMixin, generic.TemplateView):
    """Creates a booking for the bbsitting and the user"""
    template_name="bbsittingsharing/book_confirm.html"
    def get(self, request, pk):
        bbsitting = BBSitting.objects.get(pk=pk)
        already_requested = False
        if bbsitting.author==request.user:
            return HttpResponseForbidden()
        try:
            booking = Booking.objects.create(bbsitting=bbsitting, parent=request.user)
            subject = "Demande de participation au bbsitting"
            notify(request, booking, subject, 'book_request', bbsitting.author.email)
        except IntegrityError:
            already_requested = True
        return super(BookView, self).get(request, recipient=bbsitting.author.get_full_name(), already_requested=already_requested)

class ValidateView(LoginRequiredMixin, generic.TemplateView):
    """Validates the booking"""
    template_name="bbsittingsharing/book_validate.html"
    def get(self, request, pk, booking_pk):
        booking = Booking.objects.get(pk=booking_pk)
        #check the bbsitting id and author
        if booking.bbsitting.pk != int(pk) or booking.bbsitting.author != request.user:
            raise Http404
        booking.validated = True
        booking.save()
        subject = "Validation du bbsitting"
        notify(request, booking, subject, 'book_validated')
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
        subject = 'Un ami, %s, vous propose de devenir membre de Bbsitting sharing'%self.request.user.get_full_name()
        send_email([recipient], subject, 'refer_request', email_context)
        return super(ReferView, self).form_valid(form)
