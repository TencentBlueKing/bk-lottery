/* eslint-disable */
$(function () {
  $("#import-rtx-button").click(function () {
    $("#rtxImportModal").modal("show");
  });

  $('input[name="csrfmiddlewaretoken"]').val($.cookie("csrftoken"));

  $("#file-submit").on("click", function () {
    var formData = new FormData();
    formData.append("excel", $("#rtx-file")[0].files[0]);
    $.ajax({
      type: "POST",
      url: site_url + "staff/upload/",
      enctype: "multipart/form-data",
      data: formData,
      processData: false,
      contentType: false,
      dataType: "json",
      success: function (ret) {
        if (ret["result"]) {
          toastr.success(ret["message"]);
        } else {
          toastr.error(ret["message"]);
        }
      },
    });
    toastr.info("文件上传中");
  });

  //    var uploadComponent;
  //
  //    var initializeUpload = function(initFiles) {
  //        uploadComponent = $("#rtx-file").kendoUpload({
  //            async: {
  //                saveUrl: site_url + 'staff/upload/',
  //                removeUrl: site_url + 'staff/remove/',
  //                autoUpload: false,
  //            },
  //            data: {
  //                'csrfmiddlewaretoken': $.cookie('csrftoken'),
  //            },
  //            files: initFiles,
  //            upload: function(e) {
  //                if (e.files.length > 1) {
  //                    toastr.error('不能上传多个文件');
  //                    e.preventDefault();
  //                }
  //                var file = e.files[0];
  //                if (file.extension != '.xls' && file.extension != '.xlsx') {
  //                    toastr.error('请上传.xls格式的excel文件');
  //                    e.preventDefault();
  //                }
  //                return true;
  //            },
  //            remove: function(e) {
  //            },
  //            success: function(e) {
  //                if (e.response.result) {
  //                    toastr.success(e.response.message);
  //                } else {
  //                    toastr.error(e.response.message);
  //                }
  //            },
  //            error: function(e) {
  //                if (e.operation === 'remove') {
  //                    toastr.error(e.XMLHttpRequest.responseText);
  //                }
  //            },
  //        }).data('kendoUpload');
  //    };
  //
  //    var initialFiles = function() {
  //        $.getJSON(site_url + 'staff/staffLists/', function(files) {
  //            initializeUpload(files);
  //        });
  //    };
  //
  //    initialFiles();
});
