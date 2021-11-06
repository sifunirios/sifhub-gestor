from django import forms
from django.core.exceptions import ValidationError

from .models import ClientBusiness, MemberProfile


class ClientBusinessForm(forms.ModelForm):
    def clean_cnpj(self):
        """Reimplementação da validação de CNPJ único (original em django-localflavor)."""
        cnpj = self.cleaned_data.get('cnpj')
        if not cnpj:
            return ''
        business = ClientBusiness.objects.filter(cnpj=cnpj).first()
        if not business:
            return cnpj
        if business.client != self.cleaned_data.get('client'):
            raise ValidationError('Negócio com este CNPJ já existe.')
        return cnpj

    class Meta:
        model = ClientBusiness
        fields = '__all__'


class MemberProfileForm(forms.ModelForm):
    def save(self, commit=True):
        # If member type changed, update its group too
        if 'member_type' in self.changed_data:
            # member_type is a Group object
            member_type = self.cleaned_data.get('member_type')
            member = self.cleaned_data.get('member')
            member.groups.clear()
            member.groups.add(member_type)
        return super().save(commit)

    class Meta:
        model = MemberProfile
        fields = '__all__'
