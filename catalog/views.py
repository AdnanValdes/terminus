from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre

# Create your views here.

def index(request):
	"""View function for home page of the site"""

	# Generate counts of some of the name objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	# Available books (with status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()

	# Another option for counting. `all()` is implied by default
	num_authors = Author.objects.count()

	num_scifi = Book.objects.filter(genre__name__icontains="sci-fi").count()
	context = {
		'num_books':num_books,
		'num_instances':num_instances,
		'num_instances_available':num_instances_available,
		'num_authors':num_authors,
		'num_scifi':num_scifi
	}

	# Render HTML template index.html and pass data from the context variable
	return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    #context_object_name = 'my_book_list'   # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location

class BookDetailView(generic.DetailView):
    model = Book
