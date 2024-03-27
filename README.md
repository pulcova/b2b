# Install Python version 3.12 and above

# Create a virtual environment
python -m venv env

# Activate the virtual environment (for Linux/Mac)
source env/bin/activate

# Activate the virtual environment (for Windows)
env\Scripts\activate

# Install the required packages
pip install -r requirements.txt

# Create a superuser
python manage.py createsuperuser

# In Django admin, create three groups: owner, dealer, retailer

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run the server
python manage.py runserver