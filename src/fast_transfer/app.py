import os
import uuid
import datetime
import flask
import click

app = flask.Flask(__name__)
app.secret_key = str(uuid.uuid4())


@app.route("/", methods=["GET", "POST"])
def index():
    root = app.config['USER_DATA']
    if not root.startswith("/"):
        root = os.path.join(os.getcwd(), root)
    
    folder = flask.request.args.get('dir', '')
    path = os.path.join(root, folder)
    
    if flask.request.method == "POST":
        # Get the file from the client
        file = flask.request.files["file"]

        # Save the file to the server
        file_path = os.path.join(path, file.filename)
        file.save(file_path)

        flask.flash('Upload Successfully.')

        return flask.redirect(f'/?dir={folder}')

    if flask.request.args.get('file'):
        f = flask.request.args.get('file')
        return flask.send_from_directory(path, f, as_attachment=True)

    files = os.listdir(path)

    # Create a list of links to the files
    links = []
    for file in files:
        f = os.path.join(path, file)
        isdir = os.path.isdir(f)
        dir_link = f"?dir={folder}/{file}" if folder else f'?dir={file}'
        file_link = f'?dir={folder}&file={file}'
        links.append({
            'file': file if not isdir else f'{file}/',
            'link': dir_link if isdir else file_link,
            'is_dir': isdir,
            'size': os.path.getsize(f),
            'ctime': datetime.datetime.fromtimestamp(int(os.path.getctime(f))),
            'mtime': datetime.datetime.fromtimestamp(int(os.path.getmtime(f)))
        })

    dirs = []
    if folder:
        for i in folder.split('/'):
            dirs.append({
                'name': i,
                'path': f'{dirs[-1]["path"]}/{i}' if len(dirs) > 0 else i
            })

    return flask.render_template("index.html", links=links, dirs=dirs)


@click.command()
@click.argument('userdata')
def cli(userdata):
    app.config.update(
        USER_DATA=userdata
    )
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    cli()
