# GitHub Webhook Receiver & MongoDB UI
# Overview
This project aims to create a GitHub webhook receiver that listens for events such as Push, Pull Request, and Merge actions on a GitHub repository. Upon receiving these events, the data is stored in MongoDB. Additionally, a UI component periodically fetches data from MongoDB and displays the latest changes in the repository.

# Features
Receives GitHub webhook events for Push, Pull Request, and Merge actions.
Stores event data in MongoDB.
Provides a UI to view the latest changes in the repository.
Supports displaying events in a user-friendly format.

# Installation
Clone the repository from GitHub: git clone <repository-url>
Install dependencies: pip install -r requirements.txt
Set up MongoDB and configure connection settings in db_connection.py.
Start the Flask application: python app.py
