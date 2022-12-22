from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import re

app = Flask(__name__)
path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def getHostedServerNames(filePath):
    filepath = filePath
    with open(filepath) as file:
        fileContent = file.read()
        serverNameList = re.findall(
            r"(server_name.*.qdply.com)", fileContent)
        serverNameList = serverNameList[1:]
        serverNameList = [serverName.split(" ")[1]
                          for serverName in serverNameList]
        return serverNameList

def getTimeStamp(filePath):
    filepath = filePath
    with open(filepath) as file:
        fileContent = file.read()
        timeStampList = re.findall(
            r"(Timestamp:.*\/*\/*)", fileContent)
        timeStampList = [(" ").join(timestamp.split(" ")[1:])
                          for timestamp in timeStampList]
        return timeStampList


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        data = {'message': 'Successfully uploaded'}
        files = request.files.getlist("file[]")
        projectName = request.form['projectName']
        projectType = request.form['type']
        print(projectName, projectType)

        for file in files:
            path = os.path.dirname(file.filename)
            path2 = os.path.join(app.config['UPLOAD_FOLDER'], path)
            print(path2)
            if not os.path.exists(path2):
                # os.mkdir(path2)
                os.makedirs(path2)
            filename = os.path.join(path, secure_filename(
                os.path.basename(file.filename)))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        folder = os.path.join(
            app.config['UPLOAD_FOLDER'], os.path.dirname(files[0].filename))

        new_name = os.path.join(app.config['UPLOAD_FOLDER'], projectName)

        os.rename(folder, new_name)

        print(f"running sudo ../qdply -n \"{projectName}\" -f {new_name} -t \"{projectType}\"")
        shellOutput = os.system(f"sudo ../qdply -n {projectName} -f {new_name} -t {projectType}")
        if shellOutput == 3:
            data['message'] = "Subdomain already in use. Please enter a different unique name."
        elif shellOutput == 1:
            data['message'] = "Serve process failed. Please try again."

        return render_template('uploaded.html', data=data)

    serverNameList = getHostedServerNames("/Users/rishi/projects/qdply-core/nginx-config/qdply")
    timeStampList = getTimeStamp("/Users/rishi/projects/qdply-core/nginx-config/qdply")
    return render_template('index.html', data=serverNameList, timestamp=timeStampList)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
