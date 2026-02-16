"""
Flask Blog Application
Main application file containing all routes and Flask configuration.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from functools import wraps
from service import BlogService, UserService
from models import BlogPost, User
from datetime import datetime
import os


# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production-2024'

# Initialize services (global instances)
blog_service = BlogService()
user_service = UserService()


# Authentication decorators
def login_required(f):
    """Decorator to require user login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin privileges."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        
        user = user_service.get_user_by_id(session['user_id'])
        if not user or not user.is_admin():
            flash('Admin privileges required to access this page.', 'error')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """Get the currently logged-in user."""
    if 'user_id' in session:
        return user_service.get_user_by_id(session['user_id'])
    return None


# Template context processor
@app.context_processor
def inject_user():
    """Inject current user into all templates."""
    return {
        'current_user': get_current_user(),
        'categories': blog_service.get_all_categories()
    }


# Error handlers
@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors."""
    return render_template('base.html', error_message="Page not found"), 404


@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 errors."""
    return render_template('base.html', error_message="Internal server error"), 500


# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'GET':
        # If user is already logged in, redirect to intended page or home
        if 'user_id' in session:
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        
        return render_template('login.html')
    
    elif request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('login.html')
        
        # Authenticate user
        user = user_service.authenticate(username, password)
        
        if user:
            # Create session
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect to intended page or appropriate dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            elif user.is_admin():
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password.', 'error')
            return render_template('login.html')


