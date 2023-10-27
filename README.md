# OpenAI-Powered News-Feed Application: Basic Database Sharding & Production-Ready Setup

Harness the power of OpenAI's API with a state-of-the-art news-feed app. This robust multi-database solution is meticulously crafted using Django, Vue.js, and GraphQL, offering a scalable foundation for your projects.

## Prerequisites

- Install the Python 3.11.
- Install the Rust Programming Language.
- Install the MySQL (the simplest solution - XAMPP).
- Create a SQLite3 Database Folder: Create a folder named "sqlite3" in your Django backend directory and place all your databases inside it. You can find database aliases in the `django_backend/core/utils/database_config.py` file.

NOTE. I am using the VSCODE for testing setup, running scripts from `launch.json`, etc.

## 🌟 Key Features

- **Advanced Database Management Starter**: The application features a foundational database sharding configuration, ensuring efficient data distribution and optimal performance.
- **Improved Django Settings Configuration**.
- **Project Management Scripts**.
- **Python Testing Configuration and Jupyter Notebooks**: Set up Python testing and use Jupyter notebooks for code analysis.
- **Web Page Text Scraping Crawler**.
- **OpenAI Integration**: Basic integration for answering questions based on the most similar context.
- **Robust Testing**: My commitment to reliability is unwavering.

## 🚀 What's Next?

- **Google Authentication**: Stay tuned for the upcoming integration of Google-based registration and login for a smoother user experience.
- **More Tests**: Expect additional tests to ensure application reliability.
- **Continuous Improvements**: I am always on the lookout for areas of improvement and am actively working on bug fixes.

## 🔧 Installation & Setup

### Google Cloud Storage [OPTIONAL]:

To utilize Google Cloud (GC) for image storage:

1. Set up a GC console account.
2. Initiate a new project within the GC console.
3. Configure Secret Manager secrets for your GC project.
4. Create a 'creds' directory, retrieve the `credentials.json` for your GC project, place it inside, and set an environment variable pointing to this file.


```bash
mkdir creds
```

### Backend Configuration:

Backend Configuration (Linux).
Initiate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Backend Configuration (Windows).
Initiate a virtual environment:

```bash
python -m venv .venv 
.venv\Scripts\activate
```

Install required packages.

```bash
pip install -r requirements.txt
```

Reset all databases.

```bash
cd django_backend
python reset_all_dbs.py
```

Run migrations.

```bash
python manage.py makemigrations
python migrate_all_dbs.py
```

Databases initial setup with records.

```bash
python databases_initial_setup.py
```

Start dev server.

```bash
python manage.py runserver
```

### Frontend Configuration:

Frontend Configuration.
Navigate to the frontend directory from the root and install the required packages:

```bash
cd vue_frontend
npm install
```

Start the frontend development server:

```bash
npm run serve
```

## Visual Tour:

News Feed Page

<!-- ![News Feed Page]() -->

Sign In Page

<!-- ![Sign In Page]() -->

Sign Up Page

<!-- ![Sign Up Page]() -->

Article Page

<!-- ![Article Page]() -->

User Profile Page

<!-- ![User Profile Page]() -->

Crafted with precision and expertise, this application is your gateway to next-gen news-feed solutions.
