# JS for election-panel.html
updatePanel = ->
	console.log($('#election-panel li[class=active]').text())


jQuery ->
	updatePanel()