@app.route('/logout')
def logout():
    """Handle user logout."""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'GET':
        return render_template('register.html')
    
    elif request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # Validate input
        if not all([username, email, password, confirm_password]):
            flash('All fields are required.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        # Register user
        new_user = user_service.register_user(username, email, password)
        
        if new_user:
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username or email already exists.', 'error')
            return render_template('register.html')


# Dashboard Routes
@app.route('/dashboard')
@login_required
def user_dashboard():
    """User dashboard to manage their posts."""
    current_user = get_current_user()
    user_posts = blog_service.get_posts_by_user_id(current_user.id, include_unapproved=True)
    pending_count = len([post for post in user_posts if not post.is_approved])
    approved_count = len([post for post in user_posts if post.is_approved])
    
    return render_template(
        'user_dashboard.html',
        posts=user_posts,
        pending_count=pending_count,
        approved_count=approved_count,
        total_posts=len(user_posts)
    )


# User Routes
@app.route('/')
def index():
    """
    Display all blog posts on the homepage.
    Supports optional search and category filtering via query parameters.
    """
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()
    
    if search_query:
        posts = blog_service.search_posts_by_title(search_query)
        page_title = f"Search Results for '{search_query}'"
    elif category_filter:
        posts = blog_service.filter_posts_by_category(category_filter)
        page_title = f"Posts in '{category_filter}' Category"
    else:
        posts = blog_service.get_all_posts()
        page_title = "Latest Blog Posts"
    
    categories = blog_service.get_all_categories()
    
    return render_template(
        'index.html',
        posts=posts,
        categories=categories,
        page_title=page_title,
        search_query=search_query,
        current_category=category_filter
    )


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    """
    Display a single blog post by ID.
    
    Args:
        post_id (int): The ID of the post to display
    """
    post = blog_service.get_post_by_id(post_id)
    
    if not post:
        flash(f'Blog post with ID {post_id} not found.', 'error')
        return redirect(url_for('index'))
    
    return render_template('post_detail.html', post=post)


@app.route('/search')
def search():
    """
    Search for blog posts by title.
    Redirects to index with search query parameter.
    """
    search_query = request.args.get('q', '').strip()
    
    if search_query:
        return redirect(url_for('index', search=search_query))
    else:
        flash('Please enter a search term.', 'warning')
        return redirect(url_for('index'))


@app.route('/category/<category>')
def filter_by_category(category):
    """
    Filter blog posts by category.
    Redirects to index with category parameter.
    
    Args:
        category (str): The category to filter by
    """
    return redirect(url_for('index', category=category))


# Admin Routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    """
    Display the admin dashboard with all blog posts and management options.
    """
    posts = blog_service.get_all_posts(include_unapproved=True)
    pending_posts = blog_service.get_pending_posts()
    total_posts = blog_service.get_posts_count()
    categories = blog_service.get_all_categories()
    
    # Convert posts to dictionaries for JSON serialization in template
    posts_dict = [post.to_dict() for post in posts]
    
    return render_template(
        'admin.html',
        posts=posts,
        posts_dict=posts_dict,
        pending_posts=pending_posts,
        pending_count=len(pending_posts),
        total_posts=total_posts,
        categories=categories
    )


@app.route('/admin/create', methods=['GET', 'POST'])
@admin_required
def admin_create_post():
    """
    Handle both GET and POST requests for creating new blog posts.
    GET: Display the create post form
    POST: Process form submission and create new post
    """
    if request.method == 'GET':
        return render_template('edit_post.html', 
                             post=None, 
                             form_title="Create New Blog Post",
                             form_action=url_for('admin_create_post'))
    
    elif request.method == 'POST':
        # Extract form data
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author_name = request.form.get('author_name', '').strip()
        category = request.form.get('category', '').strip()
        
        # Validate form data
        if not all([title, content, author_name, category]):
            flash('All fields are required.', 'error')
            return render_template('edit_post.html', 
                                 post=None, 
                                 form_title="Create New Blog Post",
                                 form_action=url_for('admin_create_post'),
                                 form_data=request.form)
        
        try:
            # Create new post (admin posts are auto-approved)
            current_user = get_current_user()
            new_post = blog_service.create_post(
                title, content, author_name, category, 
                user_id=current_user.id, is_approved=True
            )
            flash(f'Blog post "{title}" created successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
            
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('edit_post.html', 
                                 post=None, 
                                 form_title="Create New Blog Post",
                                 form_action=url_for('admin_create_post'),
                                 form_data=request.form)


@app.route('/admin/edit/<int:post_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_post(post_id):
    """
    Handle both GET and POST requests for editing existing blog posts.
    GET: Display the edit post form with current post data
    POST: Process form submission and update post
    
    Args:
        post_id (int): The ID of the post to edit
    """
    post = blog_service.get_post_by_id(post_id)
    
    if not post:
        flash(f'Blog post with ID {post_id} not found.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'GET':
        return render_template('edit_post.html', 
                             post=post, 
                             form_title="Edit Blog Post",
                             form_action=url_for('admin_edit_post', post_id=post_id))
    
    elif request.method == 'POST':
        # Extract form data
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author_name = request.form.get('author_name', '').strip()
        category = request.form.get('category', '').strip()
        
        # Validate form data
        if not all([title, content, author_name, category]):
            flash('All fields are required.', 'error')
            return render_template('edit_post.html', 
                                 post=post, 
                                 form_title="Edit Blog Post",
                                 form_action=url_for('admin_edit_post', post_id=post_id))
        
        # Update post
        updated_post = blog_service.edit_post(post_id, title, content, author_name, category)
        
        if updated_post:
            flash(f'Blog post "{title}" updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Failed to update blog post.', 'error')
            return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete/<int:post_id>')
@admin_required
def admin_delete_post(post_id):
    """
    Delete a blog post by ID.
    
    Args:
        post_id (int): The ID of the post to delete
    """
    post = blog_service.get_post_by_id(post_id)
    
    if not post:
        flash(f'Blog post with ID {post_id} not found.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    # Store post title for confirmation message
    post_title = post.title
    
    # Delete the post
    if blog_service.delete_post(post_id):
        flash(f'Blog post "{post_title}" deleted successfully!', 'success')
    else:
        flash('Failed to delete blog post.', 'error')
    
    return redirect(url_for('admin_dashboard'))


@app.route('/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    """
    Delete a blog post by ID (user can only delete own posts).
    
    Args:
        post_id (int): The ID of the post to delete
    """
    current_user = get_current_user()
    post = blog_service.get_post_by_id(post_id)
    
    if not post:
        flash('Post not found.', 'error')
        return redirect(url_for('user_dashboard'))
    
    # Check if user owns the post or is admin
    if post.user_id != current_user.id and not current_user.is_admin():
        flash('You can only delete your own posts.', 'error')
        return redirect(url_for('user_dashboard'))
    
    # Store post title for confirmation message
    post_title = post.title
    
    # Delete the post
    if blog_service.delete_post(post_id):
        flash(f'Post "{post_title}" deleted successfully!', 'success')
    else:
        flash('Failed to delete post.', 'error')
    
    return redirect(url_for('user_dashboard'))


# Post Approval Routes
@app.route('/admin/approve/<int:post_id>')
@admin_required
def approve_post(post_id):
    """Approve a pending blog post."""
    if blog_service.approve_post(post_id):
        flash('Post approved successfully!', 'success')
    else:
        flash('Post not found.', 'error')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/reject/<int:post_id>')
@admin_required
def reject_post(post_id):
    """Reject/unapprove a blog post."""
    if blog_service.reject_post(post_id):
        flash('Post rejected.', 'info')
    else:
        flash('Post not found.', 'error')
    return redirect(url_for('admin_dashboard'))


# User Post Creation Routes
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Handle user post creation (requires approval for non-admin users)."""
    current_user = get_current_user()
    
    if request.method == 'GET':
        return render_template('edit_post.html', 
                             post=None, 
                             form_title="Create New Post",
                             form_action=url_for('create_post'))
    
    elif request.method == 'POST':
        # Extract form data
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', '').strip()
        
        # Use current user's name as author
        author_name = current_user.username
        
        # Validate form data
        if not all([title, content, category]):
            flash('Title, content, and category are required.', 'error')
            return render_template('edit_post.html', 
                                 post=None, 
                                 form_title="Create New Post",
                                 form_action=url_for('create_post'),
                                 form_data=request.form)
        
        try:
            # Create new post (requires approval for regular users)
            is_approved = current_user.is_admin()
            new_post = blog_service.create_post(
                title, content, author_name, category, 
                user_id=current_user.id, is_approved=is_approved
            )
            
            if is_approved:
                flash(f'Blog post "{title}" created and published!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash(f'Blog post "{title}" created and sent for approval!', 'success')
                return redirect(url_for('user_dashboard'))
            
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('edit_post.html', 
                                 post=None, 
                                 form_title="Create New Post",
                                 form_action=url_for('create_post'),
                                 form_data=request.form)


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Handle user post editing (only own posts)."""
    current_user = get_current_user()
    post = blog_service.get_post_by_id(post_id)
    
    if not post:
        flash('Post not found.', 'error')
        return redirect(url_for('user_dashboard'))
    
    # Check if user owns the post or is admin
    if post.user_id != current_user.id and not current_user.is_admin():
        flash('You can only edit your own posts.', 'error')
        return redirect(url_for('user_dashboard'))
    
    if request.method == 'GET':
        return render_template('edit_post.html', 
                             post=post, 
                             form_title="Edit Post",
                             form_action=url_for('edit_post', post_id=post_id))
    
    elif request.method == 'POST':
        # Extract form data
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', '').strip()
        
        # Validate form data
        if not all([title, content, category]):
            flash('All fields are required.', 'error')
            return render_template('edit_post.html', 
                                 post=post, 
                                 form_title="Edit Post",
                                 form_action=url_for('edit_post', post_id=post_id))
        
        # Update post (if user edited, needs re-approval unless admin)
        updated_post = blog_service.edit_post(post_id, title, content, post.author_name, category)
        
        # If regular user edited their post, it needs re-approval
        if updated_post and not current_user.is_admin():
            blog_service.reject_post(post_id)  # Set to pending approval
            flash('Post updated and sent for re-approval!', 'success')
        elif updated_post:
            flash('Post updated successfully!', 'success')
        else:
            flash('Failed to update post.', 'error')
        
        return redirect(url_for('user_dashboard'))


# API Routes (optional, for future AJAX functionality)
@app.route('/api/posts')
def api_get_posts():
    """
    API endpoint to get all posts as JSON.
    """
    posts = blog_service.get_all_posts()
    return jsonify([post.to_dict() for post in posts])


@app.route('/api/posts/<int:post_id>')
def api_get_post(post_id):
    """
    API endpoint to get a specific post as JSON.
    
    Args:
        post_id (int): The ID of the post to retrieve
    """
    post = blog_service.get_post_by_id(post_id)
    if post:
        return jsonify(post.to_dict())
    else:
        return jsonify({'error': 'Post not found'}), 404


@app.route('/api/categories')
def api_get_categories():
    """
    API endpoint to get all categories as JSON.
    """
    categories = blog_service.get_all_categories()
    return jsonify(categories)


# Template filters
@app.template_filter('truncate_content')
def truncate_content(content, length=200):
    """
    Template filter to truncate content for preview.
    
    Args:
        content (str): The content to truncate
        length (int): Maximum length of truncated content
    
    Returns:
        str: Truncated content with ellipsis if needed
    """
    if len(content) <= length:
        return content
    return content[:length] + '...'


@app.template_filter('format_date')
def format_date(date_obj, format_str='%B %d, %Y at %I:%M %p'):
    """
    Template filter to format datetime objects.
    
    Args:
        date_obj (datetime): The datetime object to format
        format_str (str): The format string
    
    Returns:
        str: Formatted date string
    """
    if isinstance(date_obj, datetime):
        return date_obj.strftime(format_str)
    return str(date_obj)


if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True, host='0.0.0.0', port=5000)