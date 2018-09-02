# JS for organization-panel.html
jQuery ->
    # Initialize voter lists edit buttons to opening the list for editting
    $('.edit-voter-list').click (event) ->
        toggleListForEditing(event, $(this))

    $('#updateProfile').click (event) ->
        updateOrganizationInformation(event)

    # Would use .change() but that doesn't take effect until user clicks out
    # which causes confusion...
    $('.profile-input').focus (event) ->
        restoreDefaultButtonState(false)

    $('#addAdmin').click (event) ->
        addAdmin(event)

# Open a voter list for editing
toggleListForEditing = (event, link) ->
    listID = link.attr('href')
    editing = link.attr('data-editing')
    link.attr('data-editing', 1 - editing)
    console.log(listID)
    event.preventDefault()
    if editing == '0'
        $(listID+'-paragraph').hide()
        $(listID+'-textarea').show()
        $(listID+'-buttons').show()
    else
        $(listID+'-paragraph').show()
        $(listID+'-textarea').hide()
        $(listID+'-buttons').hide()
    return false

# Tell the backend to update orgnaizational information
updateOrganizationInformation = (event) ->
    event.preventDefault()
    if $('#updateProfile').hasClass('disabled')
        return false
    data =
        'id': $('#organization-id').val()
        'name': $('#organization-name').val()
        'description': $('#organization-description').val(),
        'website' : $('#organization-website').val()
    postData =
        'method': 'update_profile'
        'data': data
    console.log(postData)
    $.ajax
        url: '/admin/organization'
        type: 'POST'
        data: 'data': JSON.stringify(postData)
        success: (data) ->
            successHandler(data)
        error: (data) ->
            errorHandler(data)
    return false

addAdmin = (event) ->

    data =
        'organization_id': $('#admin-orgid').val()
        'net_id': $('#admin-netid').val()

    $.ajax
        url: '/admin/organization'
        type: 'POST'
        data: 'data : JSON.stringify(postData)'
        success: (data) -> successHandler(data)
        error: (data) -> errorHandler(data)
    return false


successHandler = (data) ->
    s = $('#updateProfile')
    s.html('Your profile has been updated!')
    s.addClass('disabled')
    removeStyleClassesFromButton()
    s.addClass('btn-success')

errorHandler = (data) ->
    s = $('#updateProfile')
    s.html('Something went wrong :(')
    s.addClass('disabled')
    removeStyleClassesFromButton()
    s.addClass('btn-error')

restoreDefaultButtonState = (disabled) ->
    s = $('#updateProfile')
    if disabled
        s.addClass('disabled')
    else
        s.removeClass('disabled')
    s.html(s.attr('data-default-text'))
    removeStyleClassesFromButton()
    s.addClass('btn-primary')

removeStyleClassesFromButton = ->
    s = $('#updateProfile')
    s.removeClass('btn-success')
    s.removeClass('btn-error')
    s.removeClass('btn-primary')