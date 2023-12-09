from flask import *
from flask_sqlalchemy import *
from sqlalchemy.orm import *
from flask_login import *
from hashlib import *

app = Flask(__name__)
app.secret_key = 'secret_key_for_my_website 123'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"

try:
    class Base(DeclarativeBase):
        pass
except:
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    current_balance = db.Column(db.Integer)
    trash = db.Column(db.String)
    status = db.Column(db.String)

    def __repr__(self):
        return '<User %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class items(db.Model):
    itemid = db.Column(db.Integer, primary_key=True)
    iname = db.Column(db.String, nullable=False)
    iprice = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String, nullable=False)
    video = db.Column(db.String, nullable=False)
    blenderfile = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<items %r>' % self.itemid


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    item = items.query.all()
    return render_template("index.html", item=item)


@app.route('/<int:itemid>', methods=['GET', 'POST'])
def buy(itemid):
    item = items.query.get(itemid)
    nt = 0
    try:
        user_balance = current_user.current_balance
        nt = 1
    except:
        user_balance = 0
    if request.method == "POST":
        try:
            if current_user.current_balance >= item.iprice:
                User.query.get(current_user.id).current_balance -= item.iprice
                db.session.commit()
        except:
            pass
    return render_template("buy.html", item=item, bal=user_balance, nt=nt)


@app.route('/for admin')
@login_required
def for_admin():
    if current_user.status == 'admin':
        return render_template("for_admin.html")
    else:
        return redirect('/')


@app.route('/add', methods=['POST', 'GET'])
def additem():
    if request.method == "POST":
        iname = request.form['iname']
        iprice = request.form['iprice']
        image = request.form['image']
        video = request.form['video']
        blenderfile = request.form['blenderfile']
        item = items(iname=iname, iprice=iprice, image=image, video=video, blenderfile=blenderfile)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Nothing happend"

    else:
        return render_template("additem.html")


@app.route('/delete', methods=['POST', 'GET'])
def delete_item():
    if request.method == "POST":
        itemid = request.form['itemid']
        item = items.query.get(itemid)
        try:
            db.session.delete(item)
            db.session.commit()
        except:
            "Nothing happend"
    return render_template("deleteitem.html")


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    is_right = 1
    login = request.form.get('login')
    password = request.form.get('password')
    password = sha256(str(password).encode()).hexdigest()
    if login and password:
        user = User.query.filter_by(login=login, password=password).first()
        if user and user.password == password:
            login_user(user)
            return redirect('/')
        else:
            is_right = 0
            return render_template('login.html', is_right=is_right)
    else:
        return render_template('login.html', is_right=is_right)


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    all_filled = 1
    ps = 1
    used_name = 0
    if request.method == 'POST':
        if not login or not password or not password2:
            all_filled = 0
            return render_template('register.html', all_filled=all_filled, ps=ps, used_name=used_name)
        elif password != password2:
            ps = 0
            return render_template('register.html', all_filled=all_filled, ps=ps, used_name=used_name)
        else:
            try:
                pw = sha256(password.encode()).hexdigest()
                status = 'user'
                balance = 0
                if login == 'admin':
                    status = 'admin'
                    balance = 100000000000000
                new_user = User(login=login, password=pw, current_balance=balance, status=status)
                db.session.add(new_user)
                db.session.commit()
                return redirect('/login')
            except:
                used_name = 1
                return render_template('register.html', all_filled=all_filled, ps=ps, used_name=used_name)
    return render_template('register.html', all_filled=all_filled, ps=ps, used_name=used_name)


@app.route('/to_trash/<int:a>/<int:b>/<int:c>', methods=['GET', 'POST'])
@login_required
def to_trash(a, b, c):
    total_price = 0
    try:
        el = str(User.query.get(a).trash)
        if str(b) in el:
            pass
        else:
            User.query.get(a).trash = el + " " + str(b)
            db.session.commit()
    except:
        pass
    trash = []
    busket = User.query.get(a).trash.split()
    nums = "123456789"
    for i in busket:
        if i in nums:
            trash.append(i)
            total_price += int(items.query.get(i).iprice)
    if request.method == "POST":
        if c != 0:
            in_trash = User.query.get(int(a)).trash.split()
            in_trash.remove(str(c))
            User.query.get(int(a)).trash = ' '.join(in_trash)
            db.session.commit()
            total_price -= int(items.query.get(int(c)).iprice)
            trash.remove(str(c))
        else:
            if int(User.query.get(int(a)).current_balance) >= total_price:
                User.query.get(int(a)).current_balance = int(User.query.get(int(a)).current_balance) - total_price
                db.session.commit()
    items_in_busket = []
    bl_in_busket = []
    for i in trash:
        items_in_busket.append(items.query.get(int(i)))
        bl_in_busket.append('/static/blenderfile/' + str(items.query.get(int(i)).blenderfile))
    currentBalance = int(User.query.get(int(a)).current_balance)
    bl_in_busket = ' '.join(bl_in_busket)
    if b == 0:
        return render_template('trash.html', trash=trash, item=items_in_busket, total=total_price, files=bl_in_busket, balance=currentBalance)
    else:
        if c == 0:
            return redirect('/')
        else:
            return render_template('trash.html', trash=trash, item=items_in_busket, total=total_price, files=bl_in_busket, balance=currentBalance)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    return render_template('user_profile.html')






if __name__ == "__main__":
    app.run(debug=True)
