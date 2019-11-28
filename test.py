from flask import Flask,render_template,request
from flask_mysqldb import MySQL
import yaml
import re
app = Flask(__name__)


#Configure DB
db=yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']

mysql=MySQL(app)
@app.route('/', methods=['GET','POST'])
def test_app():
    if request.method == 'POST':
      cur=mysql.connection.cursor()
      #FETCH DATA
      userDetails=request.form
      name=userDetails['name']
      favourite_colour=userDetails['Favourite Colour']
      cats_or_dogs=userDetails['cats or dogs']

      name=( re.sub(r"\s+", "", name))
      name=name.lower()
      resultvalue=cur.execute("SELECT * FROM test")
      if resultvalue > 0:
          fetcheddetail=cur.fetchall()
          i=0
          for row in fetcheddetail:
             a =(row[0])
             a=( re.sub(r"\s+", "", a))
             a=a.lower()
             if name==a:
                 i=i+1


          if i > 0:
              return "name already in database"

          else:
                 cur.execute("INSERT INTO test(name ,favourite_colour,cats_or_dogs) VALUES( %s,%s,%s)",(name,favourite_colour,cats_or_dogs))
                 mysql.connection.commit()
                 cur.close()
                 return "success"
    else:
        cur.execute("INSERT INTO test(name ,favourite_colour,cats_or_dogs) VALUES(  %s,%s,%s)",(name,favourite_colour,cats_or_dogs))
        mysql.connection.commit()
        cur.close()
        return "success"

    return render_template('index.html')

if __name__ == '__main__':
   app.run(host='0.0.0.0' ,port=80,debug=True)
