from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, F
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View, DetailView, CreateView

from .forms import AuthorForm, QuoteForm, TagForm
from .models import Quotes, Authors, Tags


class BaseListView(View):
    paginate_by = 10
    template_name = 'quotes_app/quotes_list.html'

    def get(self, request, *args, **kwargs):
        tags = Tags.objects.all()
        tags_font = Tags.objects.values('name').annotate(quote_count=Count('quote')).order_by('-quote_count', 'name')
        tags_font = tags_font.annotate(font=F('quote_count') * 2)
        paginator = Paginator(self.quotes, self.paginate_by)
        page = request.GET.get('page', 1)
        try:
            quotes = paginator.page(page)
        except PageNotAnInteger:
            quotes = paginator.page(1)
        except EmptyPage:
            quotes = paginator.page(paginator.num_pages)
        context = {'quotes': quotes, 'tags': tags, 'tags_font': tags_font, **kwargs}
        return render(request, self.template_name, context)


class QuoteListView(BaseListView):
    quotes = Quotes.objects.all()


class FilterListView(BaseListView):
    quotes = None

    def get(self, request, tag=None, *args, **kwargs):
        self.quotes = Quotes.objects.filter(tags__name=tag).distinct()
        return super().get(request, *args, **kwargs)


class AuthorView(DetailView):
    model = Authors
    template_name = 'quotes_app/author.html'
    context_object_name = 'author'
    slug_field = 'fullname'
    slug_url_kwarg = 'author'


@method_decorator(login_required, name='dispatch')
class AddAuthorView(CreateView):
    model = Authors
    template_name = 'quotes_app/add_author.html'
    form_class = AuthorForm
    success_url = reverse_lazy('quotes_app:main')


@method_decorator(login_required, name='dispatch')
class AddQuoteView(CreateView):
    model = Quotes
    template_name = 'quotes_app/add_quote.html'
    form_class = QuoteForm
    success_url = reverse_lazy('quotes_app:main')


@method_decorator(login_required, name='dispatch')
class AddTagView(CreateView):
    model = Tags
    template_name = 'quotes_app/add_tag.html'
    form_class = TagForm
    success_url = reverse_lazy('quotes_app:main')


class SyncView(View):
    pass
