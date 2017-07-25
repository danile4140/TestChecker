# -*- coding:utf-8 -*-
'''
Created on 2017-3-15

@author: danny.deng

每增加一个新的地址映射文件，需要在app/__init__.py中添加对应的from app.views import xxxx
'''
from app import app
from app.utils import StringUtil, OtherUtil, RequestUtil
import flask
from flask.globals import request
from werkzeug.utils import secure_filename
import apk_private

@app.route('/apkcheck', methods=['GET'])
def apk_page():
    return flask.render_template('main/apkcheck_index.html')


allow_ext = ['apk']


# apk上传
@app.route('/apk_post', methods=['POST'])
def apk_post():
    rst = {}
    upload_file = request.files['file']
    fname = secure_filename(upload_file.filename)
    try:
        if StringUtil.is_file_ext_allowed(fname, allow_ext):
            pid, apkpath = RequestUtil.save_request_file(upload_file)
            rst['success'] = 1
            rst['data'], rst['chk_rst'] = apk_private.checkapk(apkpath)
        else:
            rst['success'] = 0
            rst['data'] = 'file ext is not allowed'
    except Exception, e:
        rst['success'] = 0
        rst['data'] = "包体错误或程序出现不可预知问题，请联系danny.deng" + '</br>Error:' + str(e)

    # delete upload file
    OtherUtil.del_file(apkpath)
    # resp = OtherUtil.object_2_json(rst)
    resp = flask.jsonify(rst)
    # resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp
