from distutils.core import setup

arguments = dict(
        name = "Shapes",
        version = "1.0.0.0",
        description = "2D Game Utilities",

        author = "Kale Kundert",
        author_email = "kale@thekunderts.net"

        py_modules = ("vector", "shapes", "collisions") )

setup(**arguments)
