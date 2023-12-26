setup:
	python3 -m venv ~/.car-prices-prediction
	# source ~/.car-prices-prediction/

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
