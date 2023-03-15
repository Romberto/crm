window.addEventListener('load', function(){
        function play() {
            var audio = document.getElementById("audio_stamp");
            audio.play();
      }
      var id = $('#trade_id').attr('data-value')
      $.ajax({
            url:'/work/ajax_stamp/',
            method: 'get',
            dataType: 'json',
            data: {id: id},
            success: function(response){
                if(response.compare == false){
                    $('.shtamp').css('display', 'None')
                }
            }
      })

      $('#compare_btn').on('click', function(){
        play()
        $('.shtamp').css('display', 'block')
        var id = $('#trade_id').attr('data-value')
              $.ajax({
            url:'/work/ajax_agreement/',
            method: 'post',
            dataType: 'json',
            data: {id: id, csrfmiddlewaretoken: window.CSRF_TOKEN},
            success: function(response){
                $('#compare_btn').css('display', 'None')
            }
      })

      })
});