# Fantasy Monitor

Fantasy Monitor is a Django-based web application designed to track player prices in LaLiga Fantasy and provide a personalized dashboard for monitoring selected players.

## Features

- Daily tracking of LaLiga Fantasy player prices
- Personalized dashboard for monitoring selected players

## Requirements

- Python 3.10+
- Django 5.1
- Other dependencies (listed in `requirements.txt`)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fantasy-monitor.git
   cd fantasy-monitor
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   python manage.py migrate
   ```

5. Create a superuser (admin) account:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage

1. Access the application at `http://localhost:8000`
2. Select players you want to monitor
3. View daily price updates on your personalized dashboard

## Contributing

We welcome contributions to Fantasy Monitor! Please feel free to submit issues, fork the repository and send pull requests!

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions, please open an issue on GitHub.

Happy fantasy managing!