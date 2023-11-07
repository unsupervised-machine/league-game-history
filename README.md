## League of Legends Match History

### Description

This project is currently in development and aims to collect user
and match data from the Riot Games API, using a Flask backend, and
store this data in a MongoDB database. Additionally, it will provide
users with a React-based web application to view their own match history.
The project is being developed to help players of Riot Games' titles (e.g., League of Legends)
keep track of their in-game performance and match history.


### Table of Contents
- Prerequisites
- Setup
- Running the Project
- Contributing
- License

### Prerequisites
Before you begin, ensure you have met the following requirements:

- Python (3.7 or higher)
- Node.js and npm
- Riot Games API Key (to access the Riot API)
- MongoDB (installed and running)
- A web browser with JavaScript enabled


Setup

    Clone the project repository to your local machine:

```bash
git clone https://github.com/your-username/riot-match-history.git
```
Navigate to the project directory:

```bash
cd riot-match-history
```
Create a virtual environment (recommended):

```bash    
python -m venv venv
```
Activate the virtual environment:

On Windows:

```bash
venv\Scripts\activate
```

On macOS and Linux:

```bash
source venv/bin/activate
```
Install Python dependencies:

```bash 
pip install -r pyproject.toml
```
Navigate to the client directory for the React app:

```bash
cd client
```

Install Node.js dependencies:

```bash
npm install
```

### Configuration

Before you can run the project, you'll need to configure a few settings:

Create a .env file in the root directory of the project to store your environment variables. Add the following variables:

```makefile
RIOT_API_KEY=YOUR_RIOT_API_KEY
MONGO_URI=YOUR_MONGO_DB_URI
```
Replace YOUR_RIOT_API_KEY with your Riot Games API key and YOUR_MONGO_DB_URI with the URI for your MongoDB database.

Ensure that your MongoDB is running and accessible with the URI you provided in the .env file.

Running the Project

To run the project, follow these steps:

1. Start the Flask backend server (from the root project directory):

```bash
python app.py
```
2. Start the React development server (from the client directory):

```sql
    npm start
```
3. Access the web application by opening a web browser and navigating to http://localhost:3000.

### Contributing

If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository on GitHub.
2. Create a new branch with a descriptive name for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

License

This project is licensed under the [MIT License](https://chat.openai.com/c/LICENSE).