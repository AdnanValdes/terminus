from django.contrib import admin

# Register your models here.
# Import the models we created to register them
from .models import Author, Genre, Book, Language, BookInstance

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
# admin.site.register(BookInstance)

class BookInline(admin.TabularInline):
	model = Book

class AuthorAdmin(admin.ModelAdmin):
	list_display = ('sname', 'fname', 'date_of_birth', 'date_of_death')

	fields = ['fname', 'sname', ('date_of_birth', 'date_of_death')]

	inlines = [BookInline]

admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'display_genre')

	inlines = [BooksInstanceInline] # Adds inline section to add book instances on admin

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	list_display = ('book', 'status', 'due_back', 'id')

	list_filter = ('status', 'due_back')
	fieldsets = (
		(None, { # The first item of the tuple is the name of the section
			'fields':('book','imprint','id')
		}),
		('Availability', {
			'fields':('status','due_back')
		})
	)
