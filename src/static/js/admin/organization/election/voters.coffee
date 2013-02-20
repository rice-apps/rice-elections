# Coffee for voters.html
jQuery ->
    class PageModel
        updateVoterList: (list) =>
            console.log(list)
            votersList = $("#voters-list")
            votersList.hide()
            votersList.children().remove()
            for voter in list
                votersList.append($("<li>#{voter}</li>"))
            votersList.fadeIn(1000)

    class ListModal
        constructor: (@type) ->
            # Position type
            @type = type

            # List Input
            @input = $("#net-ids-#{@type}")
            @inputContainer = @input.parent().parent()

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
                        $("#modal-#{@type}").modal('hide')
                        @reset()
                        pageModel.updateVoterList(response['voters'])
                    else if response['status'] == 'ERROR'
                        msg = response['msg']
                        console.log("ERROR: #{msg}")

        reset: =>
            @input.val('')
            @removeListError()

        getList: =>
            inputContainer = @input.parent().parent()
            list = []
            inputText = @input.val()
            commas = true if inputText.indexOf(',') > -1
            lines = true if inputText.indexOf('\n') > -1
            if commas and lines
                @setListError('Both commas and new lines were found in the ' +
                    'input. Please use only one of the two to seperate items.')
                return

            if not commas and not lines
                delimiter = ' '
            else if commas
                delimiter = ','
            else if lines
                delimiter = '\n'
            else
                delimiter = ' '

            for netId in @input.val().split(delimiter)
                if netId.trim()
                    list.push(netId.trim())
            
            if list.length == 0
                @setListError('Missing information.')
                return null
            else
                @removeListError()
                return list

        setListError: (msg) =>
            @inputContainer.addClass('error')
            error = $("<span class='help-inline'>#{msg}</span>")
            error.insertAfter(@input)

        removeListError: =>
            @inputContainer.removeClass('error')
            @inputContainer.children().children().filter('.help-inline').remove()

    addModal = new ListModal('add')
    deleteModal = new ListModal('delete')
    pageModel = new PageModel()