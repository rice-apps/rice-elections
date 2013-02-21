(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  jQuery(function() {
    var ListModal, PageModel, addModal, deleteModal, pageModel;
    PageModel = (function() {

      function PageModel() {
        this.updateVoterList = __bind(this.updateVoterList, this);
      }

      PageModel.prototype.updateVoterList = function(list) {
        var voter, votersList, _i, _len;
        console.log(list);
        votersList = $("#voters-list");
        votersList.hide();
        votersList.children().remove();
        for (_i = 0, _len = list.length; _i < _len; _i++) {
          voter = list[_i];
          votersList.append($("<li>" + voter + "</li>"));
        }
        return votersList.fadeIn(1000);
      };

      return PageModel;

    })();
    ListModal = (function() {

      function ListModal(type) {
        this.type = type;
        this.removeListError = __bind(this.removeListError, this);
        this.setListError = __bind(this.setListError, this);
        this.getList = __bind(this.getList, this);
        this.reset = __bind(this.reset, this);
        this.submit = __bind(this.submit, this);
        this.type = type;
        this.input = $("#net-ids-" + this.type);
        this.inputContainer = this.input.parent().parent();
        $("#voters-" + this.type + "-submit").click(this.submit);
      }

      ListModal.prototype.submit = function(e) {
        var data, list,
          _this = this;
        list = this.getList();
        if (list === null) return;
        data = {
          'method': "" + this.type + "_voters",
          'voters': list
        };
        return $.ajax({
          url: '/admin/organization/election/voters',
          type: 'POST',
          data: {
            'data': JSON.stringify(data)
          },
          success: function(data) {
            var msg, response;
            response = JSON.parse(data);
            if (response['status'] === 'OK') {
              $("#modal-" + _this.type).modal('hide');
              _this.reset();
              return pageModel.updateVoterList(response['voters']);
            } else if (response['status'] === 'ERROR') {
              msg = response['msg'];
              return console.log("ERROR: " + msg);
            }
          }
        });
      };

      ListModal.prototype.reset = function() {
        this.input.val('');
        return this.removeListError();
      };

      ListModal.prototype.getList = function() {
        var commas, delimiter, inputContainer, inputText, lines, list, netId, _i, _len, _ref;
        inputContainer = this.input.parent().parent();
        list = [];
        inputText = this.input.val();
        if (inputText.indexOf(',') > -1) commas = true;
        if (inputText.indexOf('\n') > -1) lines = true;
        if (commas && lines) {
          this.setListError('Both commas and new lines were found in the ' + 'input. Please use only one of the two to seperate items.');
          return;
        }
        if (!commas && !lines) {
          delimiter = ' ';
        } else if (commas) {
          delimiter = ',';
        } else if (lines) {
          delimiter = '\n';
        } else {
          delimiter = ' ';
        }
        _ref = this.input.val().split(delimiter);
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          netId = _ref[_i];
          if (netId.trim()) list.push(netId.trim());
        }
        if (list.length === 0) {
          this.setListError('Missing information.');
          return null;
        } else {
          this.removeListError();
          return list;
        }
      };

      ListModal.prototype.setListError = function(msg) {
        var error;
        this.inputContainer.addClass('error');
        error = $("<span class='help-inline'>" + msg + "</span>");
        return error.insertAfter(this.input);
      };

      ListModal.prototype.removeListError = function() {
        this.inputContainer.removeClass('error');
        return this.inputContainer.children().children().filter('.help-inline').remove();
      };

      return ListModal;

    })();
    addModal = new ListModal('add');
    deleteModal = new ListModal('delete');
    return pageModel = new PageModel();
  });

}).call(this);
