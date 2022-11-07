from flask import Flask, request, send_file, jsonify
from pytube import YouTube
import tempfile

app = Flask("__name__")


@app.route("/mp4/<video>", methods=['GET'])
def mp4(video):
    if request.method == "GET":
        url = f'https://www.youtube.com/watch?v={video}'
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True).get_lowest_resolution()
        title = yt.title + '.mp4'
        file = tempfile.NamedTemporaryFile(prefix="tmp_", delete=False)
        streams.download(filename=file.name, timeout=80)
        return send_file(file.name, as_attachment=True, download_name=title)


@app.route("/mp3/<video>", methods=["GET"])
def mp3(video):
    if request.method == "GET":
        url = f'https://www.youtube.com/watch?v={video}'
        yt = YouTube(url)
        streams = yt.streams.filter(only_audio=True).order_by('abr')
        stream = streams[-1]
        title = streams[-1].title + '.mp3'
        file = tempfile.NamedTemporaryFile(prefix="tmp_", delete=False)
        stream.download(filename=file.name, timeout=80)
        return send_file(file.name, as_attachment=True, download_name=title)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5500', debug=True)