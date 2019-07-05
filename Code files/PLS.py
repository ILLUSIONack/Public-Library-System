import json
import csv


class PublicLibrary():
    def __init__(self):
        self.catalog = Catalog()
        self.catalog.initBooks()
        self.loanAdministration = LoanAdministration(self.catalog)
        self.loanAdministration.initCustomers()

    def makeBackup(self, namefile):
        pass

    def restoreBackup(self, name):
        pass


class LoanAdministration():
    def __init__(self, catalog):
        self.loanItems = []
        self.customers = []
        self.catalog = catalog

    """
    Adds a customer to the current customer array state and appends the new customer to the customer.csv file
    """
    def addCustomer(self, customer):
        self.customers.append(customer)
        with open('customers.csv', mode='a', newline='') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow([customer.id, customer.gender, customer.nameSet, customer.givenName,
                                      customer.surName, customer.adress, customer.zipCode, customer.city,
                                      customer.email, customer.userName, customer.phoneNumber])
            employee_file.close()

    """
    Borrows a book to the given customer, removes it from the current book items and appends it to the loanItems array,
    Also the book that is being borrowed to the customer is being appended in the book array in the customer class.
    """
    def borrowBook(self, customer, bookitem):
        if bookitem in self.catalog.bookItems:
            self.catalog.bookItems.remove(bookitem)
            lender = self.customers.index(customer)
            converted = LoanItem(bookitem.author, bookitem.country, bookitem.imageLink, bookitem.language, bookitem.link, bookitem.pages, bookitem.title, bookitem.year, bookitem.ISBN)
            self.customers[lender].addBook(converted)
            self.loanItems.append(converted)
            print("Customer " + self.customers[lender].getName() + " borrowed " +
                  self.loanItems[self.loanItems.index(converted)].getTitle())

    """
    Loads the customers from the customers.csv file into the customer array in the loanadministration
    """
    def initCustomers(self):
        with open('./Code files/customers.csv', 'r') as csv_file:
            read = csv.reader(csv_file)
            for line in read:
                self.customers.append(
                    Customer(line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10]))
        print("Loaded", len(self.customers), "Customers")


class Person():
    def __init__(self, gender, nameSet, givenName, surName, adress, zipCode, city, email, usernName, phoneNumber):
        self.gender = gender
        self.nameSet = nameSet
        self.givenName = givenName
        self.surName = surName
        self.adress = adress
        self.zipCode = zipCode
        self.city = city
        self.email = email
        self.userName = usernName
        self.phoneNumber = phoneNumber


class Customer(Person):
    personId = 0

    """
    Generates (counts-up) a static identification upon call
    """
    @staticmethod
    def generateIdentification():
        Customer.personId += 1
        return Customer.personId

    def __init__(self, gender, nameSet, givenName, surName, adress, zipCode, city, email, userName, phoneNumber, books=[]):
        super().__init__(gender, nameSet, givenName, surName, adress, zipCode, city, email, userName, phoneNumber)
        self.id = Customer.generateIdentification()
        self.books = books

    """
    Returns the given name of the customer
    """
    def getName(self):
        return self.givenName

    """
    Prints the borrowed books of the customer
    """
    def getBorrowedBooks(self):
        print("Books borrowed of the user (" + self.givenName + ")...")
        for b in self.books:
            print("-", b.title)

    """
    Adds the book to the customer
    """
    def addBook(self, book):
        self.books.append(book)


class Author(Person):
    def __init__(self, givenName, surName='N/A', gender='N/A', nameSet='N/A', adress='N/A', zipCode='N/A', city='N/A', email='N/A', userName='N/A', phoneNumber='N/A'):
        super().__init__(gender, nameSet, givenName, surName, adress, zipCode, city, email, userName, phoneNumber)

    """
    Returns the full name of the author
    """
    def getFullName(self):
        return self.givenName + " " + self.surName


