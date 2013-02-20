// Generated by CoffeeScript 1.4.0

jQuery(function() {
  var ballotsCast, counter, updateCount;
  counter = null;
  ballotsCast = 0;
  updateCount = function() {
    var _this = this;
    return $.ajax({
      url: '/stats/ballot-count',
      type: 'GET',
      success: function(data) {
        var response;
        response = JSON.parse(data);
        ballotsCast = response['ballots_cast'];
        if (counter !== null) {
          return counter.incrementTo(ballotsCast);
        }
      }
    });
  };
  updateCount();
  counter = new flipCounter('flip-counter', {
    value: ballotsCast,
    inc: 1,
    pace: 500,
    auto: true
  });
  setInterval(updateCount, 5000);
  return counter.incrementTo(ballotsCast);
});