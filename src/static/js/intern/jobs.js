$(function () {

  $('#run-job').click(function (e) {
    var data = {
      ready_name: $('#ready-name').val(),
      ready_description: $('#ready-description').text()
    };
    console.log(data);
    $.ajax({
      url: "/intern/jobs",
      type: "POST",
      data: data,
      success: function (data, textStatus, jqXHR) {
        var job = JSON.parse(data);
        var row = $('<tr>');
        var properties = ['name', 'description', 'started', 'ended'];
        for (var i in properties) {
          $(row).append($('<td>').text(job[properties[i]]));
        }
        var jobClass = "label label-default";
        if (job.status == "complete") {
          jobClass = "label label-success";
        } else if (job.status == "failed") {
          jobClass = "label label-important";
        }
        var status = $('<span>', {class: jobClass}).text(job.status);
        $(row).append($('<td>').append(status));
        $(row).hide();
        $('#jobs-list').prepend($(row))
        $(row).fadeIn(2000);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $('#run-job').attr('class', 'btn btn-danger');
        $('#run-job').text(errorThrown);
      }
    });
  });

});