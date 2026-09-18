from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_super_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, faça login para acessar esta página."
login_manager.login_message_category = "warning"
with app.app_context():
    db.create_all()

# ================= MODELOS DE DADOS ================= #

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    bio = db.Column(db.String(250), default="Amante de livros.")
    books = db.relationship('Book', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="Tenho")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviews = db.relationship('Review', backref='book', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    comments = db.relationship('Comment', backref='review', lazy=True)
    likes = db.relationship('Like', backref='review', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ================= ROTAS ================= #

@app.route('/')
@login_required
def feed():
    reviews = Review.query.order_by(Review.timestamp.desc()).all()
    return render_template('feed.html', reviews=reviews)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if 'update_profile' in request.form:
            current_user.bio = request.form.get('bio')
            db.session.commit()
            flash('Perfil atualizado!', 'success')
        
        elif 'add_book' in request.form:
            new_book = Book(
                title=request.form.get('title'),
                author=request.form.get('author'),
                status=request.form.get('status'),
                owner=current_user
            )
            db.session.add(new_book)
            db.session.commit()
            flash('Livro adicionado à sua biblioteca!', 'success')
            
    return render_template('profile.html', user=current_user)

@app.route('/user/<username>')
@login_required
def user_profile(username):
    if username == current_user.username:
        return redirect(url_for('profile'))
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_profile.html', user=user)

@app.route('/review/<int:book_id>', methods=['POST'])
@login_required
def add_review(book_id):
    content = request.form.get('content')
    new_review = Review(content=content, user_id=current_user.id, book_id=book_id)
    db.session.add(new_review)
    db.session.commit()
    flash('Resenha publicada!', 'success')
    return redirect(url_for('profile'))

@app.route('/review/delete/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        flash('Você não tem permissão para excluir esta resenha.', 'danger')
        return redirect(url_for('feed'))

    Comment.query.filter_by(review_id=review.id).delete()
    Like.query.filter_by(review_id=review.id).delete()
    db.session.delete(review)
    db.session.commit()
    flash('Resenha excluída com sucesso!', 'success')
    return redirect(request.referrer or url_for('feed'))

@app.route('/like/<int:review_id>')
@login_required
def like_review(review_id):
    like = Like.query.filter_by(user_id=current_user.id, review_id=review_id).first()
    if like:
        db.session.delete(like)
    else:
        db.session.add(Like(user_id=current_user.id, review_id=review_id))
    db.session.commit()
    return redirect(url_for('feed'))

@app.route('/comment/<int:review_id>', methods=['POST'])
@login_required
def add_comment(review_id):
    content = request.form.get('content')
    if content:
        new_comment = Comment(content=content, user_id=current_user.id, review_id=review_id)
        db.session.add(new_comment)
        db.session.commit()
    return redirect(url_for('feed'))

# ================= AUTENTICAÇÃO ================= #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('feed'))
        flash('Usuário ou senha incorretos.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já cadastrado.', 'danger')
            return redirect(url_for('register'))
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('feed'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
