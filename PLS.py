import json
import os
import csv

class PublicLibrary():
    def __init__(self):
        self.catalog = Catalog()
        self.loanAdministration = LoanAdministration()
        self.catalog.initBooks()
        self.loanAdministration.initCustomers()

    def makeBackup(self, namefile):
        with open("./data/data.json", "r") as fromFile, open("./backup/" + namefile + ".json", "w") as to:
            to.write(fromFile.read())
            fromFile.close()
            to.close()
            print("Successfully backed up the library!")

    def restoreBackup(self,name):
        files = os.listdir("./backup/")
        for file in files:
            file = file.strip(".json")
            if file == name:
                os.remove("./data/data.json")
                with open("./backup/" + name + ".json", "r") as fromFile, open("./data/data.json", "w") as to:
                    to.write(fromFile.read())
                    fromFile.close()
                    to.close()
                    return "Successfully restored the backup file " + name
        return "Failed to restore the backup file " + name


class LoanAdministration():
    def __init__(self):
        self.loanItem = []
        self.customers = []
        self.loanItemPerBook = {}

    def addCustomer(self,gnd,ns,gn,surn,ad,zip,cty,email,user,tele):
        self.customers.append(Customer(gnd,ns,gn,surn,ad,zip,cty,email,user,tele))

    def checkAvailabilityBook(self,catalog,book):
        if book in catalog.bookItems:
            print(catalog.bookItems[catalog.bookItems.index(book)].getTitle()+", is available!")
        else:
            print("The book is not available.")

    def borrowBook(self, catalog, customer, book):
        self.loanItem.append(book)
        catalog.bookItems.remove(book)
        lender = self.customers.index(customer)
        self.customers[lender].addBook(book)
        print("Customer " + self.customers[lender].getCustomerName() + " borrowed " +
              self.loanItem[self.loanItem.index(book)].bookTitle())

    def returnBook(self, catalog, customer, book):
        self.loanItem.remove(book)
        catalog.bookItems.append(book)
        lender = self.customers.index(customer)
        self.customers[lender].removeBook(book)
        print("Customer " + self.customers[lender].getCustomerName() + " returned " +
               catalog.bookItems[catalog.bookItems.index(book)].bookTitle())


    def initCustomers(self):
        with open('./Code files/customers.csv','r') as csv_file:
            read = csv.reader(csv_file)
            for line in read:
                self.customers.append(Customer(line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10]))
        print("Customers loaded...")
        print("Welcome to the Public Library System!")


class Person():
    def __init__(self,gnd,ns,gn,surn,ad,zip,cty,email,user,tele):
        self.gender = gnd
        self.nameSet = ns
        self.givenName = gn
        self.surName = surn
        self.adress = ad
        self.zipCode = zip
        self.city = cty
        self.email = email
        self.userName = user
        self.telefoon = tele


class Customer(Person):
    personid = 12345
    @staticmethod
    def gennumber():
            Customer.personid +=1
            return Customer.personid

    def __init__(self,gnd,ns,gn,surn,ad,zip,cty,email,user,tele):
        super().__init__(gnd,ns,gn,surn,ad,zip,cty,email,user,tele)
        self.id = Customer.gennumber()
        self.books = []

    def getCustomerName(self):
        return self.givenName
    
    def showBorrowedBooks(self):
        return self.books
    
    def addBook(self,book):
        self.books.append(book)
    
    def removeBook(self,book):
        self.books.remove(book)



class Author(Person):
    def __init__(self,gn,gnd='',ns='',surn='',ad='',zip='',cty='',email='',user='',tele=''):
        super().__init__(gnd,ns,gn,surn,ad,zip,cty,email,user,tele)

    def authorName(self):
        return self.givenName


