window.addEventListener('load', function(){

    // ajax запрос текста заявки для сообщения
    $('#trade__text').on('click', function(e){
        e.preventDefault()
        var id = $(this).attr('data-value')
        $('#text_look').fadeIn()

         $.ajax({
            url:'/trade/ajax_text_vision/',
            method: 'get',
            dataType: 'html',
            data: {id: id},
            success: function(response){

                $('#text_popup').html(response)
                var price_list = $('.trade').find('.popup_full_price')
                $.each(price_list, function(){
                    var price = $(this).text()
                    if(price == '0.00'){
                        $(this).css('color', 'red')
                    }
                })

            }
         });
    });

    $('.trade_popup_wrapper').on('click', function(e){
        $('#text_look, #popup_message, #popup_agent').fadeOut()
    });

    // ajax сообщение клиенту

    $('#trade__message').on('click', function(e){
        e.preventDefault()
        $('#popup_message').fadeIn()
        var id_client = $(this).attr('data-value')
        $.ajax({
            url:'/trade/ajax_text_message/',
            method: 'get',
            dataType: 'html',
            data: {id: id_client},
            success: function(response){

                $('#popup_msg_text').html(response)
            }
         });

    });

    function sleep(milliseconds) {
      const date = Date.now();
      let currentDate = null;
      do {
        currentDate = Date.now();
      } while (currentDate - date < milliseconds);
    }
// цикл запрос с задержкой delay

    var delay = 30000;
    var timerId = setTimeout(function request() {
    var id = $('#trade_id').attr('data-value')
      $.ajax({
          url: "/trade/ajax_compare/",
          method: "get",
          data: { id : id },
          dataType: "json",
          success: function(response){
            if(response.compare == false){
                $('#agree__prices').fadeIn()
                $('.js_text_vision').fadeOut()
                $('#error_compare').fadeIn()

            }else{
                $('#agree__prices').fadeOut()
                $('.js_text_vision').fadeIn()
                $('#error_compare').fadeOut()

            }
          },
          error: function(){
            delay *= 2;
          }
      })
      timerId = setTimeout(request, delay);
    }, delay);

// кнопка логистика popup
    $('#trade__logistic').on('click', function(e){
        e.preventDefault()
        var trade_id = $(this).attr('data-value')
        $('#popup_message').fadeIn()
        $.ajax({
          url: "/trade/ajax_logistic_valid/",
          method: "get",
          data: { id : trade_id },
          dataType: "json",
          success: function(response){
                if(response.tara){
                    var msg = '<p>логистика для таррированного товара пока в разработке<p>'
                    $('#popup_msg_text').html(msg)
                }else if(response.loose){
                    var msg = '<p class="main_title"> логистика id #'+trade_id+'</p><br>'
                    msg += '<div class="logistic_form">'
                    msg += '<p><label for="id_logistic">Цена за тонну груза:</label>'
                    msg += '<input type="number" name="price" value="0" step="0.1" required="" id="id_logistic"></p>'
                    msg += '<button class="form__btn_action btn_center js_logistic" value="'+trade_id+'">добавить в цену</button>'
                    msg += '</div>'
                }else if(response.error_valid_type){
                    var msg = '<p> В сделке присутствуют товары с разным типом погрузки</p>'
                }else if(response.error_auth){
                    var msg = '<p> Пользователь не зарегистрирован !!!</p>'
                }
                $('#popup_msg_text').html(msg)

          }
        })


    });
    // добавление цены логистики , обработка формы
    $('.trade').on('click','.js_logistic', function(e){
        var trade_id = $(this).attr('value')
        var logistic_price = $(this).parent().find('#id_logistic').val()
          $.ajax({
          url: "/trade/ajax_logistic_price/",
          method: "post",
          data: { id : trade_id, logistic_price:logistic_price, csrfmiddlewaretoken: window.CSRF_TOKEN},
          dataType: "json",
          success: function(response){
            if(response.success){
             location.reload()
            }else{
                $('.value_error').html(response.error)
            }

          }
          })

    });

    // агент popup заявка поставщеку получаем поставщиков

    $('#trade__agent, #add_trade_agent').on('click', function(e){
        $('#popup_agent').fadeIn()
        var id_client = $(this).attr('data-value')
        $.ajax({
            url: '/trade/ajax_get_agets/',
            method: 'get',
            data: {id:id_client},
            dataType: "html",
            success: function(response){
                $('html, body').animate({scrollTop: 0}, 300);
                $('#popup_agent_form').html(response)
            }
        })
    })

    $('.container').on('click', '#agent_btn', function(e){
        id_trade = $(this).attr('data-value')
        var agent = $(this).parent().find('#agents').val()
        e.preventDefault()
        $.ajax({
            url: '/trade/ajax_get_agent_form/',
            method: "post",
            dataType: "html",
            data: {id:id_trade, agent: agent, csrfmiddlewaretoken: window.CSRF_TOKEN},
            success: function(response){
                $('#popup_agent_form').html(response)
            }
        })
    })


    $('.container').on('submit', '.trade_agent_form', function(e){
        e.preventDefault()
        var form = $(this).serialize()
        form += '&csrfmiddlewaretoken='+window.CSRF_TOKEN

        $.ajax({
            url: '/trade/ajax_post_agent_form/',
            data: form,
            method: "post",
            dataType: "json",
            success: function(response){
                if(response.error_auth){
                    $('#popup_agent_form').html('<p>пользователь не зарегистрирован</p>')
                }else if(response.data_no_valid){
                    $('#popup_agent_form').html('<p>не допустимая дата(прошлое)</p>')
                }else{
                    location.reload()
                }
            }

        })
    });



});