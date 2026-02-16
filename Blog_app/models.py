"""
Blog Models Module
Contains the BlogPost class definition for the blog application.
"""

from datetime import datetime
from typing import Optional
import hashlib


class User:
    """
    User class to represent users with authentication and role management.
    
    Attributes:
        id (int): Unique identifier for the user
        username (str): Unique username for login
        email (str): User's email address
        password_hash (str): Hashed password for security
        role (str): User role ('admin' or 'user')
        is_active (bool): Whether the user account is active
        created_at (datetime): When the user account was created
    """
    
    # Class variable to auto-increment IDs
    _next_id = 1
    
    def __init__(self, username: str, email: str, password: str, role: str = 'user'):
        """
        Initialize a new User instance.
        
        Args:
            username (str): The username for login
            email (str): The user's email address
            password (str): The plain text password (will be hashed)
            role (str): The user role ('admin' or 'user')
        """
        self.id = User._next_id
        User._next_id += 1
        self.username = username.lower().strip()
        self.email = email.lower().strip()
        self.password_hash = self._hash_password(password)
        self.role = role
        self.is_active = True
        self.created_at = datetime.now()
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash."""
        return self.password_hash == self._hash_password(password)
    
    def is_admin(self) -> bool:
        """Check if the user has admin privileges."""
        return self.role == 'admin'
    
    def to_dict(self) -> dict:
        """Convert user to dictionary (excluding password)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __str__(self) -> str:
        return f"User(id={self.id}, username='{self.username}', role='{self.role}')"


class BlogPost:
    """
    BlogPost class to represent a blog post with all required fields.
    
    Attributes:
        id (int): Unique identifier for the blog post
        title (str): Title of the blog post
        content (str): Main content/body of the blog post
        author_name (str): Name of the author who wrote the post
        category (str): Category that the blog post belongs to
        created_at (datetime): Timestamp when the post was created
    """
    
    # Class variable to auto-increment IDs
    _next_id = 1
    
    def __init__(
        self, 
        title: str, 
        content: str, 
        author_name: str, 
        category: str,
        post_id: Optional[int] = None,
        user_id: Optional[int] = None,
        is_approved: bool = True
    ):
        """
        Initialize a new BlogPost instance.
        
        Args:
            title (str): The title of the blog post
            content (str): The main content of the blog post
            author_name (str): The name of the author
            category (str): The category of the blog post
            post_id (Optional[int]): Optional ID for the post (auto-generated if None)
        """
        if post_id is None:
            self.id = BlogPost._next_id
            BlogPost._next_id += 1
        else:
            self.id = post_id
            # Update the next_id if necessary to avoid conflicts
            if post_id >= BlogPost._next_id:
                BlogPost._next_id = post_id + 1
                
        self.title = title
        self.content = content
        self.author_name = author_name
        self.category = category
        self.user_id = user_id  # ID of the user who created the post
        self.is_approved = is_approved  # Whether the post is approved by admin
        self.created_at = datetime.now()
    
    def __str__(self) -> str:
        """Return a string representation of the blog post."""
        return f"BlogPost(id={self.id}, title='{self.title}', author='{self.author_name}', category='{self.category}')"
    
    def __repr__(self) -> str:
        """Return a detailed string representation of the blog post."""
        return (f"BlogPost(id={self.id}, title='{self.title}', "
                f"content='{self.content[:50]}...', author_name='{self.author_name}', "
                f"category='{self.category}', created_at='{self.created_at}')")
    
    def to_dict(self) -> dict:
        """
        Convert the BlogPost instance to a dictionary.
        
        Returns:
            dict: Dictionary representation of the blog post
        """
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_name': self.author_name,
            'category': self.category,
            'user_id': self.user_id,
            'is_approved': self.is_approved,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def approve(self):
        """Approve the blog post."""
        self.is_approved = True
    
    def reject(self):
        """Reject/unapprove the blog post."""
        self.is_approved = False
    
    def update(
        self, 
        title: Optional[str] = None, 
        content: Optional[str] = None, 
        author_name: Optional[str] = None, 
        category: Optional[str] = None
    ):
        """
        Update the blog post fields.
        
        Args:
            title (Optional[str]): New title (if provided)
            content (Optional[str]): New content (if provided)
            author_name (Optional[str]): New author name (if provided)
            category (Optional[str]): New category (if provided)
        """
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        if author_name is not None:
            self.author_name = author_name
        if category is not None:
            self.category = category