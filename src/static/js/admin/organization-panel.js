(function() {
  var errorHandler, removeStyleClassesFromButton, restoreDefaultButtonState, successHandler, updateOrganizationInformation;

  jQuery(function() {
    $('#updateProfile').click(function(event) {
      return updateOrganizationInformation(event);
    });
    return $('.profile-input').focus(function(event) {
      return restoreDefaultButtonState(false);
    });
  });

  updateOrganizationInformation = function(event) {
    var data, postData;
    event.preventDefault();
    if ($('#updateProfile').hasClass('disabled')) return false;
    data = {
      'id': $('#organization-id').val(),
      'name': $('#organization-name').val(),
      'description': $('#organization-description').val(),
      'website': $('#organization-website').val()
    };
    postData = {
      'method': 'update_profile',
      'data': data
    };
    console.log(postData);
    $.ajax({
      url: '/admin/organization-panel',
      type: 'POST',
      data: {
        'data': JSON.stringify(postData)
      },
      success: function(data) {
        return successHandler(data);
      },
      error: function(data) {
        return errorHandler(data);
      }
    });
    return false;
  };

  successHandler = function(data) {
    var s;
    s = $('#updateProfile');
    s.html('Your profile has been updated!');
    s.addClass('disabled');
    removeStyleClassesFromButton();
    return s.addClass('btn-success');
  };

  errorHandler = function(data) {
    var s;
    s = $('#updateProfile');
    s.html('Something went wrong :(');
    s.addClass('disabled');
    removeStyleClassesFromButton();
    return s.addClass('btn-error');
  };

  restoreDefaultButtonState = function(disabled) {
    var s;
    s = $('#updateProfile');
    if (disabled) {
      s.addClass('disabled');
    } else {
      s.removeClass('disabled');
    }
    s.html(s.attr('data-default-text'));
    removeStyleClassesFromButton();
    return s.addClass('btn-primary');
  };

  removeStyleClassesFromButton = function() {
    var s;
    s = $('#updateProfile');
    s.removeClass('btn-success');
    s.removeClass('btn-error');
    return s.removeClass('btn-primary');
  };

}).call(this);
