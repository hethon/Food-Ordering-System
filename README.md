
# How to Run the Food Ordering System Project

## Prerequisites
1. Ensure you have Python 3.8 or above installed on your machine.

## Setting Up the Project

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd hethon-Food-Ordering-System
   ```

2. **Create a Virtual Environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Update the `.env` file with your values for:
     - `SECRET_KEY`
     - `CHAPA_SECRET_KEY`

5. **Initialize the Database**:
   - Create the database:
     ```bash
     flask db init
     flask db migrate -m "Initial migration"
     flask db upgrade
     ```
   - (Optional) Populate the database with mock data:
     ```bash
     python scripts.py
     ```

6. **Run the Development Server**:
   - Use Flask's built-in development server:
     ```bash
     flask run
     ```

7. **Access the Application**:
   - Open your browser and go to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Additional Scripts

- **Adding Mock Data**:
  To populate the menu and admin data, uncomment the respective sections in `scripts.py` and run:
  ```bash
  python scripts.py
  ```

- **Flask Shell**:
  Access a shell with preloaded context:
  ```bash
  flask shell
  ```

## Notes
- Use the `Admin` account (`admin@fos.com`) for administrative access.
- The default admin password is stored in the `.env` file as `ADMIN_PASS`. Update it for security.

## Troubleshooting
- Ensure all environment variables are properly configured in the `.env` file.
- Check Flask logs for errors if the server fails to start.

---