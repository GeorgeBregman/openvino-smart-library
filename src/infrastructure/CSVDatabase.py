import csv # модуль для работы с csv-файлами

from datetime import datetime

from IDatabaseInterfaces import IDatabaseBRM, IDatabaseAuthService, IDatabaseFRM, IDatabaseGUI # импорт всех интерфейсов
from Data_types.Book import Book
from Data_types.User import User
from Data_types.Role import Role
from Data_types.Author import Author
from Data_types.Model import Model

# ПРИМЕЧАНИЕ: для корректной работы методов оформляйте строки в БД правильно.
# При записи любых данных в файлы БД вручную обязательно в конце сделать перевод строки на новую!

path = "infrastructure/Database/"

# внешняя функция для подсчёта строк в файле
def NumOfLines(file):
    lines = 0
    for line in open(file):
        lines = lines + 1
    return lines


class CSVDatabase(IDatabaseBRM, IDatabaseAuthService, IDatabaseFRM, IDatabaseGUI):
    def GetBookCovers(self):
        FileBooksR = open(path + "Books/Books.csv", newline = '')
        FileAuthorsR = open(path + "Books/Authors.csv", newline = '')
        FileAuthorshipR = open(path + "Books/Authorship.csv", newline = '')
        book = []
        authors = []
        readerBooks = csv.DictReader(FileBooksR, delimiter = ',')
        readerAuthorship = csv.DictReader(FileAuthorshipR, delimiter = ',')
        readerAuthors = csv.DictReader(FileAuthorsR, delimiter = ',')
        # захожу в цикл по строкам файла Books.csv
        for lineBooks in readerBooks:
            # захожу в цикл по строкам файла Authorship.csv с фиксированным значением book_id
            FileAuthorshipR.seek(0) # возвращаю указатель в начало файла
            for lineAuthorship in readerAuthorship:
                # нахожу нужные(ый) author_id
                if (lineAuthorship["book_id"] == lineBooks["book_id"]):
                    # захожу в цикл по строкам файла Authors.csv с фиксированным значением author_id
                    FileAuthorsR.seek(0) # возвращаю указатель в начало файла
                    for lineAuthors in readerAuthors:
                        # имея author_id нахожу нужного автора и добавляю его в authors[]
                        if (lineAuthorship["author_id"] == lineAuthors["author_id"]):
                            authors.append(Author(lineAuthors["author_id"], lineAuthors["first_name"], lineAuthors["last_name"], lineAuthors["middle_name"]))
                            break
            new_list = authors.copy() # новый список для устранения проблем с памятью 
            book.append(Book(lineBooks["book_id"], lineBooks["file_path"], lineBooks["title"], lineBooks["year"], lineBooks["publisher"], new_list))
            authors.clear()
        
        FileBooksR.close()
        FileAuthorsR.close()
        FileAuthorshipR.close()
        return book
    
    
    def AddUser(self, user):
        FileUsersR = open(path + "Users/Users.csv", newline = '')
        FileUsersW = open(path + "Users/Users.csv", "a", newline = '') # "a" - дозапись в файл, "w" - перезапись файла
        reader = csv.DictReader(FileUsersR, delimiter = ',')
        # если такой пользователь уже есть в базе, то вернуть -1
        for line in reader:
            if ((user.first_name == line["first_name"]) and (user.last_name == line["last_name"]) and (user.middle_name == line["middle_name"]) and (user.phone == line["phone"])):
                FileUsersR.close()
                FileUsersW.close()
                return -1
        new_user_id = NumOfLines(path + "Users/Users.csv") # id нового пользователя = числу строк в файле Users.csv
        #
        fieldnames = ['user_id', 'phone', 'first_name', 'last_name', 'middle_name']
        writer = csv.DictWriter(FileUsersW, fieldnames = fieldnames, delimiter = ',')
        writer.writerow({'user_id': new_user_id, 'phone': user.phone, 'first_name': user.first_name, 'last_name': user.last_name, 'middle_name': user.middle_name})
        
        FileUsersR.close()
        FileUsersW.close()
        return new_user_id
    
    
    def GetUser(self, user_id):
        FileUsersR = open(path + "Users/Users.csv", newline = '')
        FileUserRoleR = open(path + "Users/UserRole.csv", newline = '')
        FileRolesR = open(path + "Users/Roles.csv", newline = '')
        # ищу пользователя по user_id
        reader = csv.DictReader(FileUsersR, delimiter = ',')
        user = User()
        for i, line in enumerate(reader, 1):
            if (i == user_id):
                user = User(line["user_id"], line["phone"], line["first_name"], line["last_name"], line["middle_name"])
                break
        reader = csv.DictReader(FileUserRoleR, delimiter = ',')
        role_id = 0
        # зная user_id, нахожу соответсвующее значение role_id
        for i, line in enumerate(reader, 1):
            if (i == user_id):
                role_id = int(line["role_id"])
                break
        # зная role_id, нахожу полную информацию об этой роли
        reader = csv.DictReader(FileRolesR, delimiter = ',')
        role = Role()
        for i, line in enumerate(reader, 1):
            if (i == role_id):
                role = Role(line["role_id"], line["description"])
                break
        
        FileUsersR.close()
        FileUserRoleR.close()
        FileRolesR.close()
        return (user, role) # tuple()
    
    
    def GetTrainedModel(self, name_model):
        FileModelsR = open(path + "Users/Models.csv", newline = '')
        reader = csv.DictReader(FileModelsR, delimiter = ',')
        for line in reader:
            if (name_model == line["name_model"]):
                return line["file_path"]
            
        FileModelsR.close()
        return "There is not such a model"
    
    
    def AddModel(self, model):
        FileModelsW = open(path + "Users/Models.csv", "a", newline = '')
        fieldnames = ['model_id', 'file_path', 'name_model']
        writer = csv.DictWriter(FileModelsW, fieldnames = fieldnames, delimiter = ',')
        writer.writerow({'model_id': model.model_id, 'file_path': model.file_path, 'name_model': model.name_model})
        
        FileModelsW.close()
        return model.model_id
    
    
    def AddBook(self, book):
        FileBooksR = open(path + "Books/Books.csv", newline = '')
        # если такая книга уже есть, то вернуть -1
        readerBooks = csv.DictReader(FileBooksR, delimiter = ',')
        for line in readerBooks:
            # file_path не сравниваю, т.к. могут быть 2 разных фото одной книги
            if ((book.title == line["title"]) and (book.year == line["year"]) and (book.publisher == line["publisher"])):
                FileBooksR.close()
                return -1
        FileBooksW = open(path + "Books/Books.csv", "a", newline = '')
        FileAuthorshipW = open(path + "Books/Authorship.csv", "a", newline = '')
        FileAuthorsR = open(path + "Books/Authors.csv", newline = '')
        FileAuthorsW = open(path + "Books/Authors.csv", "a", newline = '')
        new_book_id = NumOfLines(path + "Books/Books.csv") # id новой книги = числу строк в файле Books.csv
        # в таблицу книг дописываю одну новую:
        fieldnamesBooks = ['book_id', 'file_path', 'title', 'year', 'publisher']
        writerBooks = csv.DictWriter(FileBooksW, fieldnames = fieldnamesBooks, delimiter = ',')
        writerBooks.writerow({'book_id': new_book_id, 'file_path': book.file_path, 'title': book.title, 'year': book.year, 'publisher': book.publisher})
        # 
        readerAuthors = csv.DictReader(FileAuthorsR, delimiter = ',')
        fieldnamesAuthors = ['author_id', 'first_name', 'last_name', 'middle_name']
        writerAuthors = csv.DictWriter(FileAuthorsW, fieldnames = fieldnamesAuthors, delimiter = ',')
        fieldnamesAuthorship = ['book_id', 'author_id']
        writerAuthorship = csv.DictWriter(FileAuthorshipW, fieldnames = fieldnamesAuthorship, delimiter = ',')
        for aut in book.authors:
            new_author_id = 0
            for line in readerAuthors:
                # проверяю, есть ли в файле с Authors.csv, автор, который написал книгу, которую мы добавляем
                if ((aut.first_name == line["first_name"]) and (aut.last_name == line["last_name"]) and (aut.middle_name == line["middle_name"])):
                    # если да, то его id будет ассоциироваться с id книги, которую мы добавляем
                    new_author_id = line["author_id"]
            # если нет, то вычислим новый author_id и занесём автора в базу
            if (new_author_id == 0):
                new_author_id = NumOfLines(path + "Books/Authors.csv")
                writerAuthors.writerow({'author_id': new_author_id, 'first_name': aut.first_name, 'last_name': aut.last_name, 'middle_name': aut.middle_name})
            writerAuthorship.writerow({'book_id': new_book_id, 'author_id': new_author_id})
        
        FileBooksR.close()
        FileBooksW.close()
        FileAuthorsR.close()
        FileAuthorsW.close()
        FileAuthorshipW.close()
        return new_book_id
    
    
    def GetAllUsers(self):
        FileUsersR = open(path + "Users/Users.csv", newline = '')
        reader = csv.DictReader(FileUsersR, delimiter = ',')
        user = []
        for line in reader:
            user.append(User(line["user_id"], line["phone"], line["first_name"], line["last_name"], line["middle_name"]))
        
        FileUsersR.close()
        return user
    
    
    def GetAllBooks(self):
        FileBooksR = open(path + "Books/Books.csv", newline = '')
        FileAuthorsR = open(path + "Books/Authors.csv", newline = '')
        FileAuthorshipR = open(path + "Books/Authorship.csv", newline = '')
        book = []
        authors = []
        readerBooks = csv.DictReader(FileBooksR, delimiter = ',')
        readerAuthorship = csv.DictReader(FileAuthorshipR, delimiter = ',')
        readerAuthors = csv.DictReader(FileAuthorsR, delimiter = ',')
        # захожу в цикл по строкам файла Books.csv
        for lineBooks in readerBooks:
            # захожу в цикл по строкам файла Authorship.csv с фиксированным значением book_id
            FileAuthorshipR.seek(0) # возвращаю указатель в начало файла
            for lineAuthorship in readerAuthorship:
                # нахожу нужные(ый) author_id
                if (lineAuthorship["book_id"] == lineBooks["book_id"]):
                    # захожу в цикл по строкам файла Authors.csv с фиксированным значением author_id
                    FileAuthorsR.seek(0) # возвращаю указатель в начало файла
                    for lineAuthors in readerAuthors:
                        # имея author_id нахожу нужного автора и добавляю его в authors[]
                        if (lineAuthorship["author_id"] == lineAuthors["author_id"]):
                            authors.append(Author(lineAuthors["author_id"], lineAuthors["first_name"], lineAuthors["last_name"], lineAuthors["middle_name"]))
                            break
            new_list = authors.copy() # новый список для устранения проблем с памятью 
            book.append(Book(lineBooks["book_id"], lineBooks["file_path"], lineBooks["title"], lineBooks["year"], lineBooks["publisher"], new_list))
            authors.clear()
        
        FileBooksR.close()
        FileAuthorsR.close()
        FileAuthorshipR.close()
        return book
    
    def GetBorrowedBooks(self):
        # HELP!
        # пытался реализовать все циклы по строкам файлов при помощи enumerate в целях экономии времени работы методов, но возникают проблемы с возвратом указателя в начало файла
        FileBooksR = open(path + "Books/Books.csv", newline = '')
        FileUsersR = open(path + "Users/Users.csv", newline = '')
        FileAuthorsR = open(path + "Books/Authors.csv", newline = '')
        FileAuthorshipR = open(path + "Books/Authorship.csv", newline = '')
        FileReadersR = open(path + "Readers.csv", newline = '')
        user = []
        book = []
        date1 = []
        date2 = []
        authors = []
        readerReaders = csv.DictReader(FileReadersR, delimiter = ',')
        readerUsers = csv.DictReader(FileUsersR, delimiter = ',')
        readerBooks = csv.DictReader(FileBooksR, delimiter = ',')
        readerAuthorship = csv.DictReader(FileAuthorshipR, delimiter = ',')
        readerAuthors = csv.DictReader(FileAuthorsR, delimiter = ',')
        # захожу в цикл по строкам файла Readers.csv
        for lineReaders in readerReaders:
            # захожу в цикл по строкам файла Books.csv с фиксированным значением user_id
            FileUsersR.seek(0) # возвращаю указатель в начало файла
            for lineUsers in readerUsers:
                # нахожу нужного пользователя и добавляю его данные в user[]
                if (lineUsers["user_id"] == lineReaders["user_id"]):
                    user.append(User(lineUsers["user_id"], lineUsers["phone"], lineUsers["first_name"], lineUsers["last_name"], lineUsers["middle_name"]))
                    break
            # захожу в цикл по строкам файла Authorship.csv с фиксированным значением book_id
            FileAuthorshipR.seek(0) # возвращаю указатель в начало файла
            for lineAuthorship in readerAuthorship:
                # нахожу нужные(ый) author_id
                if (lineAuthorship["book_id"] == lineReaders["book_id"]):
                    # захожу в цикл по строкам файла Authors.csv с фиксированным значением author_id
                    FileAuthorsR.seek(0) # возвращаю указатель в начало файла
                    for lineAuthors in readerAuthors:
                        # имея author_id нахожу нужного автора и добавляю его в authors[]
                        if (lineAuthorship["author_id"] == lineAuthors["author_id"]):
                            authors.append(Author(lineAuthors["author_id"], lineAuthors["first_name"], lineAuthors["last_name"], lineAuthors["middle_name"]))
                            break
            # добавляю нужную дату взятия книги в date1[]
            date1.append(lineReaders["borrow_date"])
            # добавляю нужную дату сдачи книги в date2[]
            date2.append(lineReaders["return_date"])
            #
            # захожу в цикл по строкам файла Books.csv с фиксированным значением book_id
            FileBooksR.seek(0) # возвращаю указатель в начало файла
            for lineBooks in readerBooks:
                # нахожу нужную книгу
                if (lineBooks["book_id"] ==  lineReaders["book_id"]):
                    # добавляю её в book[]
                    new_list = authors.copy() # новый список для устранения проблем с памятью 
                    book.append(Book(lineBooks["book_id"], lineBooks["file_path"], lineBooks["title"], lineBooks["year"], lineBooks["publisher"], new_list))
                    authors.clear()
                    break
                
        FileUsersR.close()
        FileBooksR.close()
        FileAuthorsR.close()
        FileAuthorshipR.close()
        FileReadersR.close()
        return (book, date1, date2, user) # tuple()
        
    def ChangeBookStatus(self, user_id, book_id, status):
        FileReadersW = open(path + "Readers.csv", "a", newline = '')
        # статус = 1 - взять книгу
        # статус = 2 - сдать книгу
        # return_date == -1 - книга не сдана
        fieldnames = ['user_id', 'book_id', 'borrow_date', 'return_date']
        writer = csv.DictWriter(FileReadersW, fieldnames = fieldnames, delimiter = ',')
        if (status == 1):
            writer.writerow({'user_id': user_id, 'book_id': book_id, 'borrow_date': datetime.strftime(datetime.now(), "%d%m"), 'return_date': "-1"})
        if (status == 2):
            """HELP!"""
            # не могу найти способ перезаписать конкретную ячейку без перезаписи всего файла
        
        FileReadersW.close()

if __name__ == "__main__":
    """main"""