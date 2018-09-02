/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
// JS for organization-panel.html
jQuery(function() {
    // Initialize voter lists edit buttons to opening the list for editting
    $('.edit-voter-list').click(function(event) {
        return toggleListForEditing(event, $(this));
    });

    $('#updateProfile').click(event => updateOrganizationInformation(event));

    // Would use .change() but that doesn't take effect until user clicks out
    // which causes confusion...
    $('.profile-input').focus(event => restoreDefaultButtonState(false));

    return $('#addAdmin').click(event => addAdmin(event));
});

// Open a voter list for editing
var toggleListForEditing = function(event, link) {
    const listID = link.attr('href');
    const editing = link.attr('data-editing');
    link.attr('data-editing', 1 - editing);
    console.log(listID);
    event.preventDefault();
    if (editing === '0') {
        $(listID+'-paragraph').hide();
        $(listID+'-textarea').show();
        $(listID+'-buttons').show();
    } else {
        $(listID+'-paragraph').show();
        $(listID+'-textarea').hide();
        $(listID+'-buttons').hide();
    }
    return false;
};

// Tell the backend to update orgnaizational information
var updateOrganizationInformation = function(event) {
    event.preventDefault();
    if ($('#updateProfile').hasClass('disabled')) {
        return false;
    }
    const data = {
        'id': $('#organization-id').val(),
        'name': $('#organization-name').val(),
        'description': $('#organization-description').val(),
        'website' : $('#organization-website').val()
    };
    const postData = {
        'method': 'update_profile',
        'data': data
    };
    console.log(postData);
    $.ajax({
        url: '/admin/organization',
        type: 'POST',
        data: { 'data': JSON.stringify(postData)
    },
        success(data) {
            return successHandler(data);
        },
        error(data) {
            return errorHandler(data);
        }
    });
    return false;
};

var addAdmin = function(event) {

    const data = {
        'organization_id': $('#organization-id').val(),
        'net_id': $('#admin-netid').val()
    };

    $.ajax({
        url: '/admin/organization',
        type: 'POST',
        data: 'data : JSON.stringify(postData)',
        success(data) { return successHandler(data); },
        error(data) { return errorHandler(data); }
    });
    return false;
};


var successHandler = function(data) {
    const s = $('#updateProfile');
    s.html('Your profile has been updated!');
    s.addClass('disabled');
    removeStyleClassesFromButton();
    return s.addClass('btn-success');
};

var errorHandler = function(data) {
    const s = $('#updateProfile');
    s.html('Something went wrong :(');
    s.addClass('disabled');
    removeStyleClassesFromButton();
    return s.addClass('btn-error');
};

var restoreDefaultButtonState = function(disabled) {
    const s = $('#updateProfile');
    if (disabled) {
        s.addClass('disabled');
    } else {
        s.removeClass('disabled');
    }
    s.html(s.attr('data-default-text'));
    removeStyleClassesFromButton();
    return s.addClass('btn-primary');
};

var removeStyleClassesFromButton = function() {
    const s = $('#updateProfile');
    s.removeClass('btn-success');
    s.removeClass('btn-error');
    return s.removeClass('btn-primary');
};