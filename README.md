# DreamySkySanctuary

The Website for the Dreamy Sky Sanctuary server

## Instalation

1. Clone the repository: `git clone https://github.com/sander1946/DreamySkySanctuary.git`
2. Create a vitual environment for the python project: `python -m venv .venv`
3. Activate the virtual environment: `./.venv/Script/activate` (or `source ./.venv/bin/activate` if you are on linux)
4. Install the python requirements: `pip install -r requirements.txt`
5. Go into the `src` folder: `cd src\`
6. Start the webserver: `uvicorn main:app`
7. The webserver should be running on `http://localhost` on port `80`

## File structure

```t
DreamySkySanctuary             # The project root folder
├── .venv/                      # your virtual envirement files
│   └── ...                     
├── src/                        # FastAPI source files
│   ├── config/                 # Here goes all the config of the project
│   │   ├── config.py           # The project wide config
│   │   └── __init__.py
│   ├── routes/                 # Here goed the python code for the diffrent sections of the website
│   │   ├── main/               # Here goes all the code for the main routes
│   │   │   ├── main.py
│   │   │   └── __init__.py
│   │   ├── auth/               # Here goed the python code for the authentication of the user
│   │   │   ├── auth.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── schemas/                # Here goed all the schemas for the database that the website can use
│   │   └── ...
│   ├── utils/                  # Here goes all the general uitls that the website can use
│   │   └── ...
│   ├── dependencies.py         # All the dependencies required for the app to run
│   ├── main.py                 # The main FastAPI app
│   └── __init__.py
├── templates/                  # Here goes all the HTML files of the website split per route
│   ├── attributes/             # Here goes all the html files of the different attributes of the site, like the navbar and the footer
│   │   ├── footer.html
│   │   └── header.html
│   ├── auth/                   # Here goes all the html files of the auth route
│   │   └── auth.html
│   ├── error/                  # Here goes all the html files of the diffrent posable errors
│   │   ├── 50x.html
│   │   └── 404.html
│   ├── main/                   # Here goes all the html files of the main route
│   │   └── index.html
│   └── base.html               # The base template that all the others build off of
├── public/                     # Here goes all the assets of the website
│   ├── img/                    # Here goes all the images of the website
│   │   └── ...
│   └── ...
├── static/                     # Here goes all the dependencie files like JS and CSS
│   ├── css/                    # Here goes all the CSS for the diffrent pages
│   │   ├── footer.css
│   │   ├── header.css
│   │   └── main.css
│   └── js/                     # Here goed all the JavaScript for the diffrent pages
│       └── main.js
├── requirements.txt            # The python requirements of the project
├── run.bat                     # Run this to start the webserver if you are on windows
├── README.md
├── .env                        # Your own filled in .env file
├── .env.example                # The example .env file you can copy and fill in
├── .gitignore
└── .gitattributes
```

## Docs

Go in your browser to `http://localhost/docs` to see the auto-generated documentation.

## License

This project is licensed with the [GNU GENERAL PUBLIC LICENSE](https://github.com/sander1946/DreamySkySanctuary?tab=GPL-3.0-1-ov-file).
