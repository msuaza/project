## Weather Scraper Project

## Overview

This project is a web scraper that extracts weather forecast data from a specific website and displays it using a Flask web application. It also includes functionality to plot temperature trends over time.

## Setup
Clone the repository to your local machine:

```bash
git clone <repository_url>
```

Navigate to the project directory:

```bash
cd weather-scraper-project
```

Create a virtual environement to isolate and manage project dependencies:

```bash
python -m venv env
env\Scripts\activate
```

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

Set up your environment variables by creating a .env file in the project directory. Include the following variables:
plaintext

```
DBNAME=<your_dbname>
USER=<your_username>
PASSWORD=<your_password>
HOST=<your_host>
```

Run the Flask web application:

```bash
python db.py
```

Once the Flask app is running, you can access the weather forecast data at http://localhost:5000/weather and the temperature trends plot at http://localhost:5000/temperature_trends.

## Testing

To run the unit tests for the project, execute the following command:

```bash
python -m unittest test_project.py
```

This will run the test cases defined in test_project.py and display the results.
