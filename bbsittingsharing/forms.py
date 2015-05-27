from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext as _

from registration.users import UserModel
from bbsittingsharing.models import BBSitting, Parent

class ParentForm(UserCreationForm):
    referer = forms.CharField()
    tos = forms.BooleanField(widget=forms.CheckboxInput,
         label=_('I have read and agree to the Terms of Service'),
         error_messages={'required': _("You must agree to the terms to register")})
    class Meta:
        model = UserModel()
        fields = ('first_name', 'last_name', UserModel().USERNAME_FIELD, "email", )
    
    def clean_referer(self):
        """gets the referer if it exists or raise a form error"""
        referer = self.cleaned_data['referer']
        try:
            user = Parent.objects.get(username=referer)
        except Parent.DoesNotExist:
            raise forms.ValidationError(_(u'User "%s" does not exist.') % referer)
        return user
    
    def clean_email(self):
        """ Validate that the supplied email address is unique for the site."""
        if self.Meta.model.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']
    
    def clean_username(self):
        # Need to override since default checks unicity on auth table
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            self.Meta.model._default_manager.get(username=username)
        except self.Meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


class BBSittingForm(forms.ModelForm):
    class Meta:
        model = BBSitting
        exclude = ['author', 'booked']

class ReferForm(forms.Form):
    referee = forms.EmailField()
