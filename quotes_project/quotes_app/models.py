from django.db.models import Model, CharField, ForeignKey, CASCADE, ManyToManyField


class Authors(Model):
    fullname = CharField(max_length=120)
    born_date = CharField(max_length=80)
    born_location = CharField(max_length=200)
    description = CharField()

    class Meta:
        managed = True
        db_table = 'authors'

    def __str__(self):
        return self.fullname


class Quotes(Model):
    author = ForeignKey(Authors, CASCADE, db_column='author')
    quote = CharField()
    tags = ManyToManyField('Tags', 'quotes')

    class Meta:
        managed = True
        db_table = 'quotes'

    def __str__(self):
        return self.quote


class Tags(Model):
    name = CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'tags'

    def __str__(self):
        return self.name
