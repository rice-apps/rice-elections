# JS for organization-panel.html
jQuery ->
	$('#updateProfile').click (event) ->
		updateOrganizationInformation(event)

# Tell the backend to update orgnaizational information
updateOrganizationInformation = (event) ->
	event.preventDefault()
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
		url: '/admin/organization-panel'
		type: 'POST'
		data: 'data': JSON.stringify(postData)
		success: (data) ->
			successHandler(data)
		error: (data) ->
			errorHandler(data)

successHandler = (data) ->
	s = $('#server-response')
	s.append('Succesfully updated your ogranization profile')
	s.addClass('alert')
	s.addClass('alert-success')
	s.show()

errorHandler = (data) ->
	s = $('#server-response')
	s.append('Sorry, there was a server error.')
	s.addClass('alert')
	s.addClass('alert-error')
	s.show()
