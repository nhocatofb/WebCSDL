from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pas'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'wesharemeals'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        details = request.form
        loginname = details['loginname']
        passw = details['passw']
        cur = mysql.connection.cursor()
        cur.execute("select* from accounts where loginname = %s", [loginname])
        tmp = cur.fetchone()
        cur.close()
        print(tmp[1])
        if tmp[1] == passw:
            return render_template("menu.html")
    return render_template("home.html")


@app.route('/ressearch/', methods=['GET', 'POST'])
def ressearch():
    if request.method == "POST":
        details = request.form
        id = details['id']
        loginname = details['loginname']
        city = details['city']
        district = details['district']
        cur = mysql.connection.cursor()
        truyvan = "select* from restaurants where "
        tmp = 0
        if id:
            truyvan += "loginname = '" + id + "'"
            tmp = 1
        if loginname:
            if tmp == 1:
                truyvan += "and "
            truyvan += "resname = '" + loginname + "'"
            tmp = 1
        if city:
            if tmp == 1:
                truyvan += "and "
            truyvan += "city = '" + city + "'"
            tmp = 1
        if district:
            if tmp == 1:
                truyvan += "and "
            truyvan += "district = '" + district + "'"
        print(truyvan)
        cur.execute(truyvan)
        results = cur.fetchall()
        cur.close()
        return render_template("ressearch.html", results=results)
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM restaurants"
    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    return render_template('ressearch.html', results=results)


@app.route('/dishsearch/', methods=['GET', 'POST'])
def dishsearch():
    if request.method == "POST":
        details = request.form
        id = details['id']
        loginname = details['loginname']
        city = details['city']
        district = details['district']
        cur = mysql.connection.cursor()
        truyvan = "select* from menu where "
        tmp = 0
        if id:
            truyvan += "resname = '" + id + "'"
            tmp = 1
        if loginname:
            if tmp == 1:
                truyvan += "and "
            truyvan += "dishname = '" + loginname + "'"
            tmp = 1
        if city:
            if tmp == 1:
                truyvan += "and "
            truyvan += "evaluationpoint = '" + city + "'"
            tmp = 1
        if district:
            if tmp == 1:
                truyvan += "and "
            truyvan += "price = '" + district + "'"
            tmp = 1
        print(truyvan)
        if tmp == 0:
            cur.execute("select*from menu")
        cur.execute(truyvan)
        results = cur.fetchall()
        cur.close()
        return render_template("dishsearch.html", results=results)
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM menu"
    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    return render_template('dishsearch.html', results=results)


@app.route('/menu/')
def menu():
    return render_template("menu.html")


@app.route('/comming')
def comming():
    return render_template("comming.html")


@app.route('/about/', methods=['GET', 'POST'])
def about():
    if request.method == "POST":
        details = request.form
        loginname = details['loginname']
        passw = details['passw']
        pnumber = details['pnumber']
        acctype = details['acctype']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO accounts VALUES (%s, %s, %s, %s)", (loginname, passw, pnumber, acctype))
        mysql.connection.commit()
        cur.close()
        return home()
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
