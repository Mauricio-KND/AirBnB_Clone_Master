$(window).on('load', function () {
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
