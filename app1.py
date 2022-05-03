from flask import Flask,render_template,request,url_for,redirect,session
from flask_mail import Mail,Message
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='abc456'
app.config['MYSQL_DB']='flask'

app.config["MAIL_SERVER"]= "smtp.gmail.com"
app.config["MAIL_PORT"]=587
app.config["MAIL_USERNAME"]="bhangeprasad16@gmail.com"
app.config["MAIL_PASSWORD"]="Prasad@234"
app.config["MAIL_USE_TLS"]=True
app.config["MAIL_USE_SSL"]=False


mail=Mail(app)

mysql=MySQL(app)

app.secret_key="Prasadbhange"


@app.route("/fpassword",methods=["GET","POST"])
def fpassword():
	if request.method=="POST":	
		em=request.form["em"]
		usr=request.form["un"]	
		try:
			cursor=mysql.connection.cursor()
			sql="select password from users where username='%s'"	
			cursor.execute(sql%(usr))
			mysql.connection.commit()
			data=cursor.fetchall()
			if len(data)==0:
				return render_template("fpassword.html",msg="user dosn't exists")
			else:
				msg=Message("regarding forgotten password",sender="bhangeprasad16@gmail.com",recipients=[em])
				msg.body="Your password is " + str(data) + "\n \n \nNote:\nIf there is a empty space in the place of password,then you are new user,please signup and create your account. \n \n Thank you!!!"				
				mail.send(msg)
				return render_template("fpassword.html",msg=data)

		except Exception as e:
			return render_template("fpassword.html",msg=e)
	else:
		return render_template("fpassword.html")


@app.route("/logout",methods=["GET","POST"])
def logout():
	session.clear()
	return redirect (url_for("home"))

@app.route("/",methods=["GET","POST"])
def home():
	return render_template ("home.html")

@app.route("/a_admin",methods=["GET","POST"])
def a_admin():
	return render_template ("a_login.html")	

@app.route("/reques",methods=["GET","POST"])
def reques():
	return render_template ("request.html")	


@app.route("/add_admin",methods=["GET","POST"])
def add_admin():
	if request.method=="POST":
		un=request.form["un"]
		pw1=request.form["pw1"]
		pw2=request.form["pw2"]
		if pw1==pw2:
			try:
				#cursor=db.cursor()
				cursor=mysql.connection.cursor()
				sql="insert into admin values('%s','%s')"
				cursor.execute(sql%(un,pw1))
				mysql.connection.commit()
				return render_template("add_admin.html",msg="added successfully")

			except Exception as e:
				mysql.connection.rollback()
				return render_template("add_admin.html",msg="Admin already exists")
		else:
			return render_template("add_admin.html",msg="password did not match")
	else:
		return render_template("add_admin.html")

@app.route("/reque",methods=["GET","POST"])
def reque():
	if request.method=="POST":
		type=request.form["blood_type"]
		loc=request.form["loc"]
		num=int(request.form["cont"])
		try:
			#cursor=db.cursor()
			cursor=mysql.connection.cursor()
			sql="insert into request values('%s','%s','%d')"
			cursor.execute(sql%(type,loc,num))
			mysql.connection.commit()
			return render_template("request.html",msg="Requested successfully")
		except Exception as e:
			mysql.connection.rollback()
			return render_template("request.html",msg=e)
		
	else:
		return render_template("request.html")



