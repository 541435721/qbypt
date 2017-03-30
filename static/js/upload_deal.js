/**
 * Created by k on 2016/8/22.
 */

function del(file_name) {
    var regS = /\\/g;
    b = "%\"" + file_name.replace(regS, '\\\\') + "\"%";
    var reg = RegExp(b, "g");
    $.post("/profile_delte/", {delete_file: file_name});
    $("#id_dir").val(($("#id_dir").val().replace(reg, "")));
}
$(document).ready(function () {
    $('#file_upload').uploadify({
        'swf': '/static/js/uploadify.swf',//
        'uploader': '/uploadify_script/?project_id='+$("#project_ID").val()+'&classify='+$("#id_classify").val(),
        'folder': '/uploadfile',
        'auto': false,//false,//
        'multi': true,//设置可以上传多个文件
        'uploadLimit': 20,
        'buttonText': '选择文件',
        'removeCompleted': false,//
        'fileSizeLimit': '1024MB',//设置上传文件大小单位kb
        'fileTypeExts': '*.doc;*.docx;*.odt;*.jpg;*.png;*.txt;*exe;*.mp4;*.stl;',//设置上传文件类型为常用文档格式

        'onSelect': function (e, queueId, fileObj) {
            $('#id_span_msg').html("");
        },
        'onCancel': function (event, ID, fileObj, data) {
        },
        'onUploadComplete': function (file) {
        },
        'onUploadSuccess': function (file, data, response) {
            var regS = /\\\\/g;
            b = data.replace(regS, "\\");
            $("#" + file.id + " a:first-child").attr("onclick", "javascript:del(" + data + ")");
            $("#id_upload_name").val($("#id_upload_name").val() + b);
            //这里写的id_dir并不是说连接到网页中id为id_dir的元素，而是定位到id为dir的元素，这个id，如果是用forms类直接
            //传到网页的话，id也就是在forms.From中定义的类的变量名，比如这里的dir，就可以是对应form表单中的一个名为dir的变量
        }
    });
    $('#file_upload2').uploadify({
        'swf': '/static/js/uploadify.swf',//根据文件存放地址改变
        'uploader': '/admin_uploadify_script/?order_id=' + $("#order_id").val() + "&stlType=1",
        'folder': '/uploadfile',
        'auto': true,//false,//
        'multi': false,//设置可以上传多个文件
        'uploadLimit': 20,
        'buttonText': '选择文件',
        'removeCompleted': false,//
        'fileSizeLimit': '1024MB',//设置上传文件大小单位kb
        'fileTypeExts': '*.stl;',//设置上传文件类型为常用文档格式
        'onSelect': function (e, queueId, fileObj) {
            $('#id_span_msg').html("");
        },
        'onCancel': function (event, ID, fileObj, data) {
        },
        'onUploadComplete': function (file) {
        },
        'onUploadSuccess': function (file, data, response) {
            $("#" + file.id + " a:first-child").attr("onclick", "javascript:del(" + data + ")");
        }
    });

    $('#file_upload3').uploadify({
        'swf': '/static/js/uploadify.swf',//根据文件存放地址改变
        'uploader': '/admin_uploadify_script/?order_id=' + $("#order_id").val() + "&stlType=2",
        'folder': '/uploadfile',
        'auto': true,//false,//
        'multi': false,//设置可以上传多个文件
        'uploadLimit': 20,
        'buttonText': '选择文件',
        'removeCompleted': false,//
        'fileSizeLimit': '1024MB',//设置上传文件大小单位kb
        'fileTypeExts': '*.stl;',//设置上传文件类型为常用文档格式
        'onSelect': function (e, queueId, fileObj) {
            $('#id_span_msg').html("");
        },
        'onCancel': function (event, ID, fileObj, data) {
        },
        'onUploadComplete': function (file) {
        },
        'onUploadSuccess': function (file, data, response) {
            $("#" + file.id + " a:first-child").attr("onclick", "javascript:del(" + data + ")");
        }
    });

    $('#file_upload4').uploadify({
        'swf': '/static/js/uploadify.swf',//根据文件存放地址改变
        'uploader': '/admin_uploadify_script/?order_id=' + $("#order_id").val() + "&stlType=3",
        'folder': '/uploadfile',
        'auto': true,//false,//
        'multi': false,//设置可以上传多个文件
        'uploadLimit': 20,
        'buttonText': '选择文件',
        'removeCompleted': false,//
        'fileSizeLimit': '1024MB',//设置上传文件大小单位kb
        'fileTypeExts': '*.stl;',//设置上传文件类型为常用文档格式
        'onSelect': function (e, queueId, fileObj) {
            $('#id_span_msg').html("");
        },
        'onCancel': function (event, ID, fileObj, data) {
        },
        'onUploadComplete': function (file) {
        },
        'onUploadSuccess': function (file, data, response) {
            $("#" + file.id + " a:first-child").attr("onclick", "javascript:del(" + data + ")");
        }
    });

    $('#file_upload5').uploadify({
        'swf': '/static/js/uploadify.swf',//根据文件存放地址改变
        'uploader': '/admin_uploadify_script/?order_id=' + $("#order_id").val() + "&stlType=4",
        'folder': '/uploadfile',
        'auto': true,//false,//
        'multi': false,//设置可以上传多个文件
        'uploadLimit': 20,
        'buttonText': '选择文件',
        'removeCompleted': false,//
        'fileSizeLimit': '1024MB',//设置上传文件大小单位kb
        'fileTypeExts': '*.stl;',//设置上传文件类型为常用文档格式
        'onSelect': function (e, queueId, fileObj) {
            $('#id_span_msg').html("");
        },
        'onCancel': function (event, ID, fileObj, data) {
        },
        'onUploadComplete': function (file) {
        },
        'onUploadSuccess': function (file, data, response) {
            $("#" + file.id + " a:first-child").attr("onclick", "javascript:del(" + data + ")");
        }
    });

    $('#file_upload6').uploadify({
        'swf': '/static/js/uploadify.swf',//根据文件存放地址改变
        'uploader': '/admin_uploadify_script/?order_id=' + $("#order_id").val() + "&stlType=5",
        'folder': '/uploadfile',
        'auto': true,//false,//
        'multi': false,//设置可以上传多个文件
        'uploadLimit': 20,
        'buttonText': '选择文件',
        'removeCompleted': false,//
        'fileSizeLimit': '1024MB',//设置上传文件大小单位kb
        'fileTypeExts': '*.stl;',//设置上传文件类型为常用文档格式
        'onSelect': function (e, queueId, fileObj) {
            $('#id_span_msg').html("");
        },
        'onCancel': function (event, ID, fileObj, data) {
        },
        'onUploadComplete': function (file) {
        },
        'onUploadSuccess': function (file, data, response) {
            $("#" + file.id + " a:first-child").attr("onclick", "javascript:del(" + data + ")");
        }
    });

    $('#file_upload7').uploadify({
        'swf': '/static/js/uploadify.swf',//根据文件存放地址改变
        'uploader': '/admin_uploadify_script/?order_id=' + $("#order_id").val() + "&stlType=6",
        'folder': '/uploadfile',
        'auto': true,//false,//
        'multi': false,//设置可以上传多个文件
        'uploadLimit': 20,
        'buttonText': '选择文件',
        'removeCompleted': false,//
        'fileSizeLimit': '1024MB',//设置上传文件大小单位kb
        'fileTypeExts': '*.stl;',//设置上传文件类型为常用文档格式
        'onSelect': function (e, queueId, fileObj) {
            $('#id_span_msg').html("");
        },
        'onCancel': function (event, ID, fileObj, data) {
        },
        'onUploadComplete': function (file) {
        },
        'onUploadSuccess': function (file, data, response) {
            $("#" + file.id + " a:first-child").attr("onclick", "javascript:del(" + data + ")");
        }
    });
})
