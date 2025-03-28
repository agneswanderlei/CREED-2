from django import forms
from .models import Presos


class PresosForm(forms.ModelForm):

    class Meta:
        model = Presos
        fields = [
            'number_doc',
            'type_doc',
            'name_full',
            'state_origin',
            'institutions',
            'posto_grad',
            'sector',
            'photo',
        ]
        widgets = {
            'number_doc': forms.TextInput(attrs={'class': 'form-control'}),
            'type_doc': forms.Select(attrs={'class': 'form-control'}),
            'name_full': forms.TextInput(attrs={'class': 'form-control'}),
            'state_origin': forms.Select(attrs={'class': 'form-control'}),
            'institutions': forms.Select(attrs={'class': 'form-control'}),
            'posto_grad': forms.Select(attrs={'class': 'form-control'}),
            'sector': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(),
        }
        labels = {
            'number_doc': 'Nº Identificação',
            'type_doc': 'Tipo do Doc.',
            'name_full': 'Nome Completo',
            'state_origin': 'Estado',
            'institutions': 'Instituição',
            'posto_grad': 'Posto/Graduação',
            'sector': 'Setor',
            'photo': 'Foto',
        }

        def clean_number_doc(self):
            number_doc = self.cleaned_data['number_doc']
            if Presos.objects.filter(number_doc=number_doc).exists():
                raise forms.ValidationError('Número de documento já existe')
            return number_doc
        

        def clean_name_full(self):
            data = self.cleaned_data["name_full"].upper()
            return data

        # photo = forms.FileField(label='Selecione o arquivo')
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['photo'].widget.attrs['required'] = False

    