# 📝 Blog API  – Django REST Framework

A simple blogging platform backend built using Django and Django REST Framework.  
Users can create blog posts, comment on others' posts, and retrieve post details using token-based authentication via `Simple JWT`.

---

## 🚀 Features

- JWT Authentication using `djangorestframework-simplejwt`
- Create, list, and delete blog posts
- Add comments to posts
- Retrieve a post along with its comments and author info
- Pagination for posts and comments
- Only the post author can delete their post

---

## 📦 Tech Stack

- Python 
- Django 
- Django REST Framework
- Simple JWT
- SQLite (for development)

---

## 🔐 Authentication

Uses `Simple JWT`.  
After login, you'll receive an access and refresh token.

### Obtain Token

```http
POST /api/token/
{
  "username": "your_username",
  "password": "your_password"
}
```

---
## Setup Instructions

*1. Clone the repository*

```
git clone https://github.com/your-username/blog-platform.git
cd blogapi

```

*2. Create and activate a virtual environment*

```
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Unix/macOS

```
*3. Install dependencies*

```
pip install -r requirements.txt

```
*4 Run migrations*

```
Python manage.py makemigrations appname
Python manage.py migrate

```
*5 Create a Super User /Reguler User*

```
from django.contrib.auth.models import User

Create a superuser (is_staff=True, is_superuser=True)
User.objects.create_superuser(username='admin', email='admin@example.com', password='admin123')

Create a regular user
User.objects.create_user(username='john', email='john@example.com', password='john123')

```
*6. Start the server*

```
python manage.py runserver

```
---

## 📌 Notes
- You can change pagination size using PageNumberPagination.page_size in views.

- Ensure rest_framework and rest_framework_simplejwt are installed and configured in settings.py.




