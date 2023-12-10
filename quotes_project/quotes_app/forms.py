from django.forms import ModelForm, CharField, TextInput, Textarea, DateField, DateInput, CheckboxSelectMultiple, Select, ModelChoiceField

from .models import Authors, Quotes, Tags


class AuthorForm(ModelForm):
    fullname = CharField(max_length=120, widget=TextInput(attrs={"class": "form-control"}))
    born_date = DateField(widget=DateInput(attrs={"class": "form-control", "placeholder": "MM/DD/YYYY"}))
    born_location = CharField(max_length=200, widget=TextInput(attrs={"class": "form-control"}))
    description = CharField(widget=Textarea(attrs={"class": "form-control"}))

    def clean_born_location(self):
        born_location = self.cleaned_data['born_location']
        return f'in {born_location}'

    class Meta:
        model = Authors
        fields = ('fullname', 'born_date', 'born_location', 'description')


class QuoteForm(ModelForm):
    quote = CharField(widget=Textarea(attrs={"class": "form-control"}))
    author = ModelChoiceField(queryset=Authors.objects.all(), widget=Select(attrs={"class": "form-select"}))

    class Meta:
        model = Quotes
        fields = ('quote', 'author')


class TagForm(ModelForm):
    name = CharField(max_length=50, widget=TextInput(attrs={"class": "form-control"}))
    quote = ModelChoiceField(queryset=Quotes.objects.all(), widget=Select(attrs={"class": "form-select"}))

    class Meta:
        model = Tags
        fields = ('name', 'quote')
