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

## Docs

Go in your browser to `http://localhost/docs` to see the auto-generated documentation.

## License

This project is licensed with the [GNU GENERAL PUBLIC LICENSE](https://github.com/sander1946/DreamySkySanctuary?tab=GPL-3.0-1-ov-file).
