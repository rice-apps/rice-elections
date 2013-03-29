# Coffee for home.html
jQuery ->
    counter = null
    firstTime = true
    votesCount = 0

    updateCount = ->
        $.ajax
            url: '/stats/votes-count'
            type: 'GET'
            success: (data) =>
                response = JSON.parse(data)
                votesCount = response['votes_count']
                if counter != null
                    if firstTime
                        counter.add(Math.floor(votesCount/100)*100)
                        firstTime = false
                    counter.incrementTo(votesCount)

    updateCount()
    # Initialize a new counter
    counter = new flipCounter 'flip-counter',
        value:0
        inc:1
        pace:100
        auto:true

    setInterval(updateCount, 10000)
    counter.incrementTo(votesCount)
