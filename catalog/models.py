from django.db import models
from django.urls import reverse
import uuid

# Create your models here.
class Genre(models.Model):
	""" Model representing a book genre"""
	name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction")

	def __str__(self):
		"""String for representing the Model object"""
		return self.name


class Book(models.Model):
	"""Model representing a book (but not a specific copy of a book)"""
	title = models.CharField(max_length=200)

	# Foreign Key used because book can only have one author, but authors can have multiple books
	# Author as a string rather than object because it has not been declared yet
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

	summary = models.TextField(max_length=1000, help_text="Enter brief description of the book")
	isbn = models.CharField("ISBN", max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

	# ManyToManyField used because genre can contain many books. Books can cover many genres.
	# Genre class has already been defined, so we can specify the object above
	genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

	def __str__(self):
		"""String for representing the Model object"""
		return self.title

	def get_absolute_url(self):
		"""Returns the URL to access a detail record for this book"""
		return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
	"""Model representing a specific copy of a book"""
	# UUIDField is used for the id field to set it as the primary_key for this model. This type of field allocates a globally unique value for each instance (one for every book you can find in the library).
	id = models.UUIDField(primary_key=True, default=uuid.uuid4,
	help_text="Unique ID for this particular book")
	book = models.ForeignKey("Book", on_delete=models.RESTRICT, null=True)
	imprint = models.CharField(max_length=200)
	due_back = models.DateField(null=True, blank=True)

	LOAN_STATUS = (
		("m", "Maintenance"),
		("o", "On Loan"),
		("a", "Available"),
		("r", "Reserved")
	)

	status = models.CharField(max_length=1,
							  choices=LOAN_STATUS,
							  blank=True,
							  default="m",
							  help_text="Book availability"
	)

	class Meta:
		ordering = ['due_back']

	def __str__(self):
		return f"{self.id} ({self.book.title})"


class Author(models.Model):
	"""Model representing an author"""
	fname = models.CharField(max_length=100)
	sname = models.CharField(max_length=100)
	date_of_birth = models.DateField(null=True, blank=True)
	date_of_death = models.DateField("Died", null=True, blank=True)

	class Meta:
		ordering = ['sname', 'fname']

	def get_absolute_url(self):
		"""Returns URL to access a particular author instance"""
		return reverse('author-detail', args=[str(self.id)])

	def __str__(self):
		return f"{self.sname}, {self.fname}"