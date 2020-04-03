# flask doesnot come with database. as it is light weight. so we have to use external third party one.(sqlalchemy)
# pip install flask-sqlalchemy
# from app import db and db.create_all() at python shell it is used to setup the database. create_all() creates the db as specified in the program i mean
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
# specifying the location of database. we are using sqlite because it is easy and it is store locally. we can also use mysql and postgre
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db' #///-relative path and ////-absolute path
db=SQLAlchemy(app) # creating the database. now we have the database i.e linking out app and the database
# testing database
'''>>> from app import db
>>> db.create_all()
>>> from app import BlogPost 
>>> BlogPost.query_all()
[]
>>> db.session.add(BlogPost(title='Blog Post 1',content='Content of Blog Post 1',author='Ilyas'))
>>> BlogPost.query.all()
[<BlogPost 1>]
>>> db.session.add(BlogPost(title='Blog Post 2',content='Content of Blog Post 2',author='Ahmed'))
[<BlogPost 1>, <BlogPost 2>]
>>> BlogPost.query.all()[0].id
1
>>> BlogPost.query.all()[0].title
'Blog Post 1'
>>> BlogPost.query.all()[0].author
'Ilyas'
>>> BlogPost.query.all()[0].content
'Content of Blog Post 1'
>>> BlogPost.query.all()[0].date_posted
datetime.datetime(2020, 4, 2, 19, 22, 58, 927345)
>>> BlogPost.query.all()[1].author
'Ahmed'
'''
class BlogPost(db.Model):#  BlogPost inherits the db Model. so i think BlogPost is know database
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(20),nullable=False,default='N/A')
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    # this all are 
    def __repr__(self): # it prints whenever a blog posts is created
        return 'Blog Post'+str(self.id)
# list of dictionaries
all_posts=[
    {
        'title':'post1',
        'content':'this is the content of post1',
        'author':'Ilyas'
    },
    {
        'title':'post2',
        'content':'this is the content of post2'
    }
]
#var="hello"
@app.route('/')
def hello():
    return render_template('first.html')
@app.route('/posts',methods=['GET','POST']) # if we wont specify the methods then by default it is get method. we cant post it.
# sending the data from the .py file to html  file. and dynamic content is changed in html where as css and js is static

def posts():
    #return render_template('post.html',posts=var)
    #return render_template('post.html',posts=all_posts) # posts is a variable that is passed to post.html file and all_posts is data
    if request.method=='POST':
            post_title=request.form['title']
            post_content=request.form['content']
            post_author=request.form['author']
            new_post=BlogPost(title=post_title,content=post_content,author=post_author)
            db.session.add(new_post) # it is saved temperarily. #it is used to add the value in the database or insertion
            db.session.commit()# it is saved permenantly 
            return redirect('/posts')
    else:
        all_posts=BlogPost.query.order_by(BlogPost.date_posted).all() # it is used to extract the data from database
        return render_template('postwi.html',posts=all_posts)
@app.route('/posts/delete/<int:id>')
def delete(id):
    post=BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    post=BlogPost.query.get_or_404(id)
    if request.method=='POST':
        post.title=request.form['title']
        post.content=request.form['content']
        post.author=request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html',post=post)   


if __name__=="__main__":
    app.run(debug=True)