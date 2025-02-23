from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'Mani'  # Required for session management

class Book:
    def __init__(self, title, author, stock):
        self.title = title
        self.author = author
        self.stock = stock

class Member:
    def __init__(self, name):
        self.name = name
        self.outstanding_debt = 0

class Library:
    def __init__(self):
        self.books = {}
        self.members = {}

    def add_book(self, title, author, stock):
        if title in self.books:
            self.books[title].stock += stock
        else:
            self.books[title] = Book(title, author, stock)

    def add_member(self, name):
        if name not in self.members:
            self.members[name] = Member(name)

def issue_book(self, title, member_name):
    if title in self.books and self.books[title].stock > 0:
        if member_name in self.members:
            if self.members[member_name].outstanding_debt <= 500:
                self.books[title].stock -= 1
                return True
            else:
                print(f"Cannot issue book. {member_name} has an outstanding debt of Rs.{self.members[member_name].outstanding_debt}.")
    return False

    def return_book(self, title, member_name):
        if title in self.books and member_name in self.members:
            self.books[title].stock += 1
            fee = 50  # Example fee for returning a book
            self.members[member_name].outstanding_debt += fee
            return True
        return False

    def search_book(self, search_term):
        return [book for book in self.books.values() if search_term.lower() in book.title.lower() or search_term.lower() in book.author.lower()]

library = Library()

@app.route('/')
def index():
    return render_template('index.html', books=library.books.values(), members=library.members.values())

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    stock = int(request.form['stock'])
    library.add_book(title, author, stock)
    flash('Book added successfully!')
    return redirect(url_for('index'))

@app.route('/add_member', methods=['POST'])
def add_member():
    name = request.form['name']
    library.add_member(name)
    flash('Member added successfully!')
    return redirect(url_for('index'))

@app.route('/issue_book', methods=['POST'])
def issue_book():
    title = request.form['title']
    member_name = request.form['member_name']
    if library.issue_book(title, member_name):
        flash(f'Book "{title}" issued to {member_name}.')
    else:
        flash('Failed to issue book. Check stock or member debt.')
    return redirect(url_for('index'))

@app.route('/return_book', methods=['POST'])
def return_book():
    title = request.form['title']
    member_name = request.form['member_name']
    if library.return_book(title, member_name):
        flash(f'Book "{title}" returned from {member_name}.')
    else:
        flash('Failed to return book. Check member and book details.')
    return redirect(url_for('index'))

@app.route('/search_book', methods=['POST'])
def search_book():
    search_term = request.form['search_term']
    found_books = library.search_book(search_term)
    return render_template('index.html', books=found_books, members=library.members.values(), search_term=search_term)

if __name__ == '__main__':
    app.run(debug=True)