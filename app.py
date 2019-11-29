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
    <body bgcolor="e3fffd">
    <script src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js">
</script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
    <div class="txtCenter">
    <title>裂缝检测Demo</title>
    <h1>裂缝检测Demo</h1>  
             <br>
             <br>
         <button id="myBtn" >选择图片</button>
         <br> 
         <br>
         <br>
         <button id="myBtn2">开始预测</button>
         <br>    
    <form method=post enctype=multipart/form-data>
         <input type=file name=file id=myFile>
         <br>
         <input type=submit value=开始预测 id=myFile2>
    </form>
    </div>
    <style>  
.txtCenter{
    text-align:center;  
} 
#myFile {
    visibility: hidden; 
}
#myFile2 {
    visibility: hidden; 
}
#myBtn {

    /* 在这里自定义你的按钮样式 */
        background-color: #008CBA; 
    border: none;
    color: white;
    padding: 60px 100px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 30px;
    border-radius: 12px;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19)

}
#myBtn2 {

    /* 在这里自定义你的按钮样式 */
        background-color: #008CBA; 
    border: none;
    color: white;
    padding: 60px 100px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 30px;
    border-radius: 12px;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19)

}
</style>
<script type="text/javascript">
$('#myBtn').click(function() {

    $('#myFile').click(); // 模拟文件上传按钮点击操作

});
$('#myBtn2').click(function() {

    $('#myFile2').click(); // 模拟文件上传按钮点击操作

});
</script>
    '''
html2 = '''
    <!DOCTYPE html>
    <body bgcolor="e3fffd">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
    <div class="txtCenter">
    <title>裂缝检测Demo</title>
    <h1>裂缝检测Demo</h1>    
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
            return html2 + '<div class="txtCenter"><br><img src=' + file_url + ' height="400">' + results + '</div>'
    return html


if __name__ == '__main__':
    app.run()
	
