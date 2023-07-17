# import libraries
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


#Initializing flask app
app=Flask(__name__)

#secret key declaration
app.secret_key='Secret Key'


# Set the database URI to the absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentdbms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONs'] = False

#Initialise database
db=SQLAlchemy(app)

#Creating a class to store students db
class Data(db.Model):
    #Number of columns--4
    roll=db.Column(db.Integer, primary_key=True)
    date=db.Column(db.Date)
    name=db.Column(db.String(100))
    subject=db.Column(db.String(100))

    def __init__(self, date, name, subject):
        #variables initialising
        import datetime

        # changing date string to date format
        date_string = date
        self.date = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
        self.name = name
        self.subject = subject
with app.app_context():
    db.create_all()


#Routing to the home page of the app
@app.route('/')
def Index():
    #It returns all the data in the db
    all_data = Data.query.all()
    return render_template('home.html',students=all_data)    


@app.route('/insert',methods=['POST'])
def insert():

    if request.method == 'POST':
        date=request.form['date']
        name=request.form['name']
        subject=request.form['subject']

        my_data=Data(date=date,name=name,subject=subject)
        #Adding to db
        db.session.add(my_data)
        db.session.commit()
        return redirect(url_for('Index'))


@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        my_data=Data.query.get(request.form.get('roll'))
        my_data.date=request.form['date']
        my_data.name=request.form['name']
        my_data.subject=request.form['subject']
        db.session.commit()

        return redirect(url_for('Index'))

@app.route('/delete/<roll>',methods=['GET','POST'])
def delete(roll):
    my_data=Data.query.get(roll)
    db.session.delete(my_data)
    db.session.commit()
    

           








if __name__ == '__main__':
    app.run(debug=True)