class Book():
        
    def __init__(self, author,country,imageLink,language,link,pages,title,year):
            self.author = []
            self.addAuthor(author)
            self.country = country
            self.imageLink = imageLink
            self.language = language
            self.link = link
            self.pages = pages
            self.title = title
            self.year = year

    def addAuthor(self,author):
        self.author.append(Author(author))
    
    def bookTitle(self):
        return self.title

class Catalog(Book):
    def __init__(self):
        self.books = []
        self.bookItems = []
        self.index = {}
        self.availableBookItems = {}

    def searchBook(self, title):
        books_found = []
        print("Results for book (" + title + ")...")
        for book in self.bookItems:
            if book.isSearchedBook(title):
                books_found.append(book)
        if len(books_found) < 1:
            print("No Books Found!")
        else:
            for b in books_found:
                print("- " + b.title)

    def addBookItem(self,author,country,imageLink,language,link,pages,title,year):
        self.bookItems.append(BookItem(author,country,imageLink,language,link,pages,title,year))
    
    def initBooks(self):
        with open('./Code files/bookset.json','r') as json_file:
            read_books = json.load(json_file)
            for x in read_books:
                self.books.append(Book(x['author'],x['country'],x['imageLink'],x['language'],x['link'],x['pages'],x['title'],x['year']))
                self.bookItems.append(BookItem(x['author'],x['country'],x['imageLink'],x['language'],x['link'],x['pages'],x['title'],x['year'],BookItem.gennumber()))
            print("Books loaded...")
           

class BookItem(Book):
    bookid = 0
    @staticmethod
    def gennumber():
        BookItem.bookid +=1
        return BookItem.bookid

    def __init__(self,author,country,imageLink,language,link,pages,title,year,ISBN):
        super().__init__(author,country,imageLink,language,link,pages,title,year)
        self.ISBN = ISBN

    def getTitle(self):
        return self.title
    
    def getAuthor(self):
        return self.author[0].authorName()

    def isSearchedBook(self, titleLookup):
        return True if self.title.lower().startswith(titleLookup.lower()) else False
    
    def getISBN(self):
        return self.ISBN


class LoanItem(Book):
    def __init__(self,author,country,imageLink,language,link,pages,title,year):
        super().__init__(author,country,imageLink,language,link,pages,title,year)
    
    def getTitle(self):
        return self.title
    
    def getAuthor(self):
        return self.author[0].authorName()
        

if __name__ == "__main__":
    PublicLibrary = PublicLibrary()

    #Customer Valentin from customers.csv and Book 'Fairy Tales' from bookset.json
    customer = PublicLibrary.loanAdministration.customers[3]
    book = PublicLibrary.catalog.bookItems[1]
    theDevineComedyBook = PublicLibrary.catalog.bookItems[2]

    #Search for a book called 'Things Fall Apart'
    PublicLibrary.catalog.searchBook("Things Fall Apart")

    #Borrow book test, lend Customer 1 the book called fairy tales
    PublicLibrary.loanAdministration.borrowBook(PublicLibrary.catalog, customer, book)

    #Re-searching the FairyTails book in the bookitems, book cannot be found!
    PublicLibrary.catalog.searchBook("Fairy tales")

    #Checking for book availability, 'Fairy tales'
    PublicLibrary.loanAdministration.checkAvailabilityBook(PublicLibrary.catalog,book)

    #Check if customer has book Fairy tails, Yes they have it!
    print("Customer book's: " + customer.showBorrowedBooks()[0].bookTitle())

    #Customer Valentin returning the book Fairy Tales
    PublicLibrary.loanAdministration.returnBook(PublicLibrary.catalog, customer, book)
    
   #Re-searching the FairyTails book in the bookitems, book found again!
    PublicLibrary.catalog.searchBook("Fairy tales")

    #Checking for book availability, 'The Devine Comedy'
    PublicLibrary.loanAdministration.checkAvailabilityBook(PublicLibrary.catalog,theDevineComedyBook)

    #Checking if BootItem has ISBN number
    print(PublicLibrary.catalog.bookItems[0].getISBN())
