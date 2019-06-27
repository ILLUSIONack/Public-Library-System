import json
import os


class PublicLibrary():
    def __init__(self):
        self.catalog = Catalog()
        self.loanAdministration = LoanAdministration()

    def makeBackup(self):
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


    def addCustomer(self,customer):
        self.customers.append(customer)

    def checkAvailabilityBook(self,book):
        pass

    def borrowBook(self,book):
        pass

    def initCustomers(self):
        pass


class Person():
    def __init__(self,gn,ns,gn,surn,ad,zip,cty,email,user,tele):
        self.gender = gn
        self.nameSet = ns
        self.givenName = gn
        self.surName = ln
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
            A.personid +=1
            return A.personid

    def __init__(self,gn,ns,gn,surn,ad,zip,cty,email,user,tele):
        super().__init__(gn,ns,gn,surn,ad,zip,cty,email,user,tele)
        self.id = Customer.gennumber()
        books = []

    def borrowBook(self,book):
        //append to books []
        pass
    
    def returnBook(self,book):
        pass
    
    def showBorrowedBooks(self):
        //loop array books
        pass


class Author(Person):
    def __init__(self):
        super().__init__(sn,ln,ad,zip,cty,email,tele)

    def authorName():
        pass


class Book():
    bookid = 12345
    @staticmethod
    def gennumber():
            A.bookid +=1
            return A.bookid
        
    def __init__(self, title,author):
            self.bookid = A.gennumber()
            self.title = title
            self.author = []


class Catalog(Book):
    def __init__(self):
        self.books = []
        self.bookItems = []
        self.index = {}
        self.availableBookItems = {}

    def searchBook(self,book):
        pass

    def addBookItem(self,bookitem):
        pass
    
    def initBooks(self):


class BookItem(Book):
    def __init__(self,title):
        super().__init__(title,author)


class LoanItem():
    pass