# chat_application_API

This project implements a RESTful API for a chat application, providing various endpoints for user registration, login, note management, and version history retrieval.

Endpoints

User Registration

    Endpoint: POST /signup
    Functionality: Allows users to create an account by providing necessary information such as username, email, and password.
    Output:
        If the registration is successful, return a success message or status code.
        If there are validation errors or the username/email is already taken, return appropriate error messages or status codes.

User Login

    Endpoint: POST /login
    Functionality: Allows users to log in to their account by providing their credentials (username/email and password).
    Output:
        If the login is successful, return an authentication token or a success message with the user details.
        If the credentials are invalid, return an error message or status code.

Create New Note

    Endpoint: POST /notes/create
    Functionality: Create a new note. Only authenticated users can create a new note.
    Output:
        If the request is valid, return a success message with status code.
        If the request is invalid, return an error message or status code.

Get a Note

    Endpoint: GET /notes/{id}
    Functionality: Get a note by its ID. Only authenticated users. A note is viewable by its owner and the shared users only.
    Output:
        If the request is valid, return a success message with the note content.
        If the request is invalid, return an error message with status code.

Share a Note

    Endpoint: POST /notes/share
    Functionality: Share a note with other users. Users can be parsed in the request body. Once the note admin executes this POST API, the users embedded in the request body will be able to view and edit the note.
    Output:
        If the request is valid, return a success message with the appropriate status code.
        If the request is invalid, return an error message or status code.

Update a Note

    Endpoint: PUT /notes/{id}
    Functionality: Edit a note. The note will be editable by admin and all the shared users. All users who have access to the note can edit it. Updates to the notes are tracked with a timestamp.
    Output:
        If the request is valid, return a success message with the appropriate status code.
        If the request is invalid, return an error message or status code.

Get Note Version History

    Endpoint: GET /notes/version-history/{id}
    Functionality: Get the version history of the note. Accessible by users having access only. This includes all the changes made to the note since its creation, including timestamps, users who made the changes, and the changes made to the note.
    Output:
        If the request is valid, return the response with the appropriate status code.
        If the request is invalid, return an error message or status code.

