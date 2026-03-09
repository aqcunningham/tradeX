1. check for the python version
python3 --version
2. if not installed:
brew install python
3. create virtual environment:
python3 -m venv venv
4. activate it:
source venv/bin/activate
5. update the pip:
pip install --upgrade pip
6. install all reqs from req.ttx:
pip install -r requirements.txt
7. to check the list of all installs:
pip install -r requirements.txt

8. live updates:
flask run --debug