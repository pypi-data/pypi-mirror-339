from . import app
from . import image as image_command

app.add_typer(image_command.app, name='image')
