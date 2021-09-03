import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "terminus.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
import django
django.setup()
import pandas as pd
import numpy as np
import sqlite3
from master.models import *

def main():
    # Add countries
    countries = pd.read_csv('PreLoad/countries.txt')
    countries.columns = ['country', 'code', 'un_code']
    countries.set_index('un_code', inplace=True)
    con = sqlite3.connect('master.sqlite3')
    countries.to_sql('master_countries', con=con, if_exists='append', index=True, index_label='un_code')

    # Add provinces/states

    def add_provinces(country_name, provice_list, code_list):
        cnt = Countries.objects.get(country=country_name)
        for i, k in zip(provice_list, code_list):
            x = Provinces(province=i, code=k, country=cnt)
            x.save()

    def add_city(provinces_codes, city_list, single_state=False):
        if single_state:
            prov = Provinces.objects.get(code=provinces_codes)
            for i in city_list:
                x = Cities(city=i, province=prov)
                x.save()
        else:
            for i, k in zip(provinces_codes, city_list):
                prov = Provinces.objects.get(code=i)
                x = Cities(city=k, province=prov)
                x.save()

    def add_address(unit, address, city, zip_code):
        x = Address(unit=unit, address=address, city=Cities.objects.get(city=city), zip_code=zip_code)
        x.save()

    # Canada
    provinces = ['Alberta', 'British Columbia']
    codes = ['AB', 'BC']
    add_provinces("Canada", provinces, codes)

    # Mexico
    state = ['Mexico City']
    code = ['CMX']
    add_provinces('Mexico', state, code)

    # India
    India = pd.read_csv('PreLoad\states.csv', sep='\t')
    India = India[India['Subdivision category'] == 'State']
    India['Subdivision name'] = India['Subdivision name'].str.replace(r"\[(?:.*)]", "")
    add_provinces('India', ['Delhi', 'Uttarakhand'], ['DL', 'UT'])


    # Add citites
    add_city('BC', ['Vancouver', 'Surrey', 'Delta', 'Richmond'], single_state=True)
    add_city(['CMX'], ['Mexico City'])
    add_city(['UT'], ['Mussoorie'])
    add_city(['DL'], ['Delhi'])

    # Add addresses
    addresses = pd.read_csv("PreLoad/Addresses.csv").loc[:11].drop(9)
    addresses.columns = ['Start', 'End', 'Unit', 'Address', 'District', 'City', 'Province', 'Zip', 'Country']
    addresses = addresses.fillna(np.nan).replace([np.nan], [None])

    for i in addresses.iterrows():
        i = i[1]
        x = Address(unit=i.Unit, address=i.Address, district=i.District, city=Cities.objects.get(city=i.City), zip_code=i.Zip)
        x.save()

    # Add housing
    def add_housing(zip_code, start, end):
        x = Housing(address=Address.objects.get(zip_code=zip_code), from_date=start, to_date=end)
        x.save()

    housing = pd.read_csv("PreLoad/Addresses.csv").loc[:11].drop(9)
    housing['Start'] = pd.to_datetime(housing['Start'], format='%Y-%m-%d')
    housing['End'] = pd.to_datetime(housing['End'], format='%Y-%m-%d')

    for h in housing.loc[:9].iterrows():
        h = h[1]
        add_housing(h.Zip, h.Start, h.End)

    # Add employers
    def add_employer(employer, address, phone):
        x = Employer(employer=employer, address=Address.objects.get(address=address), phone=phone)
        x.save()

    add_address(unit=None, address='7800 Alpha Way', city='Delta', zip_code='V4k 0A7')
    add_address(unit='Unit 4', address='4335 Skeena Street', city='Delta', zip_code='V4k 0A6')
    add_address(unit=None, address='4440 Cowley Crescent', city='Richmond', zip_code='V7B 1B8')
    add_employer(employer='Alpha Aviation, Inc', address='7800 Alpha Way', phone=6049465361)
    add_employer('Pacific Flying Club', '4335 Skeena Street', 6049460011)
    add_employer("Pacific Coastal Airlines", '4440 Cowley Crescent', 6042142361)


    # Add work/jobs
    def add_work(position, employer, start, end):
        x = Work(position=position, employer=Employer.objects.get(employer=employer), start_date=start, end_date=end)
        x.save()

    w = pd.read_csv('PreLoad\work.csv').dropna()
    w['Start'] = pd.to_datetime(w['Start'], format='%Y-%m-%d')
    w.End = pd.to_datetime(w.End, format='%Y-%m-%d')
    position = ['First Officer', 'Flight Instructor', 'CSA']
    w['Position'] = position
    for work in w.iterrows():
        work = work[1]
        add_work(work.Position, work.Employer, work.Start, work.End)

    # Add travel
    def add_travel(from_country, to_country, travel_date, comments):
        x = Travel(from_country=Countries.objects.get(code=from_country), to_country=Countries.objects.get(code=to_country), travel_date=travel_date, comments=comments)
        x.save()

    t = pd.read_csv('PreLoad/travel.csv')
    t = t.fillna(np.nan).replace([np.nan], [None])
    t.Date = pd.to_datetime(t.Date, format='%Y-%m-%d')
    t = t.loc[:56]

    for travel in t.iterrows():
        travel = travel[1]
        add_travel(travel.Dep, travel.Arr, travel.Date, travel.Comments)

    # Add authors
    cb = pd.read_csv('PreLoad/Books_complete.csv')
    authors = pd.Series(cb['Author(s)'].unique()).str.split(",", expand=True)
    authors.columns = ['surname', 'first_name']
    authors['surname'] = authors['surname'].str.strip()
    authors['first_name'] = authors['first_name'].str.strip()
    authors.drop_duplicates(inplace=True)
    authors.sort_values(by='surname', inplace=True)
    authors = authors.fillna(np.nan).replace([np.nan], [None])
    authors.to_sql('master_authors', con=con, if_exists='append', index=True, index_label='id')

    # Add books
    def add_books(title, series, book_format, author_first, author_last, owned=True):
        try:
            book = Books.objects.get(title=title, series=series, book_format=book_format)
        except Exception as e:
            print(e)
            print(f'Adding new book, {title}, {book_format}, {author_first, author_last}')
            book = Books(title=title, series=series, book_format=book_format, owned=owned)
            book.save()
        book.authors.add(Authors.objects.get(first_name=author_first, surname=author_last))

    b = pd.read_csv('PreLoad/Books_complete.csv')
    b[['last_name', 'first_name']] = pd.Series(b['Author(s)']).str.split(",", expand=True)
    b = b.fillna(np.nan).replace([np.nan], [None])
    b.last_name = b.last_name.str.strip()
    b.first_name = b.first_name.str.strip()
    b.Format = b.Format.replace([None], 'print')

    for entry in b.iterrows():
        entry = entry[1]
        add_books(title=entry.Name, series=entry.Series, book_format=entry.Format, author_first=entry.first_name, author_last=entry.last_name)

    # Add Documents
    def add_document(document, expiry):
        x = Documents(document=document, expiry=expiry)
        x.save()

    d = pd.read_csv('PreLoad/Documents.csv').dropna()
    d.Expiration = pd.to_datetime(d.Expiration, format='%d-%m-%y')

    for entry in d.iterrows():
        entry = entry[1]
        add_document(document=entry.Item, expiry=entry.Expiration)

if __name__ == '__main__':
    main()