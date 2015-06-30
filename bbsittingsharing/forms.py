from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext as _

from registration.users import UserModel
from bbsittingsharing.models import BBSitting, Parent, Equipment

class ListSelect(forms.Select):
    """Override of select field to return a list for group choice"""
    def render(self, *args, **kwargs):
        """Adds an empty value for consistency with other model select fields"""
        self.choices.field.empty_label = "---------"
        return super(ListSelect, self).render(*args, **kwargs)
    def value_from_datadict(self, data, files, name):
        """Transforms the single value returned into a list, so that it's managed by the manytomany field"""
        return [super(ListSelect, self).value_from_datadict(data, files, name)]

class ParentForm(UserCreationForm):
    referer = forms.EmailField(label=_("Referer"))
    tos = forms.BooleanField(label=_('I have read and agree to the Terms of Service'),
         error_messages={'required': _("You must agree to the terms to register")})
    
    class Meta:
        model = UserModel()
        fields = ('first_name', 'last_name', UserModel().USERNAME_FIELD, "female", "email", "groups", "district", "school", "referer")
        widgets = {'groups': ListSelect(), 'referer': forms.EmailInput(),
            'female': forms.RadioSelect(choices=((True, _('a woman')), (False, _('a man'))))}
        labels = {'groups': _("Arrondissement")}
        help_texts = {'groups': None}
    
    def clean_referer(self):
        """gets the referer if it exists or raise a form error"""
        referer = self.cleaned_data['referer']
        if referer is None:
            raise forms.ValidationError(_(u'Please provide the email of the person who introduced you.'))
        try:
            user = Parent.objects.get(email=referer)
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
        raise forms.ValidationError(self.error_messages['duplicate_username'], code='duplicate_username')

class UpdateProfileForm(forms.ModelForm):
    equipment = forms.ModelMultipleChoiceField(queryset = Equipment.objects.filter(default=True),
        required=False, widget=forms.CheckboxSelectMultiple(), label=_("Available equipment"))
    other_equipment = forms.CharField(label=_("Other"), required=False)
    class Meta:
        model = Parent
        fields = ['first_name', 'last_name', 'email', 'phone', 'kidsnb', 'school', 'bbsitter', 'ok_at_home', 'ok_at_others', 'picture', 'equipment']
        widgets = {'ok_at_home': forms.RadioSelect(choices=((True, _('Yes')), (False, _('No')))),
            'ok_at_others': forms.RadioSelect(choices=((True, _('Yes')), (False, _('No'))))}
    
    def clean_other_equipment(self):
        if self.cleaned_data["other_equipment"]:
            new_equipment = Equipment.objects.create(name = self.cleaned_data["other_equipment"], default=False)
            self.cleaned_data["equipment"] = list(self.cleaned_data["equipment"])
            self.cleaned_data["equipment"].append(new_equipment)

class BBSittingForm(forms.ModelForm):
    class Meta:
        model = BBSitting
        exclude = ['author', 'booked']
        widgets = {'date': forms.TextInput(attrs={'type':'date'}),
            'start': forms.TextInput(attrs={'type':'time', 'step': 900}),
            'end'  : forms.TextInput(attrs={'type':'time', 'step': 900}),
            'bbsitter_found': forms.RadioSelect(choices=((True, _('Yes')), (False, _('No')))),
            'at_authors': forms.Select(choices=((True, _('At my place')), (False, _('At someone else''s'))))}

class ReferForm(forms.Form):
    referee = forms.EmailField(label=_("Please provide the email of the person you want to share bbsittings with"))

class ContactForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea())
