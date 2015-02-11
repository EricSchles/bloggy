from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import os
import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

#http://blog.y3xz.com/blog/2012/08/16/flask-and-postgresql-on-heroku

class Blag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	entry = db.Column(db.Text())
	timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
        title = db.Column(db.String(1000))
	def __init__(self,title,entry):
		self.title = title
                self.entry = entry

	def __repr__(self):
		return '<title %r>' % self.title


@app.route("/new_entry")
def new_entry():
	return render_template("new_entry.html")

@app.route("/add",methods=["GET","POST"])
def add_entry():
        title = request.form["title"]
        entry = request.form["entry"]
	blag = Blag(title,entry)
	db.session.add(blag)
	db.session.commit()
        return render_template("index.html")

@app.route("/view_all",methods=["GET","POST"])
def view_all():
        return render_template("blogs.html",posts=Blags.query.all())

@app.route("/view",methods=["GET","POST"])
def view():
        post = request.args.get("post")
        return render_template("viewer.html",title=post.title,entry=post.entry)

if __name__ == '__main__':
	app.run(debug=True)
