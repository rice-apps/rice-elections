# Coffee for voters.html

jQuery ->
    addModal = new ListModal('add')
    deleteModal = new ListModal('delete')
    page = new Page()

class Page
    updateVoterList: (list) =>
        console.log(list)

class ListModal
    constructor: (@type) ->
        # Position type
        @type = type

        # List Input
        @input = $("#net-ids-#{@type}")

        $("#voters-#{@type}-submit").click(@submit)

    submit: (e) =>
        list = @getList()
        if list == null
            return

        data =
            'method': "#{@type}_voters"
            'voters': list
        $.ajax
            url: '/admin/organization/election/voters'
            type: 'POST'
            data:
                'data': JSON.stringify(data)
            success: (data) =>
                response = JSON.parse(data)
                if response['status'] == 'OK'
                    $("modal-#{@type}").modal('hide')
                    console.log('Success!')
                    @reset()
                else if response['status'] == 'ERROR'
                    console.log("ERROR: #{response['msg']}")

    reset: =>
        @input.val('')
        inputContainer = @input.parent().parent()
        inputContainer.removeClass('error')
        inputContainer.children().children().filter('.help-inline').remove()

    getList: =>
        inputContainer = @input.parent().parent()
        list = []
        for netId in @input.val().split(',')
            if netId.trim()
                list.push(netId.trim())
        
        if list.length == 0
            inputContainer.addClass('error')
            error = $("<span class='help-inline'>Missing information.</span>")
            error.insertAfter(@input)
            return null
        else
            inputContainer.removeClass('error')
            inputContainer.children().children().filter('.help-inline').remove()
            return list