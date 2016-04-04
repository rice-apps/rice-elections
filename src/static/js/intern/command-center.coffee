postURL = '/intern/command-center'
jQuery ->
    for field in ['name', 'description', 'website']
        $('#organization-'+field).change ->
            $('#organization-create').removeClass('disabled')

    $('#organization-create').click (e) ->
        return if $('#organization-create').hasClass('disabled')
        name = $('#organization-name').val().trim()
        description = $('#organization-description').val().trim()
        website = $('#organization-website').val().trim()

        for val in [name, description, website]
            if not val
                $('#organization-create').removeClass('btn-primary')
                $('#organization-create').addClass('btn-danger')
                $('#organization-create').text('Missing information')
                $('#organization-create').addClass('disabled')
                return

        data =
            name: name
            description: description
            website: website
            method: 'create_organization'

        $.ajax
            url: postURL
            type: 'POST'
            data: 'data': JSON.stringify(data)
            success: (data) =>
                response = JSON.parse(data)
                if response.status == 'OK'
                    $('#organization-create').removeClass('btn-danger')
                    $('#organization-create').addClass('btn-success')
                    $('#organization-create').text('Created')
                    $('#organization-create').addClass('disabled')
                    
    $('#admin-add').click (e) ->
        return if $('#admin-add').hasClass('disabled')
        net_id = $('#admin-netid').val().trim()
        organization = $('#admin-organization').val().trim()
        
        for val in [net_id, organization]
            if not val
                $('#admin-add').removeClass('btn-primary')
                $('#admin-add').addClass('btn-danger')
                $('#admin-add').text('Missing information')
                $('#admin-add').addClass('disabled')
                return
                
        data = 
            net_id: net_id
            organization: organization
            method: 'add_admin'
            
        $.ajax
            url: postURL
            type: 'POST'
            data: 'data': JSON.stringify(data)
            success: (data) =>
                response = JSON.parse(data)
                if response.status == 'OK'
                    $('#admin-add').removeClass('btn-danger')
                    $('#admin-add').addClass('btn-success')
                    $('#admin-add').text('Created')
                    $('#admin-add').addClass('disabled')
                

        