from flask import Flask,render_template,request,redirect,flash,session,url_for
import sqlite3
connection=sqlite3.connect('JobHolders.db')
cursor=connection.cursor()
try:
    cursor.execute('CREATE TABLE JobHolders(Name Varchar(20), ID int(1000), Salary int(100000), Age int(100), Address Varchar(20))')
    connection.commit()
    print("JobHolders Table Created Successfully")
except Exception as err:
    print(f"Error: {err}")
connection.close()

app=Flask(__name__)
app.secret_key='abcd1234'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/savedetails',methods=['GET','POST'])
def savedetails():
    msg=''
    if request.method=='POST':
        try:
            Name=request.form['Name']
            Id=request.form['Id']
            Salary=request.form['Salary']
            Age=request.form['Age']
            Address=request.form['Address']
            connection=sqlite3.connect('JobHolders.db')
            cursor=connection.cursor()
            cursor.execute('INSERT INTO JobHolders(Name,Id,Salary,Age,Address)Values(?,?,?,?,?)',(Name,Id,Salary,Age,Address))
            connection.commit()
            msg='Values Inserted Successfully'
        except Exception as err:
            msg='Unfortunately Values are not Inserted'
        finally:
            connection.close()
        return render_template('success.html',msg=msg)
@app.route('/view')
def view():
    connection=sqlite3.connect('JobHolders.db')
    connection.row_factory=sqlite3.Row
    cursor=connection.cursor()
    cursor.execute("SELECT * From JobHolders")
    result=cursor.fetchall()
    connection.close()
    return render_template('view.html',rows=result)

@app.route('/update',methods=['GET','POST'])
def update():
    msg=''
    if request.method=='POST':
        try:
            Name=request.form['Name']
            Id=request.form['Id']
            connection=sqlite3.connect('JobHolders.db')
            cursor=connection.cursor()
            cursor.execute('UPDATE JobHolders SET Name=? WHERE Id=?',(Name,Id))
            connection.commit()
            msg='Records Updated Successfully'
        except Exception as err:
            msg='Unfortunately Records are not updated'
        finally:
            connection.close()
        return render_template('update.html',msg=msg)
    return render_template('update.html')

@app.route('/delete')
def delete():
    return render_template('delete.html')

@app.route('/deleterecord',methods=['GET','POST'])
def deleterecord():
    id=request.form['Id']
    connection=sqlite3.connect('JobHolders.db')
    cursor=connection.cursor()
    try:
        cursor.execute('DELETE FROM JobHolders WHERE Id=?',(id,))
        connection.commit()
        msg="Selected Records are Deleted Successfully"
    except Exception as err:
        msg="Unfortunately Selected Record is not deleted"
    finally:
        connection.close()
    return render_template('delete_record.html',msg=msg)

if __name__=='__main__':
    app.run(debug=True)