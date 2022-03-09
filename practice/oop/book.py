class Book:
    # class attributes (they are shared by all instances of the class, can be manipulated by an instance)
    version = "New"

    # constructor method
    def __init__(self, default_title="Borne Ultimatum"):
        # instance attributes (each instance has its own unique values of the attributes)
        self.title = default_title
        self.pages = None

        """
        private attributes are indicated by __ before the name.
        They should only be accessed by methods within the class def.
        """
        self.__comments = []

    def __repr__(self):
        print("Printing using __repr__")
        return f"Title: {self.title}\nPages: {self.pages}\nComments: {str(self.__comments)}\n"

    def add_comment(self, new_comment):
        self.__comments.append(new_comment)

    def show_info(self):
        print(f"[+] Title: {self.title:>20}")
        print(f"[+] Pages: {str(self.pages):>20}")
        print(f"[+] Version: {self.version:>20}\n")


book_1 = Book()
book_1.show_info()

book_2 = Book("Elden Ring")
book_2.pages = 500
book_2.show_info()

book_3 = Book("Quiet Night")
book_3.pages = 1000
book_3.show_info()
print(book_3)

# __dict__ creates a dictionary copy of the instance
print("Using __dict__")
print(book_3.__dict__)
print("\n")

book_4 = Book()
book_4.add_comment("Outstanding")
print(book_4)


# book_4.__comments.append("Great")
# Since __comments is a private attribute, accessing it like this will cause an error
