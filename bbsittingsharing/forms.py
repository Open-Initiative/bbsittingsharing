from django.forms import ModelForm
from bbsittingsharing.models import BBSitting

class BBSittingForm(ModelForm):
    class Meta:
        model = BBSitting
        exclude = ['author', 'booked']
