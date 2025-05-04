# URL Shortener

A RESTful API service for shortening URLs with a minimal frontend interface.

## Features

- Create, retrieve, update and delete shortened URLs
- Get usage statistics for shortened URLs
- Simple frontend interface for URL shortening
- RESTful API following best practices

## Tech Stack

- Backend: Python (Flask)
- Database: MongoDB
- Frontend: HTML, CSS, JavaScript

## Setup Instructions

### Prerequisites

- Python 3.8+
- MongoDB

### Installation

1. Clone the repository
   ```
   git clone <repository-url>
   cd url_shortener
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Set up MongoDB
   - Make sure MongoDB is running on your system
   - The application will connect to MongoDB at localhost:27017 by default

5. Start the application
   ```
   python app.py
   ```

6. Access the application
   - API endpoints available at http://localhost:5000/
   - Frontend interface available at http://localhost:5000/

## API Endpoints

- `POST /shorten` - Create a new short URL
- `GET /shorten/<shortCode>` - Retrieve original URL data
- `PUT /shorten/<shortCode>` - Update an existing short URL
- `DELETE /shorten/<shortCode>` - Delete a short URL
- `GET /shorten/<shortCode>/stats` - Get usage statistics for a short URL
- `GET /<shortCode>` - Redirect to the original URL

## Project Structure

```
url_shortener/
├── app.py              # Main application entry point
├── config.py           # Configuration settings
├── requirements.txt    # Project dependencies
├── static/             # Static files (CSS, JS)
├── templates/          # HTML templates
├── services/           # Business logic
│   ├── __init__.py
│   └── url_service.py   
├── models/             # Database models
│   ├── __init__.py
│   └── url.py
└── utils/              # Utility functions
    ├── __init__.py
    └── shortcode_generator.py
``` 