@app.route("/add_bb",methods=["GET","POST"])
def add_bb():
	if request.method=="POST":
		ch=request.form["choice1"]
		id=int(request.form["id"])
		blood=request.form["blood_type"]
		loc=request.form["loc"]
		bb_name=request.form["bb_name"]
		cont=int(request.form["cont"])
		if ch=="bb":
			try:
				#cursor=db.cursor()
				cursor=mysql.connection.cursor()
				sql="insert into blood_bank values('%d','%s','%s','%s','%d')"
				cursor.execute(sql%(id,blood,loc,bb_name,cont))
				mysql.connection.commit()
				return render_template("add_bb.html",msg="added successfully")
			except Exception as e:
				mysql.connection.rollback()
				return render_template("add_bb.html",msg=e)
		else:
			try:
				#cursor=db.cursor()
				cursor=mysql.connection.cursor()
				sql="insert into blood_donor values('%d','%s','%s','%s','%d')"
				cursor.execute(sql%(id,blood,loc,bb_name,cont))
				mysql.connection.commit()
				return render_template("add_bb.html",msg="added successfully")
			except Exception as e:
				mysql.connection.rollback()
				return render_template("add_bb.html",msg=e)
			
	else:
		return render_template("add_bb.html")


@app.route("/edit_bb",methods=["GET","POST"])
def edit_bb():
	if request.method=="POST":
		ch=request.form["choice1"]
		id=int(request.form["id"])
		blood=request.form["blood_type"]
		loc=request.form["loc"]
		bb_name=request.form["bb_name"]
		cont=int(request.form["cont"])
		if ch=="bb":
			try:
				#cursor=db.cursor()
				cursor=mysql.connection.cursor()
				sql="update blood_bank set blood='%s',loc='%s',bb_name='%s',cont='%d' where id='%d'"
				cursor.execute(sql%(blood,loc,bb_name,cont,id))
				mysql.connection.commit()
				return render_template("edit_bb.html",msg="edited successfully")
			except Exception as e:
				mysql.connection.rollback()
				return render_template("edit_bb.html",msg=e)
		else:
			try:
				#cursor=db.cursor()
				cursor=mysql.connection.cursor()
				sql="update blood_donor set blood='%s',loc='%s',bb_name='%s',cont='%d' where id='%d'"
				cursor.execute(sql%(blood,loc,bb_name,cont,id))
				mysql.connection.commit()
				return render_template("edit_bb.html",msg="edited successfully")
			except Exception as e:
				mysql.connection.rollback()
				return render_template("edit_bb.html",msg=e)
			
	else:
		return render_template("edit_bb.html")

@app.route("/del_admin",methods=["GET","POST"])
def del_admin():
	if request.method=="POST":
		username=request.form["username"]
		try:
			#cursor=db.cursor()
			cursor=mysql.connection.cursor()
			sql="delete from admin where username='%s'"
			cursor.execute(sql%(username))
			mysql.connection.commit()
			return render_template("del_admin.html",msg="deleted successfully")

		except Exception as e:
			mysql.connection.rollback()
			return render_template("del_admin.html",msg="admin doesn't exists")
	else:
		return render_template("del_admin.html",msg="admin doesn't exists")

@app.route("/del_bb",methods=["GET","POST"])
def del_bb():
	if request.method=="POST":
		id=int(request.form["id"])
		ch=request.form["choice1"]
		if ch=="bb":
			try:
				#cursor=db.cursor()
				cursor=mysql.connection.cursor()
				sql="delete from blood_bank where id='%d'"
				cursor.execute(sql%(id))
				mysql.connection.commit()
				return render_template("del_bb.html",msg="deleted successfully")

			except Exception as e:
				mysql.connection.rollback()
				return render_template("del_bb.html",msg=e)
		else:
			try:
				#cursor=db.cursor()
				cursor=mysql.connection.cursor()
				sql="delete from blood_donor where id='%d'"
				cursor.execute(sql%(id))
				mysql.connection.commit()
				return render_template("del_bb.html",msg="deleted successfully")

			except Exception as e:
				mysql.connection.rollback()
				return render_template("del_bb.html",msg=e)
	else:
		return render_template("del_bb.html")


