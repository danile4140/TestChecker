Dropzone.autoDiscover = false;

var myDropzone = new Dropzone("#apk_file", {
    url: "/apk_post",
    maxFilesize: 1024,
    acceptedFiles: '.apk',
    maxFiles: 5,
    success: function (file, response, e) {
        if (response.success == 1) {
            //显示app信息
            $('#appname').text(response.data.appname);
            $('#packagename').text(response.data.packagename);
            $('#versionname').text(response.data.versionname);
            $('#versioncode').text(response.data.versioncode);

            //定义一个json对象，对应检查项显示,
            // chk_rst的key : 显示描述， a标签id
            var show_json = {
                "apk_include_file": "文件检查",
                "check_installLocation": "安装检查",
                "check_include_uses-permission": "权限检查",
                "check_include_meta-data": "meta检查",
                "check_intent": "intent-filter检查",
                "check_include_activity": "activity检查",
                "check_include_receiver": "receiver检查",
                "check_include_service": "service检查",
                "check_include_element":"element检查",
                "check_customized":"特殊检查点"
            };
            $('#chk').remove();
            html = '<table class="table table-hover" style="table-layout:fixed;word-break:break-all;">  <thead>  <tr> <th width=20%>检查内容</th>' +
                '<th width=10%>结果</th> <th>详细描述</th>  </tr>   </thead>   <tbody>';

            for (var i in response.chk_rst) {
                var content_html = '<tr> <td>' + show_json[i] + '</td>';


                var collapse_html = '<button class="btn btn-xs btn-primary collapsed" type="button" data-toggle="collapse" ' +
                    'data-target="#' + i + '" aria-expanded="false" aria-controls="' + i + '">详情' +
                    '</button>  <div class="collapse" id="' + i + '" aria-expanded="false" style="height: 0px;"> ' +
                    '<div class="well well-sm"> ';
                var sign = true;
                //若有error或者warning，则出现详情按钮
                // var result_html =  '<td style="color:Green"><strong>pass</strong>'
                if (response.chk_rst[i].error.length > 0) {
                    html = html + content_html + '<td style="color:Red "><strong>Fail</strong></td><td>' + collapse_html;
                    sign = false;
                }
                else if (response.chk_rst[i].warning.length > 0) {
                    html = html + content_html + '<td style="color:GoldenRod "><strong>warning</strong></td><td>' + collapse_html;
                    sign = false;
                }
                else {
                    html = html + content_html + '<td style="color:Green "><strong>Pass</strong></td><td>';
                }

                //处理error
                for (var j = 0; j < response.chk_rst[i].warning.length; j++)
                    html = html + '<li style="color:GoldenRod ">  <i class="icon-warning-sign"></i>&nbsp' + response.chk_rst[i].warning[j] + '</li>';

                //处理warning
                for (var j = 0; j < response.chk_rst[i].error.length; j++)
                    html = html + '<li style="color:FireBrick ">  <i class="icon-remove-sign"></i>&nbsp' + response.chk_rst[i].error[j] + '</li>';

                if (sign = false)
                    html = html + '</div> </div>';
                html = html + '</td></tr>'
            }
            html = html + '</tbody> </table>';
            $('#check_result').append(html);
        }
        else {
            html = '<div class="alert alert-danger"> <a href="#" class="close" data-dismiss="alert"> &times;' +
                '</a>' + response.data + '  </div>';
            $('#apk_file').append(html);
        }
    }
});