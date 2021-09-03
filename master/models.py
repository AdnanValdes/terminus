from django.db import models

# Create your models here.
from django.db import models
from django.db.models.fields import related

# Create your models here.
class Users(models.Model):
    first_name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.EmailField()


# Location data
class Countries(models.Model):
    country = models.CharField(max_length=32, unique=True)
    code = models.CharField(max_length=3, unique=True)
    un_code = models.IntegerField(unique=True, primary_key=True, default=-99)

    def __str__(self):
        return f"{self.country} ({self.code})"

class Provinces(models.Model):
    province = models.CharField(max_length=16)
    code = models.CharField(max_length=6, null=True, blank=True)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.province}, {self.country}"


class Cities(models.Model):
    city = models.CharField(max_length=16)
    province = models.ForeignKey(Provinces, on_delete=models.CASCADE, related_name="state")

    def __str__(self):
        return f"{self.city}, {self.province}"


class Address(models.Model):
    unit = models.CharField(max_length=16, null=True, blank=True)
    address = models.CharField(max_length=128)
    district = models.CharField(max_length=128, null=True, blank=True)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.unit} - {self.address}, {self.city}, {self.zip_code}"


# Housing data
class Housing(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.address}, {self.from_date} TO {self.to_date}"

# Employment data
class Employer(models.Model):
    employer = models.CharField(max_length=32)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="office")
    phone = models.IntegerField()

    def __str__(self):
        return f"{self.employer}, {self.address}"


class Work(models.Model):
    position = models.CharField(max_length=32)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.position}, {self.employer}\n{self.start_date} to {self.end_date}"


class Travel(models.Model):
    from_country = models.ForeignKey(Countries, on_delete=models.CASCADE, related_name='departure')
    to_country = models.ForeignKey(Countries, on_delete=models.CASCADE, related_name='arrival')
    travel_date = models.DateField()
    comments = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return f" DEP: {self.from_country}, ARR: {self.to_country}, TRVL DATE: {self.travel_date} "


# Book data
class Authors(models.Model):
    first_name = models.CharField(max_length=64, null=True)
    surname = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f'{self.surname}, {self.first_name}'


class Books(models.Model):

    AUDIOBOOK = "audio"
    EBOOK = "ebook"
    PRINT = "print"
    BOOK_FORMAT = [
        (AUDIOBOOK, "Audiobook"),
        (EBOOK, 'Ebook'),
        (PRINT, 'Print')
    ]

    title = models.CharField(max_length=64)
    series = models.CharField(max_length=64, null=True, blank=True)
    book_format = models.CharField(max_length=5, choices=BOOK_FORMAT, default=PRINT)
    authors = models.ManyToManyField(Authors)
    owned = models.BooleanField(default=True)


    def __str__(self):
        return f'{self.title}, {self.author}, {self.book_format}'


class Documents(models.Model):
    document = models.CharField(max_length=64)
    expiry = models.DateField()
