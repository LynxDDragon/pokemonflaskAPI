from . import bp as app
from flask import render_template, request, redirect, url_for, flash
from app.blueprints.main.models import User, Post, Pokemon, Collection
from app import db
from flask_login import current_user, login_required

# Routes that return/display HTML

@app.route('/')
@login_required
def home():
    posts = Post.query.all()
    return render_template('home.html', user=current_user, posts=posts)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.all()
    pokes = Pokemon.query.all()
    return render_template('user.html', user=user, posts=posts, pokes=pokes)

@app.route('/pokemon')
@login_required
def pokemon():
    pokes = Pokemon.query.all()
    return render_template('pokemon.html', user=current_user, pokes=pokes)

@app.route('/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

@app.route('/post', methods=['POST'])
@login_required
def create_post():
    post_title = request.form['title']
    post_body = request.form['body']
    
    new_post = Post(title=post_title, body=post_body, user_id=current_user.id)

    db.session.add(new_post)
    db.session.commit()

    flash('Post added successfully', 'success')
    return redirect(url_for('main.home'))

@app.route('/post/<id>')
def post(id):
    single_post = Post.query.get(id)
    return render_template('single-post.html', post=single_post)

#pokemon listings

@app.route('/pokecreate', methods=['POST'])
@login_required
def create_pokemon():
    poke_name = request.form['name']
    poke_description = request.form['description']
    poke_typing = request.form['type']
    
    new_poke = Pokemon(name=poke_name, description=poke_description, typing=poke_typing, user_id=current_user.id)

    db.session.add(new_poke)
    db.session.commit()

    flash('Pokemon has been added!!!', 'success')
    return redirect(url_for('main.pokemon'))

@app.route('/pokeentry/<id>')
def pokeentry(id):
    pokemon_entry = Pokemon.query.get(id)
    return render_template('poke_entry.html', user=current_user, pokeentry=pokemon_entry)


@app.route('/pokecatch')
def catchpoke():
    poke_name = request.form['name']
    poke_description = request.form['description']
    poke_typing = request.form['type']
    
    catch = Collection(name=poke_name, description=poke_description, typing=poke_typing, user_id=current_user.id)

    db.session.add(catch)
    db.session.commit()

    flash('You Caught a New Pokemon!!!', 'success')
    return redirect(url_for('main.pokemon'))
