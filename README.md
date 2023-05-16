# Fitstar Pro Website

The Gym website is developed using the Django-Fullstack framework, incorporating a range of tools and technologies such as Python 3, Django 3.4, Bootstrap, JavaScript, jQuery, and Ajax. The project structure consists of distinct directories, including 'client' for end-user templates enabling signup, login, profile updates, blog addition, and role selection; 'superadmin' for managing clients and adding end-users; 'static' containing essential CSS, JS, and image files; 'FitStarPro' serving as the main Django project directory with the crucial 'settings.py' file; and 'requirement.txt' listing project dependencies. This organized structure and powerful tech stack ensure a robust and user-friendly Gym website experience.

## Tools and Technologies Used
This website for a Gym was built using the following tools and technologies:

    Python 3
    Django 3.4
    Django-Fullstack framework
    Bootstrap
    JavaScript
    jQuery
    Ajax

The combination of these technologies enables the development of a robust and interactive website for the Gym.

## Running the Project

To run the project, follow these steps:

1. Set up a virtual environment using the command: `python -m venv venv`
2. Activate the virtual environment.
3. Install the required packages by running: `pip install -r requirement.txt`
4. Start the Django development server: `python manage.py runserver`
5. Access the website in your browser at: `http://localhost:8000/`

## Project Structure

- `client`: Contains all the client templates where end-users can sign up, login, update their profiles, add blogs, and select their role (model, center, or professional).
- `superadmin`: Allows manipulation of clients and addition of end-users.
- `static`: Contains all the CSS, JS, and image files.
- `FitStarPro`: The main Django project directory where the `settings.py` file is located.
- `requirement.txt`: Lists the project dependencies.


Make sure you have Python 3 and Django 3.4 installed before running the project.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -am 'Add some feature'`
4. Push the branch to your forked repository: `git push origin feature-name`
5. Open a pull request on GitHub.

Please ensure that your code follows the project's coding conventions and includes appropriate tests.
