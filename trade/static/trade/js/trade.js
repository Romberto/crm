window.addEventListener('load', function(){
    $('.js_product_count').on('click', 'a', function(e){
        e.preventDefault()
        $.each($.find('.tr_count'),function(){
            $(this).css('display', 'None')
            $(this).parent().find('a').css('display', 'block')
        })
        var Value = $(this).text() // получаем значение поля
        $(this).css('display', 'None') // скрываем поле a
        $(this).parent().find('input').css('display', 'block')
        $(this).parent().find('input').val(Value)
    })

    $('.tr_count').change(function(){
        var val = $(this).val()
        var id_item = $(this).attr('data-value')
        var Parent = $(this).parent()
        $.each($.find('.tr_count'),function(){
            $(this).css('display', 'None')
            $(this).parent().find('a').css('display', 'block')
        })
        $.ajax({
            url:'/trade/ajax_edit/',
            method: 'post',
            dataType: 'json',
            data: {id: id_item, val: val, csrfmiddlewaretoken: window.CSRF_TOKEN},
            success: function(response){
                if(response.reload){
                       location.reload()

                }else if(response.ValueError){
                   $('.trade_info_block').find('.value_error').text(response.ValueError)
                }
                else{
                Parent.find('a').text(val)
                Parent.next().text(response.total_price_item)
                Parent.next().next().text(response.total_weight_item)
                $('#full_price').html('<b>общая стоимость: </b>'+response.total_price+' руб.')
                $('#full_weight').html('<b>общая масса нетто: </b>'+response.total_weight+' кг.')
                $('.trade_info_block').find('.value_error').text('')
                }
            }

        });

    })




    //запрос на заполнение грузовой специализации

    $('.warning_list').on('click', '.warning_btn', function(e){
        e.preventDefault()
        var Id_product = $(this).attr('data-value')
        console.log(Id_product)
        alert('запросы в разработке')
    })

    $('#agree__prices').on('click', function(e){
        e.preventDefault()
        var Id_trade = $(this).attr('data-value')
        console.log(Id_trade)
        alert('запросы в разработке')

    })



});