class Book():
    def __init__(self, author, country, imageLink, language, link, pages, title, year):
        self.author = []
        self.author.append(Author(author))
        self.country = country
        self.imageLink = imageLink
        self.language = language
        self.link = link
        self.pages = pages
        self.title = title
        self.year = year

    """
    Returns the title of the book
    """
    def getTitle(self):
        return self.title

    "Returns true if the title matches with one of the book items else it will return false"
    def isSearchedBook(self, titleLookup):
        return True if self.title.lower().startswith(titleLookup.lower()) else False


    "Returns true if the author name matches with one of the book items else it will return false"
    def isSearchedAuthor(self, input):
        for a in self.author:
            author_name = a.getFullName()
            if author_name.lower().startswith(input.lower()):
                return True
        return False



class Catalog(Book):
    def __init__(self):
        self.books = []
        self.bookItems = []
        self.index = {}
        self.availableBookItems = {}

    """
    Prints out the book that are available given by a title or author name.
    """
    def searchBook(self, input):
        books_found = []
        print("Results for (" + input + ")...")
        for book in self.books:
            if book.isSearchedBook(input):
                books_found.append(book)
            elif book.isSearchedAuthor(input):
                books_found.append(book)
        if len(books_found) < 1:
            print("No Books Found!")
        else:
            for b in books_found:
                print("- " + b.title + "")

    """
    Prints out the book that are available given by a title, ISBN or author name.
    """
    def checkAvailability(self, input):
        books_found = []
        print("Results for availability (" + input + ")...")
        for book in self.bookItems:
            if book.isSearchedBook(input):
                books_found.append(book)
            elif book.isSearchedISBN(input):
                books_found.append(book)
            elif book.isSearchedAuthor(input):
                books_found.append(book)
        if len(books_found) < 1:
            print("No Books Found!")
        else:
            for b in books_found:
                print("- " + b.title + " (ISBN: " + str(b.ISBN) + ")")

    """
    Adds a new book to the book array and appends it in the bookset.json file
    """
    def addBook(self, author, country, imageLink, language, link, pages, title, year):
        self.books.append(Book(author, country, imageLink, language, link, pages, title, year))
        with open("./Code files/bookset.json", 'r+') as inputfile:
            data = json.load(inputfile)
            data.append({
                "author": author,
                "country": country,
                "imageLink": imageLink,
                "language": language,
                "link": link,
                "pages": pages,
                "title": title,
                "year": year
            })
            inputfile.seek(0)
            json.dump(data, inputfile)
            inputfile.truncate()
            inputfile.close()
        print("Successfully added the book", title)

    """
    Adds a new book item to the book item array
    """
    def addBookItem(self, author, country, imageLink, language, link, pages, title, year):
        self.bookItems.append(BookItem(author, country, imageLink, language, link, pages, title, year, BookItem.generateISBN()))

    """
    Loads the books from the bookset.json file into the books and bookitems array
    """
    def initBooks(self):
        with open('./Code files/bookset.json', 'r') as json_file:
            read_books = json.load(json_file)
            for x in read_books:
                self.books.append(
                    Book(x['author'], x['country'], x['imageLink'], x['language'], x['link'], x['pages'], x['title'],
                         x['year']))
                for i in range(2):
                    self.bookItems.append(BookItem(x['author'], x['country'], x['imageLink'], x['language'], x['link'], x['pages'],
                             x['title'], x['year'], BookItem.generateISBN()))
        print("Loaded", len(self.books), "Books and", len(self.bookItems), "Book Items!")


class BookItem(Book):
    bookItemIsbn = 0

    """
    Generates (counts-up) a static ISBN upon call
    """
    @staticmethod
    def generateISBN():
        BookItem.bookItemIsbn += 1
        return BookItem.bookItemIsbn

    def __init__(self, author, country, imageLink, language, link, pages, title, year, ISBN):
        super().__init__(author, country, imageLink, language, link, pages, title, year)
        self.ISBN = ISBN

    "Returns true if the isbn matches with one of the book items else it will return false"
    def isSearchedISBN(self, isbn):
        return True if str(self.ISBN) == str(isbn) else False



