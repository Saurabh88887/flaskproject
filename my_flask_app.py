from flask import Flask  # Import Flask

# Create a Flask application instance
my_app = Flask(__name__)

# Define a route for the root URL ('/')
@my_app.route('/')
def hello_world():
    return 'Hello, Flask!'  # Return a response

# Run the app only if this script is executed directly
if __name__ == '__main__':
    my_app.run(debug=True)  # Enable debug mode for development
