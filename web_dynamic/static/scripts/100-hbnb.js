$(window).on('load', function () {
  const parseHtml = function (data) {
    if (data.length > 0) {
      $('.places').empty();
      let title = '<h1>Places</h1><h4 class="results">' + data.length.toString() + ' results</h4>';
      $('.places').append($(title));
      for (let i = 0; i < data.length; i++) {
        let html = '';
        html += '<article><div class="title_box">';
        html += '<h2>' + data[i].name + '</h2>';
        html += '<div class="price_by_night">$';
        html += data[i].price_by_night + '</div></div>';
        html += '<div class="information">';
        html += '<div class="max_guest">';
        html += data[i].max_guest;
        html += ' Guests</div><div class="number_rooms">';
        html += data[i].number_rooms;
        html += 'Bedroom</div><div class="number_bathrooms">';
        html += data[i].number_bathrooms;
        html += ' Bathroom</div></div><div class="user"><b>Owner:</b> ';
        html += data[i].owner;
        html += '</div><div class="description">';
        html += data[i].description;
        html += '</div></article>';
        const content = $(html);
        $('.places').append(content);
      }
    }
  };
  const  apiStatus = function () {
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
  const requestPlaces = function (filters) {
    const url = 'http://0.0.0.0:5001/api/v1/places_search/';
    $.ajax({
      type: 'POST',
      contentType: 'application/json',
      dataType: 'json',
      data: JSON.stringify(filters),
      crossDomain: true,
      url: url,
      success: function (data) {
        // console.log(data);
        parseHtml(data);
      },
      error: function (e) {
        console.log(e.message);
      }
    });
  };
  const chAm = {};
  const states = {};
  const cities = {};
  $('.amenity > input').change(function () {
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
    // console.log(amenities, chAm);
    $('.amenities > h4').text(amenities.slice(0, -2));
  });
  $('.state-div > input').change(function () {
    if (this.checked) {
      states[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      if ($(this).attr('data-id') in states) {
        delete states[$(this).attr('data-id')];
      }
    }
    let sts = '';
    for (const state in states) {
      sts += states[state];
      sts += ', ';
    }
    for (const city in cities) {
      sts += cities[city];
      sts += ', ';
    }

    $('.locations > h4').text(sts.slice(0, -2));
  });
  $('.city > input').change(function () {
    if (this.checked) {
      const name = $(this).attr('data-name')
      cities[$(this).attr('data-id')] = name;
      console.log(name);
    } else {
      if ($(this).attr('data-id') in states) {
        delete cities[$(this).attr('data-id')];
      }
    }
    let sts = '';
    for (const state in states) {
      sts += states[state];
      sts += ', ';
    }
    for (const city in cities) {
      sts += cities[city];
      sts += ', ';
    }

    $('.locations > h4').text(sts.slice(0, -2));
  });

  $('BUTTON').on('click', function (evnt) {
    console.log('Button clicked');
    // console.log(evnt);
    const amens = Object.keys(chAm);
    const stats = Object.keys(states);
    const citis = Object.keys(cities);
    // console.log(amens);
    requestPlaces({ amenities: amens,
                    states: stats,
                    cities: citis
                    });
  });
  requestPlaces({});
});
