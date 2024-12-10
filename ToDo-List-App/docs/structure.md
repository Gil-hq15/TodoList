## 🛠️ **Project Structure**

```plaintext
.
├── app/                    # Core Flask application
│   ├── __init__.py         # App factory and extensions initialization
│   ├── models.py           # Database models (User and Todo)
│   ├── routes/             # Modularized route definitions
│   ├── static/             # Static files (CSS, JS, images)
│   └── templates/          # HTML templates for the app
├── config.py               # Configuration classes (development, testing, production)
├── run.py                  # App runner
├── requirements.txt        # Python dependencies
├── tests/                  # Unit, integration, acceptance, and performance tests
└── README.md               # Project documentation
```