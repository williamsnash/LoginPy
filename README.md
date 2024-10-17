# LoginPy
A simple login system using Python and SQLite3 to have a http server using Flask.

## What is included?
- Password hashing for secure storage
- User registration
- User
  - Login
  - Logout
  - Session management
  - Delete account
- 3 masonry layouts
- 2 function wraps
  - Login required - Used for html routes that require login
  - Api Auth required - Used for api routes that require login
- Pagination of large image folders
- Custom image folders not in static folder
- Reduce code logic for 3 masonry layout to help reduce change issues

## Setup/ Running
1. Install the required packages
    ```bash
    pip install -r requirements.txt
    ```
2. Run the server
    ```bash
    python server.py
    ```
3. If deploying for prod. Change api.run(debug=True) to api.run(debug=False) in server.py


## Files
### server.py
- The main file that runs the server
- Contains all the routes
- ONLY routes should be here (see server_helper.py)
## server_helper.py
- Contains the helper functions for the server
- Any functions that are not routes are here

# Docs/ Misc
## Masonry Layout
- [CSS-Masonry](https://w3bits.com/css-masonry/)
- [Masonry Viewer](https://github.com/alexwlchan/masonry-viewer)
- [Native Masonry](https://www.smashingmagazine.com/native-css-masonry-layout-css-grid/)

## Change string date to datetime
- `time = datetime.strptime(last_login, "%Y-%m-%d | %I:%M.%S %p")`