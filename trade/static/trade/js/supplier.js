window.addEventListener('load', function(){
    // изменить цену в заявке поставщика
    $('.js_supplier_price, .js_supplier_count, .js_supplier_date').on('click', function(e){
        e.preventDefault()
        $.each($.find('.supplier_price'),function(){
            $(this).css('display', 'None')
            $(this).parent().find('a').css('display', 'block')
        })
        $.each($.find('.supplier_count'),function(){
            $(this).css('display', 'None')
            $(this).parent().find('a').css('display', 'block')
        })
        $.each($.find('.supplier_date'),function(){
            $(this).css('display', 'None')
            $(this).parent().find('a').css('display', 'block')
        })

        var text = $(this).text()

        $(this).css('display', 'none')
        $(this).parent().find('input').css('display', 'block')
        $(this).parent().children('input').val(parseInt(text))
        });
    // ajax запрос изменение цены в заявке поставщика
    $('.supplier_price').change(function(e){
        var id_item = $(this).attr('data-value')
        var price = $(this).val()
        var trow = $(this).parent().parent()
        if($(this).val() >= 0){
        $('.supplier_error').html('')
        $.ajax({
            url: '/trade/ajax_supplier_price/',
            method: 'post',
            dataType: 'json',
            data:{id:id_item, price:price,  csrfmiddlewaretoken: window.CSRF_TOKEN},
            success: function(response){
                if(response.no_auth){
                    $('#supplier').html('<p>пользователь не зарегистрирован</p>').css('color', 'red')
                }else {
                    trow.find('.supplier_full_price').text(response.item_full_price)
                    $('#supplier_full_price span' ).text(response.full_price)
                    trow.find('.js_supplier_price').text(price)
                }
            }
        })}else{
             $('.supplier_error').html('<p>Ошибка значение меньше нуля</p>').css('color', 'red')
             trow.find('.js_supplier_price').css('display', 'block')
             $(this).css('display', 'none')
        }
    })

    // изменить количество в заявке поставщика
    $('.supplier_count').change(function(e){
        var id_item = $(this).attr('data-value')
        var count = $(this).val()
        var trow = $(this).parent().parent()
        if($(this).val() >= 0){
            $('.supplier_error').html('')
            $.ajax({
                url: '/trade/ajax_supplier_count/',
                method: 'post',
                dataType: 'json',
                data: {id: id_item, count: count, csrfmiddlewaretoken: window.CSRF_TOKEN},
                success: function(response){
                if(response.no_auth){
                    $('.supplier_error').html('<p>пользователь не зарегистрирован</p>').css('color', 'red')

                }else if(response.remove){
                    location.reload()
                }else{
                    trow.find('.js_supplier_count').text(count)
                    trow.find('.supplier_full_price').text(response.item_full_price)
                    trow.find('.supplier_full_weight').text(response.item_fill_weight)
                    $('#supplier_full_price span' ).text(response.full_price)
                    $('#supplier_full_weight span' ).text(response.full_weight)
                    }
                }
            })

        }else{
            $('.supplier_error').html('<p>Ошибка значение меньше нуля</p>').css('color', 'red')
            trow.find('.js_supplier_count').css('display', 'block')
            $(this).css('display', 'none')
        }
    })

    // изменить дату поставки

    $('.supplier_date').change(function(e){
        var id_item = $(this).attr('data-value')
        var date = $(this).val()
        var trow = $(this).parent().parent()
        if(Date.parse(date)-Date.parse(new Date()) < 0){
            $('.supplier_error').html('<p>Ошибка недопустимая дата</p>').css('color', 'red')
            trow.find('.js_supplier_date').css('display', 'block')
            $(this).css('display', 'none')
        }else{
            $('.supplier_error').html('')
            $.ajax({
                url: '/trade/ajax_supplier_date/',
                method: 'post',
                dataType: 'json',
                data: {id: id_item, date:date , csrfmiddlewaretoken: window.CSRF_TOKEN},
                success: function(response){
                    if(response.no_auth){
                        $('.supplier_error').html('<p>пользователь не зарегистрирован</p>').css('color', 'red')
                        trow.find('.js_supplier_date').css('display', 'block')
                        $(this).css('display', 'none')
                    }else{
                        trow.find('.js_supplier_date').text(response.date_delivery)

                    }
                }
            })
        }

    })





});