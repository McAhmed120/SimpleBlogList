from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Define the Post model (database structure)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.content}')"


# Route to display all posts with pagination
@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=5)  # Correct usage with keyword arguments
    return render_template('index.html', posts=posts)


# Route to display form to add a new post
from flask import flash

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # Back-end validation: check if title or content is empty
        if not title or not content:
            flash("Both title and content are required.", "error")
            return redirect(url_for('add_post'))  # Redirect back to the add post form

        # Create a new Post instance
        new_post = Post(title=title, content=content)

        # Add to the database session and commit
        db.session.add(new_post)
        db.session.commit()

        # Flash success message
        flash("Post added successfully!", "success")
        return redirect(url_for('home'))  # Redirect back to the homepage

    return render_template('add_post.html')  # Show form to create a new post


# Route to edit a post
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # Back-end validation: check if title or content is empty
        if not title or not content:
            flash("Both title and content are required.", "error")
            return redirect(url_for('edit_post', id=post.id))  # Redirect back to the edit form

        post.title = title
        post.content = content

        db.session.commit()

        # Flash success message
        flash("Post updated successfully!", "success")
        return redirect(url_for('home'))  # Redirect back to the homepage

    return render_template('edit_post.html', post=post)






# Route to delete a post
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
