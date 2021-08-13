from users.models import Boss, CustomUser
from django import forms
from django.db.models import Q

from hits.models import Hit

class CreateHitForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['target_name'].required = True
        
        user = self.request.user
        self.user_rol = self.get_user_rol(user)
        print(self.user_rol)
        active_users = CustomUser.objects.filter(status=1)
        lackeys = Boss.objects.get(id=user.id).lackeys.all().filter(id__in=active_users) if self.user_rol != 'Hitman' else Boss.objects.none()

        self.fields['hitman'].queryset = lackeys

        if self.instance.pk or self.instance.status != 0:
            self.fields['created_by'].widget.attrs['class'] = 'disable'
            self.fields['target_name'].widget.attrs['class'] = 'disable'
            self.fields['hitman'].queryset = CustomUser.objects.filter(Q(id__in=lackeys) | Q(id=self.instance.hitman.id))
            if self.instance.status != 0 or self.user_rol == 'Hitman':
                self.fields['hitman'].widget.attrs['class'] = 'disable'
            if self.instance.status != 0:
                self.fields['status'].widget.attrs['class'] = 'disable'
                self.fields['description'].widget.attrs['class'] = 'disable'
        else:
            self.fields['status'].initial = 0
            self.fields['created_by'].initial = user
            self.fields['status'].required = False
            self.fields['created_by'].required = False

    def get_user_rol(self, user):
        return user.groups.all().values_list('name')[0][0]

    def clean_target_name(self):
        instance = getattr(self, 'instance', None)
        if instance.pk:
            return instance.target_name
        else:
            print('self.instance.pk')
            return self.cleaned_data['target_name']

    def clean_description(self):
        instance = getattr(self, 'instance', None)
        if instance.pk and instance.status != 0:
            return instance.description
        else:
            return self.cleaned_data['description']
    
    def clean_created_by(self):
        instance = getattr(self, 'instance', None)
        if instance.pk:
            return instance.created_by
        else:
            return self.cleaned_data['created_by']

    def clean_status(self):
        instance = getattr(self, 'instance', None)
        if instance.pk and instance.status != 0:
            return instance.status
        else:
            return self.cleaned_data['status']

    def clean_hitman(self):
        instance = getattr(self, 'instance', None)
        if self.user_rol == 'Hitman' or instance.status != 0:
            return instance.hitman
        else:
            return self.cleaned_data['hitman']

    class Meta:
        model = Hit
        fields = ['hitman', 'target_name', 'description', 'status', 'created_by']

        widgets = {
            'target_name': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.TextInput(attrs={'class': 'input'}),
            'hitman': forms.Select(attrs={'class': 'input'}),
            'status': forms.Select(attrs={'class': 'input'}),
            'created_by': forms.Select(attrs={'class': 'input'}),
        }

        labels = {
            'target_name': 'Target name',
            'description': 'Description',
            'hitman': 'Htman',
            'status': 'Status',
            'created_by': 'Created by',
        }
