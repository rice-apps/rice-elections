# JS for election-panel.html
updatePanel = ->
	console.log($('#election-panel li[class=active]').text())
	postData =
		'method': 'information'
		'id': $('#election-panel').attr('data-election-id')
	$.ajax
		url: '/election-panel'
		type: 'POST'
		data: 'data': JSON.stringify(postData)
		success: (data) ->
			console.log('Success!')
			console.log(data)
			$('#election-information').append(data)

jQuery ->
	updatePanel()