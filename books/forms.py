from .models import Book
from django import forms
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'publication_date', 'author', 'price', 'pages', 'book_type', )