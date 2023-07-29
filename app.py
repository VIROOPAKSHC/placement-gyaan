from flask import Flask

app=Flask(__name__)

@app.route('/')
def hello():
	return "Hello and welcome to the flask project"

if __name__ == '__main__':
	app.run()