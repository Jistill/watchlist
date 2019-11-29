import os
import net
import time
from flask import Flask, request, url_for, send_from_directory
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','JPG','PNG','JPEG'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/uploads'
app.config['MAX_CONTENT_LENGTH'] = 160 * 10240 * 10240


html = '''
    <!DOCTYPE html>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
    <div class="txtCenter">
    <title>裂缝检测Demo</title>
    <h1>裂缝检测Demo</h1>    
    <form method=post enctype=multipart/form-data>
         <input type=file name=file > 
         <input type=submit value=预测>
    </form>
    </div>
    <style>  
.txtCenter{
    text-align:center;  
} 
</style>
    '''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = url_for('uploaded_file', filename=filename)
            area = 'uploads/' + filename
            re = net.get_label(area)
            results = '<br><h2>' + re +'</h2>'
            return html + '<div class="txtCenter"><br><img src=' + file_url + ' height="400">' + results + '</div>'
    return html


if __name__ == '__main__':
    app.run()
	
