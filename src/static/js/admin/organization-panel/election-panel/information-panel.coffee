# Coffee for information.html

jQuery ->
	# Initialize date / time pickers
    $('#startDate, #endDate').parent().datepicker()
    $('#startTime, #endTime').timepicker
        minuteStep: 5
    
    # Initialize tooltips
    $('label[rel="tooltip"]').tooltip()
    
    # Form validation
    $('#election-submit').click(submitForm)

    