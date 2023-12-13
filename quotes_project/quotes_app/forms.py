from django.forms import ModelForm, CharField, TextInput, Textarea, DateField, DateInput, CheckboxSelectMultiple, \
    Select, ModelChoiceField, ModelMultipleChoiceField, SelectMultiple

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
    author = ModelChoiceField(Authors.objects.all(), widget=Select(attrs={"class": "form-select"}))
    tags = ModelMultipleChoiceField(Tags.objects.all(), widget=SelectMultiple(attrs={"class": "form-select"}),
                                    required=False)

    class Meta:
        model = Quotes
        fields = ('quote', 'author', 'tags')


class CreateTagForm(ModelForm):
    name = CharField(max_length=50, widget=TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Tags
        fields = ('name',)

    def save(self, commit=True):
        tag_name = self.cleaned_data['name']
        tag, created = Tags.objects.get_or_create(name=tag_name)
        if commit:
            tag.save()
        return tag


class BindTagForm(ModelForm):
    quote = ModelChoiceField(Quotes.objects.all(), widget=Select(attrs={"class": "form-select"}), required=True)
    tags = ModelMultipleChoiceField(Tags.objects.all(), widget=SelectMultiple(attrs={"class": "form-select"}),
                                    required=True)

    class Meta:
        model = Tags
        fields = ('quote', 'tags')

    def save(self, commit=True):
        quote_instance = self.cleaned_data['quote']
        tags_instances = self.cleaned_data['tags']
        for tag_instance in tags_instances:
            if tag_instance not in quote_instance.tags.all():
                quote_instance.tags.add(tag_instance)
        if commit:
            quote_instance.save()
        return quote_instance
