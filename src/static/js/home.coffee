# Coffee for home.html
jQuery ->
    counter = null
    votesCount = 0

    updateCount = ->
        $.ajax
            url: '/stats/votes-count'
            type: 'GET'
            success: (data) =>
                response = JSON.parse(data)
                votesCount = response['votes_count']
                if counter != null
                    counter.incrementTo(votesCount)

    updateCount()
    # Initialize a new counter
    counter = new flipCounter 'flip-counter', 
        value:votesCount
        inc:1
        pace:1
        auto:true

    setInterval(updateCount, 10000)
    counter.incrementTo(votesCount)