class LoanItem(BookItem):
    def __init__(self, author, country, imageLink, language, link, pages, title, year, ISBN):
        super().__init__(author, country, imageLink, language, link, pages, title, year, ISBN)


if __name__ == "__main__":
    print("Initiating the library...")
    library = PublicLibrary()
    print("Welcome to the Public Library System!")
    print("Lets start of by declaring our first customer (Valentin)...")
    customer = library.loanAdministration.customers[3]
    print("We have declared a variable for valentin")
    print("Valentin is interested in searching up the book 'The Book Of Job'")
    library.catalog.searchBook("The Book Of Job")
    print("Valentin would now like to check the availibility of 'The Book Of Job'")
    library.catalog.checkAvailability("The Book Of Job")
    print("Valentin also is looking for another book, but he only knows it's ISBN which is '2'")
    library.catalog.checkAvailability("2")
    print("Valentin is now done with searching and would like to borrow the books")
    print("He starts with borrowing the book 'The Book Of Job'")
    the_book_of_job = library.catalog.bookItems[8]
    library.loanAdministration.borrowBook(customer, the_book_of_job)
    print("Let's first take a look at the books that Valentin has borrowed thus far")
    customer.getBorrowedBooks()
    print("Let's now take a look at our book items status and search again for 'The Book Of Job'")
    library.catalog.checkAvailability("The Book Of Job")
    print("As we can see there is only one more book item left for the book 'The Book Of Job'")
    print("Valentin is still interested in borrowing the 'Things Fall Apart' book")
    things_fall_apart = library.catalog.bookItems[1]
    library.loanAdministration.borrowBook(customer, things_fall_apart)
    print("Now let's do the same thing for this book and search it up 'Things Fall Apart'")
    library.catalog.checkAvailability("Things Fall Apart")
    print("The loan administration is stocking up again and it's adding a new book")
    print("Let's first try and search up the book item that the loan administration is going to be adding soon... with the title", 'The End Of Times')
    library.catalog.checkAvailability("The End Of Times")
    print("As you can see no result, the loan administration will now be adding the book")
    library.catalog.addBook("Hamza Fethi", "Netherlands", "images/times-end.jpg", "Dutch", "https://en.wikipedia.org/wiki/Fairy_Tales_Told_for_Children._First_Collection.\n", 433, "The End Of Times", 1750)
    print("Now that we have added the book we can add a book item for this book")
    library.catalog.addBookItem("Hamza Fethi", "Netherlands", "images/times-end.jpg", "Dutch", "https://en.wikipedia.org/wiki/Fairy_Tales_Told_for_Children._First_Collection.\n", 433, "The End Of Times", 1750)
    print("The loan administration has succesfully added a new book and a book item", 'The End Of Times', "Lets try and search it up")
    library.catalog.checkAvailability("The End Of Times")
    print("Lets get back to valentin, he brought with him a friend who would like to register as a new member. His name is 'Gary Veulen'")
    new_customer = Customer("male", "Dutch", "Gary", "Veulen", "Palisanderstraat 43", "3031 CG", "Rotterdam", "garyveulen1998@gmail.com", "GaryVeulen", "06-84211309")
    library.loanAdministration.addCustomer(new_customer)
    print("The loan administration successfully made 'Gary Veulen' a new customer")
    print("Gary is also interested in borrowing the book 'The Book Of Job'")
    library.catalog.checkAvailability("The Book Of Job")
    the_book_of_job_second = library.catalog.bookItems[7]
    library.loanAdministration.borrowBook(new_customer, the_book_of_job_second)
    print("Gary is also looking to borrow the same book for his little sister")
    library.catalog.checkAvailability("The Book Of Job")
    print("Gary is not able to borrow the book as its not available anymore!")
    print("The library will be closing soon so it will be backed up before closing")
    library.makeBackup("backup_first")