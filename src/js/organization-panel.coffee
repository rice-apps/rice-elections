# JS for organization-panel.html
jQuery ->
	$('#updateProfile').click (event) ->
		updateOrganizationInformation(event)

# Tell the backend to update orgnaizational information
updateOrganizationInformation = (event) ->
	event.preventDefault()
	postData =
		'id': $('#organization-id').val()
		'name': $('#organization-name').val()
		'description': $('#organization-description').val(),
		'website' : $('#organization-website').val()
	console.log(postData)
	$.ajax
		url: '/organization-panel'
		type: 'POST'
		data: 'data': JSON.stringify(postData)
		success: (data) ->
			console.log('Success!')
			console.log(data)
			$('#election-information').append(data)
		error: (data) ->
			console.log('Error...')
			console.log(data)