from flask import Flask,render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm,NewChild,AddReport
from kindergartenDB_ORM import User,Child_accounting,Parents,Report_visits,Subdivision,Month,Kindergarten
from sqlalchemy import func

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)


@app.route('/',methods=['POST','GET'])
def start_page():
    form = LoginForm(request.form)
    conn = db.engine.connect()
    if request.method == 'POST' and form.validate():
        login_form = form.login.data
        password_form = form.password.data
        if db.session.query(User).filter_by(login = login_form).scalar() != None:
            if db.session.query(User).filter_by(password = password_form) != None:
                session['curent_admin'] = login_form
                conn.close()
                return redirect(url_for('main_page'))
    return render_template('startPage.html')

@app.route('/MainPage')
def main_page():
    main_query = db.session.query(Child_accounting,Kindergarten,Parents,Subdivision,func.sum(Report_visits.payment_sum))\
    .join(Kindergarten).filter(Child_accounting.kindergarten_id == Kindergarten.id)\
    .join(Parents).filter(Child_accounting.parent_id == Parents.id)\
    .join(Subdivision).filter(Parents.subdivision_id == Subdivision.id)\
    .outerjoin(Report_visits, Child_accounting.id == Report_visits.child_accounting_id)\
    .group_by(Child_accounting,Kindergarten,Parents,Subdivision)


    show_report_visits = db.session.query(Report_visits)

    return render_template('MainPage.html',children_html = main_query, report_visits_html= show_report_visits)

@app.route('/AddChildren',methods=['GET', 'POST'])
def add_children():
    form = NewChild(request.form)
    conn = db.engine.connect()
    subdivisions = db.session.query(Subdivision)
    kindergartens = db.session.query(Kindergarten)

    if request.method == 'POST' and form.validate():

        parent_surname = request.form['parent_surname']
        parent_name = request.form['parent_name']
        parent_patronymic = request.form['parent_patronymic']
        subdivision_id = request.form['subdivision_id']
        if db.session.query(Parents).filter_by(surname=parent_surname,name=parent_name,patronymic=parent_patronymic).scalar() == None:
            parent_db = Parents(parent_surname,parent_name,parent_patronymic,subdivision_id)
            db.session.add(parent_db)
            db.session.commit()
            db.session.close()

        kindergarten_id = request.form['kindergarten_id']
        child_parent_id = db.session.query(Parents).filter_by(surname=parent_surname,name=parent_name,patronymic=parent_patronymic).first().id
        child_surname = request.form['child_surname']
        child_name = request.form['child_name']
        child_patronymic = request.form['child_patronymic']
        # payment_sum = request.form['payment_sum']
        if db.session.query(Child_accounting).filter_by(surname=child_surname, name=child_name,patronymic=child_patronymic).scalar() == None:
            child_db = Child_accounting(kindergarten_id,child_parent_id,child_surname,child_name,child_patronymic,None)
            db.session.add(child_db)
            db.session.commit()
            db.session.close()
        conn.close()
        return redirect(url_for('main_page'))
    return render_template('AddNewFamily.html',subdivisions_html=subdivisions,kindergartens_html=kindergartens)

@app.route('/showSubdivision',methods=['GET', 'POST'])
def show_Subdivision():
    subdivision_count = db.session.query(Subdivision,func.count(Parents.id))\
        .outerjoin(Parents,Subdivision.id == Parents.subdivision_id)\
        .group_by(Subdivision)\
        .order_by(Subdivision.name.asc())

    subdivision_query = db.session.query(Child_accounting,Kindergarten,Parents,Subdivision)\
    .join(Kindergarten).filter(Child_accounting.kindergarten_id == Kindergarten.id)\
    .join(Parents).filter(Child_accounting.parent_id == Parents.id)\
    .join(Subdivision).filter(Parents.subdivision_id == Subdivision.id)

    return render_template('showSubdivision.html',subdivision_html=subdivision_query,subdivision_count=subdivision_count)

@app.route('/report_visits/<string:ids>',methods=['GET', 'POST'])
def report_visits(ids):
    conn = db.engine.connect()

    result_visits  = db.session.query(Month,Report_visits,Child_accounting,Kindergarten)\
        .join(Report_visits).filter(Report_visits.month_id == Month.id)\
        .join(Child_accounting).filter(Child_accounting.id == Report_visits.child_accounting_id)\
        .join(Kindergarten).filter(Kindergarten.id == Child_accounting.kindergarten_id)\
        .filter(Report_visits.child_accounting_id == ids)

    child_info = db.session.query(Child_accounting)\
        .filter(Child_accounting.id == ids).first()

    return render_template('reportVisit.html',visits_html = result_visits,child_info=child_info)

@app.route('/add_report/<string:ids>',methods=['GET', 'POST'])
def add_report(ids):
    form = AddReport(request.form)
    conn = db.engine.connect()

    result_month = db.session.query(Month)
    result_kindergarten = db.session.query(Kindergarten,Child_accounting)\
        .join(Child_accounting)\
        .filter(Kindergarten.id == Child_accounting.kindergarten_id)\
        .filter(Child_accounting.id == ids).first()


    if request.method == 'POST' and form.validate():
        month_id = request.form['month_id']
        number_of_work_days = db.session.query(Month).filter(Month.id == month_id).first().number_of_work_days
        number_of_visiting_days = request.form['parent_surname']
        child_acc_id = ids
        payment_sum = int(int(result_kindergarten[0].price)/number_of_work_days*int(number_of_visiting_days))

        report_db = Report_visits(month_id,number_of_visiting_days,ids,payment_sum)
        if db.session.query(Report_visits).filter_by(month_id=month_id,child_accounting_id=ids).scalar() == None:
            db.session.add(report_db)
            db.session.commit()
            db.session.close()
        return redirect(url_for('report_visits',ids=ids))


    return render_template('addMonthReport.html',result_month=result_month, result_kindergarten=result_kindergarten,form=form)

@app.route('/showKindergarten',methods=['GET', 'POST'])
def show_Kindergarten():
    kindergarten_count = db.session.query(Kindergarten,func.count(Child_accounting.id))\
        .outerjoin(Child_accounting,Kindergarten.id == Child_accounting.kindergarten_id)\
        .group_by(Kindergarten)\
        .order_by(Kindergarten.name.asc())

    kindergarten_query = db.session.query(Child_accounting,Kindergarten,Parents,Subdivision)\
    .join(Kindergarten).filter(Child_accounting.kindergarten_id == Kindergarten.id)\
    .join(Parents).filter(Child_accounting.parent_id == Parents.id)\
    .join(Subdivision).filter(Parents.subdivision_id == Subdivision.id)

    return render_template('showKindergarten.html',kindergarten_html=kindergarten_query,kindergarten_count=kindergarten_count)





if __name__ == '__main__':
    app.secret_key = 'secret222'
    app.run(debug=True)

