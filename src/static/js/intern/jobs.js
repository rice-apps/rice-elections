$(function () {

  $('#run-job').click(function (e) {
    var data = {
      ready_name: $('#ready-name').text(),
      ready_description: $('#ready-description').text()
    };
    console.log(data);
    $.ajax({
      url: "/intern/jobs",
      type: "POST",
      data: data,
      success: function (data, textStatus, jqXHR) {
        
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $('#run-job').attr('class', 'btn btn-danger');
        $('#run-job').text(errorThrown);
      }
    });
  });

});