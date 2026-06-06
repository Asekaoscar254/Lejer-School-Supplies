# Lejer Inventory Management

Lejer is a Django-based inventory management system built for schools and laboratories. It includes role-based access control so that Admin and Staff users see only the pages and actions they are permitted to access.

## Key Features

- User authentication using Django's built-in `django.contrib.auth`
- Role-based access control using `Admin` and `Staff` groups
- Admin users can access all system views and manage products, stock, and orders
- Staff users are restricted to inventory overview and dashboard review pages
- Admin and Staff dashboards redirect users appropriately after login

## Application Structure

- `main/` – core app containing models, views, templates, and forms
- `lejer/` – project configuration and URL routing
- `lejerenv/` – local Python virtual environment (excluded from git)

## Setup

1. Create and activate a Python virtual environment:

```bash
python -m venv lejerenv
# Windows
lejerenv\Scripts\activate
# macOS/Linux
source lejerenv/bin/activate
```

2. Install Django and required dependencies:

```bash
pip install django
```

3. Run database migrations:

```bash
python manage.py migrate
```

4. Create a superuser to access the admin site:

```bash
python manage.py createsuperuser
```

5. Start the development server:

```bash
python manage.py runserver
```

6. Open the application in your browser:

```
http://127.0.0.1:8000/
```

## Role-Based Access Control

This project uses Django Groups to distinguish between user roles:

- `Admin` group: full access to all views and management actions
- `Staff` group: limited access to inventory display and review pages only

### Assigning Roles

Use the Django admin to assign users to groups, or use the shell:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User, Group

admin_group, _ = Group.objects.get_or_create(name='Admin')
staff_group, _ = Group.objects.get_or_create(name='Staff')

user = User.objects.get(username='your-user')
user.groups.add(staff_group)
```

## Login Behavior

After login, users are redirected as follows:

- Admin users → `admin_dashboard`
- Staff users → `staff_dashboard`

Unauthorized access is blocked by view decorators, so Staff users cannot reach Admin-only pages.

## GitHub Push

1. Initialize git if this repository is not already version controlled:

```bash
git init
```

2. Add project files and commit:

```bash
git add .
git commit -m "Initial commit"
```

3. Add your GitHub remote and push:

```bash
git remote add origin https://github.com/<your-username>/<your-repo>.git
git branch -M main
git push -u origin main
```

Replace `<your-username>` and `<your-repo>` with your GitHub account and repository name.
