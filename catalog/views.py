from django.shortcuts import render
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

	context = {
		'num_books':num_books,
		'num_instances':num_instances,
		'num_instances_available':num_instances_available,
		'num_authors':num_authors
	}

	# Render HTML template index.html and pass data from the context variable
	return render(request, 'index.html', context=context)