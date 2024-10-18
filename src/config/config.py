import os
VERSION: str = '0.0.1'
APP_NAME: str = 'DreamySkySanctuary'
DESCRIPTION: str = 'The website of the Dreamy Sky Sanctuary, a discord server about the game Sky: Children of the Light.'

BASE_DIR: str = os.getcwd()
TEMPLATES_DIR: str = os.path.join(BASE_DIR, "templates")
PUBLIC_DIR: str = os.path.join(BASE_DIR, "public")
STATIC_DIR: str = os.path.join(BASE_DIR, "static")