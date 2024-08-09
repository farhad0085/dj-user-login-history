import pathlib
from setuptools import setup

# The directory containing this file
BASE_PATH = pathlib.Path(__file__).resolve().parent

# The text of the README file
README = (BASE_PATH / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="dj-user-login-history",
    version="1.0.6",
    description="Django app which keep track of user login history.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/farhad0085/dj-user-login-history",
    author="Farhad Hossain",
    author_email="farhadhossain0085@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["login_history", "login_history/migrations"],
    include_package_data=True,
    install_requires=["django>=2.2"],
)

# build
# python setup.py sdist bdist_wheel
# upload to pypi
# twine upload dist/*