@app.route("/usr_home",methods=["GET","POST"])
def usr_home():
	if request.method=="POST":
		loc=request.form["loc"]
		ch=request.form["choice1"]
		if ch=="bb":
			try:
				#cursor=db.cursor()
				cursor=mysql.connection.cursor()
				sql="select blood,bb_name,cont from blood_bank where loc='%s'"
				cursor.execute(sql%(loc))
				data=cursor.fetchall()
				mysql.connection.commit()
				return render_template("usr_home.html",msg=data,name=session["username"])

			except Exception as e:
				mysql.connection.rollback()
				return render_template("usr_home.html",msg=e)
		else:
			try:
				#cursor=db.cursor()
				cursor=mysql.connection.cursor()
				sql="select blood,bb_name,cont from blood_donor where loc='%s'"
				cursor.execute(sql%(loc))
				data=cursor.fetchall()
				mysql.connection.commit()
				return render_template("usr_home.html",msg=data,name=session["username"])

			except Exception as e:
				mysql.connection.rollback()
				return render_template("usr_home.html",msg=e)
	else:
		return render_template("usr_home.html")


@app.route("/user",methods=["GET","POST"])
def user():
	return render_template ("login.html")	

@app.route("/login",methods=["GET","POST"])
def login():
	if request.method=="POST":
		un=request.form["un"]
		pw=request.form["pw"]
		try:
			#cursor=db.cursor()
			sql="select * from users where username='%s' and password='%s'"
			cursor=mysql.connection.cursor()
			cursor.execute(sql%(un,pw))
			data=cursor.fetchall()
			if len(data)==0:
				return render_template("login.html",msg="invalid login")
			else:
				session["username"]=un
				return redirect(url_for("usr_home"))
		except Exception as e:
			return render_template("login.html",msg=e)

	else:
		return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
	if request.method=="POST":
		un=request.form["un"]
		pw1=request.form["pw1"]
		pw2=request.form["pw2"]
		if pw1==pw2:
			try:
				#cursor=db.cursor()
				cursor=mysql.connection.cursor()
				sql="insert into users values('%s','%s')"
				cursor.execute(sql%(un,pw1))
				mysql.connection.commit()
				return redirect(url_for("login"))
			except Exception as e:
				mysql.connection.rollback()
				return render_template("signup.html",msg="user already exists")
		else:
			return render_template("signup.html",msg="password did not match")
	else:
		return render_template("signup.html")

@app.route("/admin_menu",methods=["GET","POST"])
def admin_menu():
	if request.method=="POST":
		un=request.form["un"]
		pw=request.form["pw"]
		try:
			#cursor=db.cursor()
			sql="select * from admin where username='%s' and password='%s'"
			cursor=mysql.connection.cursor()
			cursor.execute(sql%(un,pw))
			data=cursor.fetchall()
			if len(data)==0:
				return render_template("a_login.html",msg="invalid login")
			else:
				return render_template("admin_menu.html")
		except Exception as e:
			return render_template("a_login.html",msg=e)

	else:
		return render_template("a_login.html")

@app.route("/ad_admin",methods=["GET","POST"])
def ad_admin():
	return render_template("add_admin.html")

@app.route("/ad_bb",methods=["GET","POST"])
def ad_bb():
	return render_template("add_bb.html")

@app.route("/edi_bb",methods=["GET","POST"])
def edi_bb():
	return render_template("edit_bb.html")

@app.route("/de_admin",methods=["GET","POST"])
def de_admin():
	return render_template("del_admin.html")

@app.route("/de_bb",methods=["GET","POST"])
def de_bb():
	return render_template("del_bb.html")

@app.route("/show_home",methods=["GET","POST"])
def show_home():
	if request.method=="POST":
		loc=request.form["loc"]
		try:
			#cursor=db.cursor()
			cursor=mysql.connection.cursor()
			sql="select * from request where loc='%s'"
			cursor.execute(sql%(loc))
			data=cursor.fetchall()
			mysql.connection.commit()
			return render_template("show.html",msg=data)
		except Exception as e:
			mysql.connection.rollback()
			return render_template("show.html",msg=e)
	else:
			return render_template("show.html")

@app.route("/re_bb",methods=["GET","POST"])
def re_bb():
	return render_template("show.html")




if __name__=="__main__":
	app.run(debug=True,use_reloader=True)