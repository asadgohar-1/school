
import os
from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy import or_
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin

from flask_bcrypt import Bcrypt
from flask_uploads import configure_uploads, UploadSet, DOCUMENTS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage    

import random


myApp = Flask(__name__)

myApp.secret_key="Thisisasecret!"

project_dir = os.path.abspath(os.path.dirname(__file__))
print("=" * 100)

database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))
myApp.config["SQLALCHEMY_DATABASE_URI"] = database_file
myApp.config[" SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(myApp)

bcrypt = Bcrypt(myApp)
login_manager = LoginManager()
login_manager.init_app(myApp)


myApp.config['UPLOADED_DOCUMENTS_DEST'] = "upload"
myApp.config['UPLOADED_DOCUMENTS_ALLOW'] = ['pdf', 'png', 'jpg', 'jpeg','mp4','mov','wmv','avi','mkv','webm']
docs = UploadSet('documents', DOCUMENTS)
configure_uploads(myApp, docs)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30),unique=True, nullable=False)
    phone= db.Column(db.String(30), nullable=False)
    Email = db.Column(db.String(30), nullable=False)
    organiantion = db.Column(db.String(100))
    password=db.Column(db.String(100), nullable=False)
    role_id=db.Column(db.Integer, db.ForeignKey('role.role_id'))
    user_id_media = db.relationship("Media", backref="user_id_media")
   


class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_type=db.Column(db.String(100), nullable=False)
    user_role_id = db.relationship("User", backref="user_role_id")


class Faq(db.Model):
    faq_id = db.Column(db.Integer, primary_key=True)
    question=db.Column(db.String(100), nullable=False)
    answer=db.Column(db.String(100), nullable=False)
    faq_id_book = db.relationship("Book", backref="faq_id_book")

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    autor_name=db.Column(db.String(100), nullable=False)
    title=db.Column(db.String(100), nullable=False)
    year=db.Column(db.String(100), nullable=False)
    published=db.Column(db.String(100), nullable=False)
    book_data=db.Column(db.String(100), nullable=False)
    cover=db.Column(db.String(100), nullable=False)
    faq_id=db.Column(db.Integer, db.ForeignKey('faq.faq_id'))


class Media(db.Model):
   
    media_id=db.Column(db.Integer, primary_key=True)
    role_type=db.Column(db.String(100), nullable=False)
    book_id=db.Column(db.Integer,db.ForeignKey('book.book_id'))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))



class Contact(db.Model):
   
    contact_id=db.Column(db.Integer, primary_key=True)
    phone= db.Column(db.String(30), nullable=False)
    Email = db.Column(db.String(30), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))




@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@myApp.route("/")
def home():
    return "i'm running"

@myApp.route('/db_create',methods=["POST","GET"])
def db_create():
    # try:
        db.create_all()
        return "done"
    # except:
    #     return "400"
@myApp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return "already login" 
    if request.method == 'POST':
        Email = request.form["Email"]
        password1 = request.form["password"]
       

        user = User.query.filter_by(Email=Email).first()
        if user:
            if bcrypt.check_password_hash(user.password, password1):
                remember = True
                # if rememberme == "True":
                #     remember = True
                # print(remember)
                login_user(load_user(user.id), remember)
                return "200"
             
            else:

                return "Invalid Passowrd"
        else:
            return "Invalid Email"

    return "404"




@myApp.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        user = User()
        user1 = User.query.all()
        email = request.form["email"]
        user.user_name = request.form["name"]
        user.password = bcrypt.generate_password_hash(request.form["password"]).decode('utf-8')
        user.organiantion = request.form["organiantion"]   
        user.phone=request.form["phone"]
        user.role_id=request.form["role_id"]
        
        for u in user1:
            if u.Email == email:
               return "Email Exits"
        user.Email = email
        db.session.add(user)
        db.session.commit()
        
        return "200"
    else:
        role_id=Role.query.all()
        ids=[]
        for i in role_id:
            ids.append(i.role_id)
        dic={}
        dic["role_id"]=ids
        return dic

@myApp.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        if current_user.is_authenticated:
            c = Contact()
            
            c.Email = request.form["email"]
            c.phone = request.form["phone"]
            c.user_id = current_user.id
           
        
       
            db.session.add(c)
            db.session.commit()
        
        return "200"
        
# @myApp.route('/contact', methods=["POST", "GET"])
# def contact():
#     if request.method == "POST":
#         if current_user.is_authenticated:
#             c = Contact()
            
#             c.Email = request.form["email"]
#             c.phone = request.form["phone"]
#             c.user_id = current_user.id
           
        
       
#             db.session.add(c)
#             db.session.commit()
        
#         return "200"
        
# @myApp.route('/contact', methods=["POST", "GET"])
# def contact():
#     if request.method == "POST":
#         if current_user.is_authenticated:
#             c = Contact()
            
#             c.Email = request.form["email"]
#             c.phone = request.form["phone"]
#             c.user_id = current_user.id
           
        
       
#             db.session.add(c)
#             db.session.commit()
        
#         return "200"
        
@myApp.route('/faq', methods=["POST", "GET"])
def faq():
    
        if current_user.is_authenticated:
            f = Faq.query.all()
            dic={}
            for i in f:
                dic[i.question]=i.answer
            
        
            return dic
@myApp.route('/add_faq', methods=["POST", "GET"])
def add_faq():
    if request.method == "POST":
        if current_user.is_authenticated:
            f = Faq()
            
            f.question = request.form["question"]
            f.answer = request.form["answer"]
            
        
       
            db.session.add(f)
            db.session.commit()
        
            return "200"
        
@myApp.route('/books', methods=["POST", "GET"])


def books():
    
        if current_user.is_authenticated:
            f = Book.query.all()
            arr=[]
            dic={}
            dic1={}
            for i in f:
                dic["autor_name"]=i.autor_name
                dic["title"]=i.title
                dic["year"]=i.year
                dic["published"]=i.published
                dic["cover"]=i.cover
                dic["book_data"]=i.book_data
                arr.append(dic)
            dic1["booki_info"]=arr
        
            return dic1


@myApp.route('/add_book', methods=["POST", "GET"])
def add_book():
    if request.method == "POST":
        if current_user.is_authenticated:
            b = Book()
            nrandom = random.randint(0,99999999)
            
            b.autor_name = request.form["autor_name"]
            b.title = request.form["title"]
            b.year = request.form["year"]
            b.published = request.form["published"]
            cover = request.files["cover"]
            filename = docs.save(cover, f'books/{b.autor_name}/cover/',f"{str(nrandom)}{cover.filename}")
            b.cover = docs.url(filename)
            book_data=request.files["book_data"]
            filename = docs.save(book_data, f'books/{b.autor_name}/book_data/',f"{str(nrandom)}{book_data.filename}")
            b.book_data = docs.url(filename)
            b.faq_id=request.form["faq_id"]
           
        
       
            db.session.add(b)
            db.session.commit()
        
        return "200"
    else:
        faq=Faq.query.all()
        ids=[]
        for i in faq:
            ids.append(i.faq_id)
        dic={}
        dic["faq_ids"]=ids
        return dic
      


   

@myApp.route('/logout')
def log_out():
    logout_user()
    return "done"
 

if __name__ == '__main__':
    myApp.run(debug=True)