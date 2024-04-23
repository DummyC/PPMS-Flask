# Project Procurement Monitoring System

schoo project full of jank
built with flask and bootstrap

## Setup Environment (on leenoox)

install python3 and virtualenv

```
apt install python3
pip3 install virtualenv
```

clone the repo & cd
```
git clone https://github.com/DummyC/PPMS-Flask.git && cd PPMS-Flask
```

initialize venv and source activate script
```
virtualenv env
source env/bin/activate
```

get dependencies
```
pip3 install -r requirements.txt
```

setup environment variables (your method of choice)
```
export SECRET_KEY='your-key-here'
export MAIL_SERVER_EMAIL='your-email-here'
export MAIL_SERVER_PASSWORD='your-password-here'
```

run app
```
python3 run.py
```

nyenyenyenyen

# HEWWOO

mockaroo sql for projects - https://www.mockaroo.com/8f524890
```
curl "https://api.mockaroo.com/api/8f524890?count=1000&key=null" > "project.sql"
```