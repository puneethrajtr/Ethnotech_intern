"""
Blog Service Module
Contains the BlogService class that handles all blog post operations and business logic.
"""

from typing import List, Optional
from models import BlogPost, User


class UserService:
    """
    UserService class to handle user authentication and management.
    """
    
    def __init__(self):
        """Initialize the UserService with default admin account."""
        self._users: List[User] = []
        self._create_default_users()
    
    def _create_default_users(self):
        """Create default admin and demo users."""
        # Default admin user
        admin = User(
            username='admin',
            email='admin@blog.com',
            password='admin123',
            role='admin'
        )
        self._users.append(admin)
        
        # Demo regular user
        user = User(
            username='user',
            email='user@blog.com',
            password='user123',
            role='user'
        )
        self._users.append(user)
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password."""
        user = self.get_user_by_username(username)
        if user and user.check_password(password) and user.is_active:
            return user
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        username = username.lower().strip()
        for user in self._users:
            if user.username == username:
                return user
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        for user in self._users:
            if user.id == user_id:
                return user
        return None
    
    def register_user(self, username: str, email: str, password: str, role: str = 'user') -> Optional[User]:
        """Register a new user."""
        # Check if username already exists
        if self.get_user_by_username(username):
            return None
        
        # Check if email already exists
        email = email.lower().strip()
        for user in self._users:
            if user.email == email:
                return None
        
        # Create new user
        new_user = User(username, email, password, role)
        self._users.append(new_user)
        return new_user
    
    def get_all_users(self) -> List[User]:
        """Get all users."""
        return self._users


class BlogService:
    """
    BlogService class to handle all blog post operations.
    
    This class manages the in-memory storage of blog posts and provides
    methods for CRUD operations, searching, and filtering.
    """
    
    def __init__(self):
        """Initialize the BlogService with an empty list of posts."""
        self._posts: List[BlogPost] = []
        # Add some sample data for demonstration
        self._create_sample_data()
    
    def _create_sample_data(self):
        """Create some sample blog posts for demonstration purposes."""
        sample_posts = [
            {
                'title': 'Welcome to Our Blog',
                'content': '''Welcome to our amazing blog platform! This is our first post where we introduce you to the world of blogging. 
                
Here you'll find articles about technology, programming, and web development. Our goal is to share knowledge and help fellow developers improve their skills.

Stay tuned for more exciting content coming your way!''',
                'author_name': 'Admin',
                'category': 'General',
                'user_id': 1,  # Admin user
                'is_approved': True
            },
            {
                'title': 'Getting Started with Python Flask',
                'content': '''Flask is a lightweight and powerful web framework for Python. It's perfect for building web applications quickly and efficiently.

In this post, we'll cover:
- Setting up a Flask environment
- Creating your first Flask app
- Understanding routing and templates
- Best practices for Flask development

Flask follows the principle of "micro-framework" which means it provides the core features you need while remaining flexible and extensible.''',
                'author_name': 'John Doe',
                'category': 'Programming',
                'user_id': 2,  # Regular user
                'is_approved': True
            },
            {
                'title': 'Modern Web Development Trends',
                'content': '''The world of web development is constantly evolving. Here are some of the most important trends shaping the industry in 2026:

1. **Progressive Web Apps (PWAs)**: Combining the best of web and mobile apps
2. **Serverless Architecture**: Building scalable applications without server management
3. **AI Integration**: Incorporating machine learning and AI into web applications
4. **Enhanced Security**: Focus on cybersecurity and data protection
5. **Green Computing**: Sustainable and energy-efficient development practices

These trends are revolutionizing how we build and deploy web applications.''',
                'author_name': 'Jane Smith',
                'category': 'Technology',
                'user_id': 2,  # Regular user
                'is_approved': True
            }
        ]
        
        for post_data in sample_posts:
            self.create_post(
                post_data['title'],
                post_data['content'],
                post_data['author_name'],
                post_data['category'],
                post_data['user_id'],
                post_data['is_approved']
            )
    
    def create_post(self, title: str, content: str, author_name: str, category: str, 
                   user_id: Optional[int] = None, is_approved: bool = True) -> BlogPost:
        """
        Create a new blog post.
        
        Args:
            title (str): The title of the blog post
            content (str): The content of the blog post
            author_name (str): The name of the author
            category (str): The category of the blog post
        
        Returns:
            BlogPost: The newly created blog post
        
        Raises:
            ValueError: If any required field is empty or None
        """
        # Validate input
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if not content or not content.strip():
            raise ValueError("Content cannot be empty")
        if not author_name or not author_name.strip():
            raise ValueError("Author name cannot be empty")
        if not category or not category.strip():
            raise ValueError("Category cannot be empty")
        
        # Create new blog post
        new_post = BlogPost(
            title=title.strip(),
            content=content.strip(),
            author_name=author_name.strip(),
            category=category.strip(),
            user_id=user_id,
            is_approved=is_approved
        )
        
        # Add to the list
        self._posts.append(new_post)
        
        return new_post
    
    def edit_post(self, post_id: int, title: str = None, content: str = None, 
                  author_name: str = None, category: str = None) -> Optional[BlogPost]:
        """
        Edit an existing blog post.
        
        Args:
            post_id (int): The ID of the post to edit
            title (str, optional): New title for the post
            content (str, optional): New content for the post
            author_name (str, optional): New author name for the post
            category (str, optional): New category for the post
        
        Returns:
            BlogPost: The updated blog post, or None if post not found
        """
        post = self.get_post_by_id(post_id)
        if post:
            post.update(
                title=title.strip() if title else None,
                content=content.strip() if content else None,
                author_name=author_name.strip() if author_name else None,
                category=category.strip() if category else None
            )
            return post
        return None
    
    def delete_post(self, post_id: int) -> bool:
        """
        Delete a blog post by ID.
        
        Args:
            post_id (int): The ID of the post to delete
        
        Returns:
            bool: True if the post was deleted, False if not found
        """
        post = self.get_post_by_id(post_id)
        if post:
            self._posts.remove(post)
            return True
        return False
    
    def get_all_posts(self, include_unapproved: bool = False) -> List[BlogPost]:
        """
        Get all blog posts sorted by creation date (newest first).
        
        Args:
            include_unapproved (bool): Whether to include unapproved posts
        
        Returns:
            List[BlogPost]: List of blog posts
        """
        if include_unapproved:
            posts = self._posts
        else:
            posts = [post for post in self._posts if post.is_approved]
        
        return sorted(posts, key=lambda post: post.created_at, reverse=True)
    
    def get_post_by_id(self, post_id: int) -> Optional[BlogPost]:
        """
        Get a specific blog post by its ID.
        
        Args:
            post_id (int): The ID of the post to retrieve
        
        Returns:
            BlogPost: The blog post with the specified ID, or None if not found
        """
        for post in self._posts:
            if post.id == post_id:
                return post
        return None
    
    def search_posts_by_title(self, search_term: str, include_unapproved: bool = False) -> List[BlogPost]:
        """
        Search for blog posts by title (case-insensitive).
        
        Args:
            search_term (str): The term to search for in titles
            include_unapproved (bool): Whether to include unapproved posts
        
        Returns:
            List[BlogPost]: List of matching blog posts
        """
        if not search_term or not search_term.strip():
            return self.get_all_posts(include_unapproved)
        
        search_term = search_term.strip().lower()
        matching_posts = []
        
        for post in self._posts:
            if (include_unapproved or post.is_approved) and search_term in post.title.lower():
                matching_posts.append(post)
        
        return sorted(matching_posts, key=lambda post: post.created_at, reverse=True)
    
    def filter_posts_by_category(self, category: str, include_unapproved: bool = False) -> List[BlogPost]:
        """
        Filter blog posts by category (case-insensitive).
        
        Args:
            category (str): The category to filter by
            include_unapproved (bool): Whether to include unapproved posts
        
        Returns:
            List[BlogPost]: List of blog posts in the specified category
        """
        if not category or not category.strip():
            return self.get_all_posts(include_unapproved)
        
        category = category.strip().lower()
        matching_posts = []
        
        for post in self._posts:
            if (include_unapproved or post.is_approved) and post.category.lower() == category:
                matching_posts.append(post)
        
        return sorted(matching_posts, key=lambda post: post.created_at, reverse=True)
    
    def get_all_categories(self) -> List[str]:
        """
        Get a list of all unique categories.
        
        Returns:
            List[str]: List of unique categories
        """
        categories = set()
        for post in self._posts:
            categories.add(post.category)
        return sorted(list(categories))
    
    def get_posts_count(self) -> int:
        """
        Get the total number of posts.
        
        Returns:
            int: Total number of posts
        """
        return len(self._posts)
    
    def get_posts_by_author(self, author_name: str) -> List[BlogPost]:
        """
        Get all posts by a specific author.
        
        Args:
            author_name (str): The name of the author
        
        Returns:
            List[BlogPost]: List of posts by the author
        """
        if not author_name or not author_name.strip():
            return []
        
        author_name = author_name.strip().lower()
        matching_posts = []
        
        for post in self._posts:
            if post.author_name.lower() == author_name:
                matching_posts.append(post)
        
        return sorted(matching_posts, key=lambda post: post.created_at, reverse=True)
    
    def get_posts_by_user_id(self, user_id: int, include_unapproved: bool = True) -> List[BlogPost]:
        """
        Get all posts by a specific user ID.
        
        Args:
            user_id (int): The ID of the user
            include_unapproved (bool): Whether to include unapproved posts
        
        Returns:
            List[BlogPost]: List of posts by the user
        """
        matching_posts = []
        
        for post in self._posts:
            if post.user_id == user_id and (include_unapproved or post.is_approved):
                matching_posts.append(post)
        
        return sorted(matching_posts, key=lambda post: post.created_at, reverse=True)
    
    def get_pending_posts(self) -> List[BlogPost]:
        """
        Get all posts pending approval.
        
        Returns:
            List[BlogPost]: List of posts waiting for approval
        """
        pending_posts = [post for post in self._posts if not post.is_approved]
        return sorted(pending_posts, key=lambda post: post.created_at, reverse=True)
    
    def approve_post(self, post_id: int) -> bool:
        """
        Approve a blog post by ID.
        
        Args:
            post_id (int): The ID of the post to approve
        
        Returns:
            bool: True if the post was approved, False if not found
        """
        post = self.get_post_by_id(post_id)
        if post:
            post.approve()
            return True
        return False
    
    def reject_post(self, post_id: int) -> bool:
        """
        Reject/unapprove a blog post by ID.
        
        Args:
            post_id (int): The ID of the post to reject
        
        Returns:
            bool: True if the post was rejected, False if not found
        """
        post = self.get_post_by_id(post_id)
        if post:
            post.reject()
            return True
        return False