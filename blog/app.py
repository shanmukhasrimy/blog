from flask import Flask,render_template,request,redirect,url_for
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",password="system",database="flaskblog")
with mysql.connector.connect(host="localhost",user="root",password="system",database="flaskblog"):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("create table if not exists registrationforms(username varchar(50) primary key, mobile varchar(40) unique,email varchar(50) unique,address varchar(50),password varchar(20))")
    cursor.execute("create table if not exists loginform(username varchar(40) primary key,password varchar(30))")
app=Flask(__name__)
@app.route("/")
def home():
    return "homepage of blog"

@app.route("/reg", methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into registrationforms values(%s,%s,%s,%s,%s)',[username,mobile,email,address,password])
        mydb.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from regisrationforms where username=%s && password=%s',[username,password])
        data=cursor.fetchone()[0]
        print(data)
        cursor.close()
        if data==1:
            return redirect(url_for('home'))
        else:
            return "invalid username and password"
    return render_template("login.html")
app.run()