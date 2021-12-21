from django.contrib import admin

# Register your models here.
# Import the models we created to register them
from .models import Author, Genre, Book, Language, BookInstance

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(BookInstance)