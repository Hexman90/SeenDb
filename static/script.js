$(document).on('click', '.addtolist', function() {
    var list_id = $(this).attr('id');
    var data = {
      'id': movie_data["id"],
      'title': movie_data["title"],
      'year': movie_data["year"],
      'genres': movie_data["genres"],
      'imDbRating': movie_data["imDbRating"],
      'plot': movie_data["plot"],
      'stars': movie_data["stars"],
      'linkEmbed': movie_data['trailer']['linkEmbed'],
      'image': movie_data["image"],
      'list_id': list_id
    };
    $.ajax({
      url: '/addtolist',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(data),
      success: function(response) {
        $('#' + list_id).prop('disabled', true);
  
        // Add the 'disabled' class to the button
        $('#' + list_id).addClass('disabled');
      },
      error: function(xhr) {
      }
    });

  });

  $(document).on('click', '.removefromlist', function() {
    var movie_id = $(this).attr('id');
    var name = document.getElementById('list_name');
    var list_name = name.textContent;
    var data = {
      'list_name': list_name,
      'movie_id': movie_id
    };
    $.ajax({
      url: '/removefromlist',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(data),
      success: function(response) {
        location.reload();
      },
      error: function(xhr) {
        // handle error response
      }
    });
  });
