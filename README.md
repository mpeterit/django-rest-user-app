# Django User Management App: An Example Project

This Django REST Framework project is an example implementation of a user management application. It serves as a
starting point for developers who are building Django apps requiring custom user data handling and user profile
management.

## Project Description

The main objective of this example project is to showcase how to create, update, and manage users and store
user-specific data in Django, demonstrating key concepts and best practices. This application introduces a framework
that you can individualize to your project's specific needs.

Key concepts covered:

* **Email Authentication**: How to replace the traditional username with an email for authentication purposes. This
  allows users to register and log in using their unique email addresses. This approach can be extended or modified
  based on specific project needs.

* **Profile Management**: The project showcases how to create and manage user profiles that are linked to the primary
  user model. This structure enables the storing of additional, non-authentication related information, like profile
  pictures, gender, and birthdate.

* **Image Handling**: The project includes an example of how to allow users to upload, update, and store images (profile
  pictures in this case). All uploaded pictures are automatically resized and optimized to improve performance and save
  storage space. This concept could be further expanded to handle other file types.

* **Data Validation**: The application provides an example of backend validation of data values to ensure data integrity
  and enforce business rules. For example, the system validates that the birthdate provided by the user is not in the
  future. This validation approach can be adapted for a wide range of data integrity requirements.

* **Custom Permissions**: The project demonstrates how to define and enforce a custom set of permissions for different
  user operations. This can be adjusted and extended to match more complex access control rules.

## System Architecture

This example application is built on the Django REST Framework and uses an extensible `User` model for user management.
The `User` model extends Django's `AbstractUser` model, with the email field serving as the username field.
The `UserProfile` model, linked to the `User` model via a `OneToOneField`, is used to store additional user data.

The `UserSerializer` and `UserProfileSerializer` classes in the `user/serializers.py` file manage the serialization and
deserialization of `User` and `UserProfile` instances, implement data validation, and save instances to the database.

The `UserViewSet` class in the `user/views.py` file provides the CRUD operations for the `User` model. It defines
permissions for different operations, based on the user's role and the specific action being performed.

## Installation

Follow the instructions below to get this project up and running on your local machine:

1. Clone this repository:
    ```
    git clone https://github.com/your-username/django-user-app.git
    ```
2. Navigate to the project directory:
    ```
    cd django-user-app
    ```
3. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Run the migrations:
    ```
    python manage.py migrate
    ```
5. Start the server:
    ```
    python manage.py runserver
    ```

## Usage

After you have the server running, you can interact with the API:

1. **Register a new user**: Make a POST request to `http://localhost:8000//users/` with the email, password, password2,
   and
   user_profile data.
2. **Update a user profile**: Make a PUT request to `http://localhost:8000//users/<user-id>/` with the new user data.

The source code contains detailed comments explaining each function and class, serving as a guide for customizing the
code to your needs.

## Testing

Tests are located in the `user/tests.py`.

Remember, this project serves as an illustrative example, demonstrating key concepts and practices of Django REST
Framework user management. It's not a one-size-fits-all solution, but a starting point. Feel free to explore, modify,
and tailor the structure and code to fit your project's requirements.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file.