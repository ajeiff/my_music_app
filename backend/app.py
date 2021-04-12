import json

from flask import Flask

app = Flask(__name__)


@app.route('/audios', methods=['GET'])
def dict_music_api():
    audios = {}
    dict_music(audios=audios)
    return json.dumps(audios)


if __name__ == '__main__':
    app.run()
    print("back server launched...")
