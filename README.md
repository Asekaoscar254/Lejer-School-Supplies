# Lejer Inventory Management

A Django inventory management system with role-based access control for Admin and Staff users.

## Getting Started

1. Create and activate a virtual environment:

```bash
python -m venv lejerenv
# Windows
lejerenv\Scripts\activate
# macOS/Linux
source lejerenv/bin/activate
```

2. Install dependencies:

```bash
pip install django
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Create a superuser:

```bash
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

## GitHub Push

1. Initialize git:

```bash
git init
```

2. Add files and commit:

```bash
git add .
git commit -m "Initial commit"
```

3. Add GitHub remote and push:

```bash
git remote add origin https://github.com/<your-username>/<your-repo>.git
git branch -M main
git push -u origin main
```

Replace `<your-username>` and `<your-repo>` with your GitHub account and repository name.
