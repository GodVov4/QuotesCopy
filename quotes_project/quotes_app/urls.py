from django.urls import path

from .views import AuthorView, AddAuthorView, AddQuoteView, AddTagView, QuoteListView, FilterListView, BindTagView, sync

app_name = 'quotes_app'

urlpatterns = [
    path('', QuoteListView.as_view(), name='main'),
    path('add_author/', AddAuthorView.as_view(), name='add_author'),
    path('add_quote/', AddQuoteView.as_view(), name='add_quote'),
    path('add_tag/', AddTagView.as_view(), name='add_tag'),
    path('bind_tags/', BindTagView.as_view(), name='bind_tags'),
    path('tag/<str:tag>/', FilterListView.as_view(), name='tag'),
    path('author/<str:author>/', AuthorView.as_view(), name='author'),
    path('sync/', sync, name='sync'),
]
