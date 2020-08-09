$(window).on('load', function () {
  const apiStatus = function () {
    const url = 'http://0.0.0.0:5001/api/v1/status/';
    $.ajax({
      type: 'GET',
      url: url,
      success: function (data) {
        if ('status' in data) {
          console.log(data.status);
          $('#api_status').addClass('available');
        } else {
          console.log(data.error);
          $('#api_status').removeClass('available');
        }
      }
    });
  };
  apiStatus();
  const chAm = {};
  $('input').change(function () {
    if (this.checked) {
      console.log('Checked');
      chAm[$(this).attr('data-id')] = $(this).attr('data-name');
      // console.log(chAm);
    } else {
      if ($(this).attr('data-id') in chAm) {
        delete chAm[$(this).attr('data-id')];
      }
    }
    let amenities = '';
    for (const id in chAm) {
      amenities += chAm[id];
      amenities += ', ';
    }
    $('.amenities > h4').text(amenities.slice(0, -2));
  });
});
