## Prasanna Assessment Backend Folder Strucutre
project_folder/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
|   ├── utils.py
│   ├── routes/
│   │   ├── book_routes.py
│   │   ├── user_routes.py
|   ├── services/
│   │   ├── auth_services.py
│   └── static/
│       └── swagger.json
├── migrations/  # Created after running `flask db init`
│   ├── versions/
│   └── env.py
├── .env
├── requirements.txt
├── run.py
└── tests/
    ├── test_book_routes.py
    └── test_user_routes.py

# Dependencies
1. Python 3.9.x
2. PostgreSQL 14.*


# Setup Instructions

1. Create a virtual environment
      ```
      python3 -m venv venv
      ```

2. Activate the virtual environment
      ```
      source venv/bin/activate
      ```

3. Install the dependencies
      ```
      pip install -r requirements.txt
      ```

4. Create a .env file in the root directory and add the following environment variables

5. Run the applications
      ```
      flask run
      ```

6. Notes
   
   
   Initiate migration

         ```
         flask db init
         ```
      
   Generate new migrations

         ```
         flask db migrate -m "Initial migration."
            
         flask db revision --message <migration_name>
         ```
      
   Update existing migrations

      ```
      flask db upgrade
      ```

6. Weasyprint requirements
   
   
   Ubuntu

         ```
         apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

         ```

      
   
