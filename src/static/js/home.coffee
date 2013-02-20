# Coffee for home.html
jQuery ->
    counter = null
    ballotsCast = 0

    updateCount = ->
        $.ajax
            url: '/stats/ballot-count'
            type: 'GET'
            success: (data) =>
                response = JSON.parse(data)
                ballotsCast = response['ballots_cast']
                if counter != null
                    counter.incrementTo(ballotsCast)

    updateCount()
    # Initialize a new counter
    counter = new flipCounter 'flip-counter', 
        value:ballotsCast
        inc:1
        pace:500
        auto:true

    setInterval(updateCount, 5000)
    counter.incrementTo(ballotsCast)

