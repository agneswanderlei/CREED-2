from django import forms
from .models import Oficios, OficiosPresos
from presos.models import Teste
from django.core.exceptions import ValidationError
from django.utils.timezone import now


class OficiosForm(forms.ModelForm):
    
    class Meta:
        model = Oficios
        fields = '__all__'

        labels = {
            'n_oficios': 'Nº Ofício',
            'orgao': 'Remetente',
            'date_send': 'Data do Ofício',
            'descricao': 'Descrição do Oficio',
            'tipo_prisao': 'Tipo da Prisão',
            'n_sei': 'Nº do SEI',
            # 'n_pront_presos': 'Nº Prontuário'
            
        }
        widgets = {
            'tipo_prisao': forms.Select(attrs={'class': 'form-select'}),
            'orgao': forms.TextInput(attrs={'class': 'form-control'}),
            'n_oficios': forms.TextInput(attrs={'class': 'form-control'}),
            'n_sei': forms.TextInput(attrs={'class': 'form-control'}),
            'date_send': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'n_pront_presos': forms.SelectMultiple(attrs={'class': 'form-control'})
            
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     n_oficios = cleaned_data.get('n_oficios')
    #     date_send = cleaned_data.get('date_send')

    #     # Validação: Verifica se existe um número de ofício no mesmo ano
    #     if n_oficios and date_send:
    #         year = date_send.year  # Obtém o ano da data do ofício
    #         if Oficios.objects.filter(n_oficios=n_oficios, date_send__year=year).exists():
    #             raise ValidationError(
    #                 f"Já existe um ofício com o número {n_oficios} cadastrado no ano {year}."
    #             )

    #     return cleaned_data
    def clean(self):
        cleaned_data = super().clean()
        n_oficios = cleaned_data.get('n_oficios')
        date_send = cleaned_data.get('date_send')

        if n_oficios and date_send:
            year = date_send.year  # Obtém o ano da data do ofício
            # Caso seja uma atualização, exclua o próprio objeto da validação
            instance_id = self.instance.id if self.instance else None
            if instance_id:
                conflict = Oficios.objects.filter(
                    n_oficios=n_oficios, 
                    date_send__year=year
                ).exclude(id=instance_id).exists()
            else:
                # Criação
                conflict = Oficios.objects.filter(
                    n_oficios=n_oficios, 
                    date_send__year=year
                ).exists()
                
            if conflict:
                raise ValidationError(
                    f"Já existe um ofício com o número {n_oficios} cadastrado no ano {year}."
                )

        return cleaned_data

class OficiosPresosForm(forms.ModelForm):
    class Meta:
        model = OficiosPresos
        fields = '__all__'
        labels = {
            'data_envio': 'Data de Envio',
            'nome': 'Nome',
            'prontuario': 'Prontuário',
            'funcao': 'Função',
            'instituicao': 'Instituição',
            'state_origin': 'Estado',
            'tipo_prisao': 'Tipo de prisao',
            'n_oficios': 'Nº Ofícios',
            'n_sei': 'Nº do SEI'
        }


class TesteForm(forms.ModelForm):
    model = Teste
    fields = '__all__'
    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'})
    }