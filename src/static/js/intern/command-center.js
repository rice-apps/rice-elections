var postURL;

postURL = '/intern/command-center';

jQuery(function() {
  var field, _i, _len, _ref;
  _ref = ['name', 'description', 'website'];
  for (_i = 0, _len = _ref.length; _i < _len; _i++) {
    field = _ref[_i];
    $('#organization-' + field).change(function() {
      return $('#organization-create').removeClass('disabled');
    });
  }
  return $('#organization-create').click(function(e) {
    var data, description, name, val, website, _j, _len1, _ref1,
      _this = this;
    if ($('#organization-create').hasClass('disabled')) {
      return;
    }
    name = $('#organization-name').val().trim();
    description = $('#organization-description').val().trim();
    website = $('#organization-website').val().trim();
    _ref1 = [name, description, website];
    for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
      val = _ref1[_j];
      if (!val) {
        $('#organization-create').removeClass('btn-primary');
        $('#organization-create').addClass('btn-danger');
        $('#organization-create').text('Missing information');
        $('#organization-create').addClass('disabled');
        return;
      }
    }
    data = {
      name: name,
      description: description,
      website: website,
      method: 'create_organization'
    };
    return $.ajax({
      url: postURL,
      type: 'POST',
      data: {
        'data': JSON.stringify(data)
      },
      success: function(data) {
        var response;
        response = JSON.parse(data);
        if (response.status === 'OK') {
          $('#organization-create').removeClass('btn-danger');
          $('#organization-create').addClass('btn-success');
          $('#organization-create').text('Created');
          return $('#organization-create').addClass('disabled');
        }
      }
    });
  });
});
