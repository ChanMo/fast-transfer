import os
import uuid
import datetime
import flask

app = flask.Flask(__name__)
app.secret_key = str(uuid.uuid4())

directory = os.environ.get('FLASK_USER_DATA', os.getcwd())
if not directory.startswith("/"):
    directory = os.path.join(os.getcwd(), directory)

    
@app.route("/", methods=["GET", "POST"])
def index():
    dir = flask.request.args.get('dir', '')
    # Get the list of files in the current directory
    dir2 = os.path.join(directory, dir)
    
    if flask.request.method == "POST":
        # Get the file from the client
        file = flask.request.files["file"]

        # Save the file to the server
        file_path = os.path.join(dir2, file.filename)
        file.save(file_path)

        flask.flash('Upload Successfully.')

        return flask.redirect(f'/?dir={dir}')

    if flask.request.args.get('file'):
        f = flask.request.args.get('file')
        return flask.send_from_directory(dir2, f, as_attachment=True)

    files = os.listdir(dir2)

    # Create a list of links to the files
    links = []
    for file in files:
        f = os.path.join(dir2, file)
        isdir = os.path.isdir(f)
        dir_link = f"?dir={dir}/{file}" if dir else f'?dir={file}'
        file_link = f'?dir={dir}&file={file}'
        links.append({
            'file': file if not isdir else f'{file}/',
            'link': dir_link if isdir else file_link,
            'is_dir': isdir,
            'size': os.path.getsize(f),
            'ctime': datetime.datetime.fromtimestamp(int(os.path.getctime(f))),
            'mtime': datetime.datetime.fromtimestamp(int(os.path.getmtime(f)))
        })

    dirs = []
    if dir:
        for i in dir.split('/'):
            dirs.append({
                'name': i,
                'path': f'{dirs[-1]["path"]}/{i}' if len(dirs) else i
            })

    return flask.render_template("index.html", links=links, dirs=dirs)


if __name__ == "__main__":
    app.run(debug=True)
