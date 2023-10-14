# OpenAI-Powered News-Feed Application: Basic Database Sharding & Production-Ready Setup

Harness the power of OpenAI's API with a state-of-the-art news-feed app. This robust multi-database solution is meticulously crafted using Django, Vue.js, and GraphQL, offering a scalable foundation for your projects.

## 🌟 Key Features

- **Advanced Database Management**: The application features a foundational database sharding configuration, ensuring efficient data distribution and optimal performance.

## 🚀 What's Next?

- **OpenAI Integration**: Stay tuned for upcoming features that will leverage OpenAI's API to dynamically generate news feeds.
- **Google Authentication**: I am working on integrating Google-based registration and login for a smoother user experience.
- **Robust Testing**: My commitment to reliability is unwavering. Expect an enhanced auto-testing suite soon.
- **Continuous Improvements**: I am always on the lookout for areas of improvement and am actively working on bug fixes.

## 🔧 Installation & Setup

### Google Cloud Storage:

To utilize Google Cloud (GC) for image storage:

1. Set up a GC console account.
2. Initiate a new project within the GC console.
3. Configure Secret Manager secrets for your GC project.
4. Create a 'creds' directory, retrieve the `credentials.json` for your GC project, place it inside, and set an environment variable pointing to this file.


```bash
mkdir creds
```

Backend Configuration (Linux).
Navigate to the backend directory and initiate a virtual environment:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

Backend Configuration (Windows).
Navigate to the backend directory and initiate a virtual environment:

```bash
cd backend
python -m venv .venv 
.venv\Scripts\activate
```

Install required packages.

```bash
pip install -r requirements.txt
```

Reset all databases.

```bash
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

Frontend Configuration.
Navigate to the frontend directory and install the required packages:

```bash
cd vue-frontend
npm install
```

Start the frontend development server:

```bash
npm run serve
```

## Visual Tour

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
