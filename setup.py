from setuptools import setup

setup(
    name="aio_telegram_log_handler",
    version="1.0.1",
    author="Daniil Solynin",
    author_email="solynynd@gmail.com",
    description="Package for send some important logs directly to telegram",
    classifiers=["Programming Language :: Python :: >3.9"],
    packages=["tghandler"],
    install_requires=["aiohttp >= 3.8.4"],
)
