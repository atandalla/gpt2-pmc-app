from flask import Flask
from flask_restful import Api
from servicios import IndexDocs, ResultSimi, GPT2

app = Flask(__name__)
api = Api(app)


api.add_resource(IndexDocs, '/api/search/documents/<string:getquery>')
api.add_resource(ResultSimi, '/api/search/Similarydocuments/<string:getquery1>')
api.add_resource(GPT2, '/api/search/GPT2/<string:getquery2>/<string:abstract1>')


@app.route('/')
def index() -> str:
    return "API PYTHON MACHINE LEARNING - ORDENAMIENTO DOCUMENTOS,SIMILITUD,GPT2"


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000,debug=True)
