from django.db.models import Model, CharField, DateField, ForeignKey, CASCADE, DO_NOTHING


class Authors(Model):
    fullname = CharField(max_length=120)
    born_date = DateField()
    born_location = CharField(max_length=200)
    description = CharField()

    class Meta:
        managed = False
        db_table = 'authors'

    def __str__(self):
        return self.fullname


class Quotes(Model):
    author = ForeignKey(Authors, CASCADE, db_column='author')
    quote = CharField()

    class Meta:
        managed = False
        db_table = 'quotes'

    def __str__(self):
        return self.quote


class Tags(Model):
    name = CharField(max_length=50)
    quote = ForeignKey(Quotes, DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tags'

    def __str__(self):
        return self.name
