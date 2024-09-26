# Front end design of Database

We uses Streamlit to create a simple frontend interface for managing a Chroma database. 

## Page Title: 

Displays "Chroma Database Management" as the page's title.

## Delete Database:

When the user clicks the "Delete Existing Database" button, the code tries to run a Python script named `delete_database_script.py`.

If successful, a success message "Database deleted" is shown to the user.

If the operation fails, an exception is caught, and an error message is displayed.

## Load New Documents and Update Database:

When the user clicks the "Load New Documents and Update Database" button, the code runs the `generate_data_store_script.py` script to load new documents and update the database.

A success message "Database updated" is displayed upon successful execution, and an error message is shown if it fails.

## Load JSON Documents and Update Database:

When the user clicks the "Load JSON Documents and Update Database" button, the `generate_json_data_store_script.py` script is executed.

A success message "JSON document database updated" is shown if the process is successful, while failure results in an error message.