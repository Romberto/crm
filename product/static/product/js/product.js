window.addEventListener('load', function(){

// появление попапа для изменения названия группы продуктов
    $('.js_edit_group').on('click', function(e){
        e.preventDefault()
        var text =$(this).prev().text()
        var id = $(this).attr('data-value')
        $('#popup_edit').val(text)
        $('#popup_edit').attr("data-value", id)
        $('.popup_erorrs').html('')
        $('html, body').animate({scrollTop: 0}, 600);
        $('.popup_edit_group').fadeIn()
    });
// скрыть попап для изменения названия группы продуктов
        $(document).mouseup(function (e) {
        var container = $(".popup_edit_group");
        if (container.has(e.target).length === 0){
            container.fadeOut();
        }
    });
// ajax изменить название группы товаров

    $('.product').on('click', '#popup__btn', function(e){
        e.preventDefault()
        var new_name = $('#popup_edit').val()
        var id_group = $('#popup_edit').attr('data-value')
            $.ajax({
            url: '/product/product_group_edit/',            /* Куда пойдет запрос */
            method: 'get',                  /* Метод передачи (post или get) */
            dataType: 'json',               /* Тип данных в ответе (xml, json, script, html). */
            data: {id: id_group, val: new_name},            /* Параметры передаваемые в запросе. */
            success: function(response){    /* функция которая будет выполнена после успешного запроса.  */
                if(response.error){
                    $('.popup_erorrs').html(response.msg)
                }else{
                    location.reload()
                }
            }
        })
    });
// появление попапа удаление пруппы товаров

    $('.js_delete_group').on('click', function(e){
        e.preventDefault()
        alert('Внимание удалив группу , вы удалите все продукты входящие в эту группу.')
        var id = $(this).attr('data-value')
        var text = $('#droup_'+id).text()
        $('html, body').animate({scrollTop: 0}, 600);
        $('.popup_delete_group').fadeIn()
        $('#name_group').html(text)
        $('#popup__btn_delete_yes').attr('data-value', id)
    });

// скрыть попап для удаление группы продуктов
        $(document).mouseup(function (e) {
            var container = $(".popup_delete_group, .popup_delete_product, .popup_packing_edit");
            if (container.has(e.target).length === 0){
                container.fadeOut();
            }
        });

        $('#popup__btn_delete_no').on('click', function(e){
            $('.popup_delete_group').fadeOut()
        });

        $('.product').on('click', '#popup__btn_delete_yes', function(e){
            e.preventDefault()
            var id = $(this).attr('data-value')
            $.ajax({
            url: '/product/product_group_delete/',            /* Куда пойдет запрос */
            method: 'get',                  /* Метод передачи (post или get) */
            dataType: 'json',               /* Тип данных в ответе (xml, json, script, html). */
            data: {id: id},            /* Параметры передаваемые в запросе. */
            success: function(response){
                if(response.error){
                    $('.popup_erorrs').html(response.msg)
                }else{
                    location.reload()
                }
            }

            })
        })

        // попап удаление продукта

        $('.js_delete_product').on('click', function(e){
            e.preventDefault()
            alert('Внимание удаление товара и все документы связанные с ним !')
            var id = $(this).attr('data-value')
            $('#popup__btn_product_delete_yes').attr('data-value', id)
            var article = $('#product_'+id).text()
            $('#name_group').text(article)
            $('html, body').animate({scrollTop: 0}, 600);
            $('.popup_delete_product').fadeIn()
        });

        $('#popup__btn_product_delete_no').on('click', function(e){
            e.preventDefault()
            $('.popup_delete_product').fadeOut()

        })

        $('#popup__btn_product_delete_yes').on('click', function(e){
            e.preventDefault()
            var id_product = $('#popup__btn_product_delete_yes').attr('data-value')
            $.ajax({
                url: '/product/product_delete/',            /* Куда пойдет запрос */
                method: 'get',                  /* Метод передачи (post или get) */
                dataType: 'json',               /* Тип данных в ответе (xml, json, script, html). */
                data: {id: id_product},            /* Параметры передаваемые в запросе. */
                success: function(response){
                    if(response.error){
                        $('.popup_erorrs').html(response.msg)
                    }else{
                        location.reload()
                    }
                }
            })
        });
// попап появляется для просмотра спецификации продукта

    $('.js_packing_edit').on('click', function(e){
        e.preventDefault()
        var id_packing = $(this).attr('data-value')
        $('html, body').animate({scrollTop: 0}, 600);
        $('.popup_packing_edit').fadeIn()
        $.ajax({
            url: '/product/packing/',
            method: 'get',
            dataType: "html",
            data: {id: id_packing},
            success: function(response){

                $('.popup_packing_edit').html(response)
            }

        });
    });

    // попап появляется для изменения спецификации продукта
    $('.product').on('click','#packing_edit', function(e){
        e.preventDefault()
        var id_packing = $(this).attr('data-value')
        $.ajax({
            url: '/product/packing_edit/',
            method: 'get',
            dataType: "html",
            data: {id: id_packing},
            success: function(response){
                $('.popup_packing_edit').html(response)
            }
        });
    })

    $('.product').on('click','#packing_edit_post', function(e){
        e.preventDefault()
        var id_packing = $(this).attr('data-value')
        var packing_name = $(this).parent().find('#id_packing_name').val()
        var netto = $(this).parent().find('#id_netto').val()
        var brutto = $(this).parent().find('#id_brutto').val()
        var quantity_box = $(this).parent().find('#id_quantity_box').val()
            $.ajax({
            url: '/product/packing_edit_post/',
            method: 'get',
            dataType: "json",
            data: {id: id_packing, packing_name:packing_name, netto:netto, brutto:brutto, quantity_box:quantity_box},
            success: function(response){
                    if(response.error){
                        $('.popup_erorrs').html(response.msg)
                    }else{
                        location.reload()
                    }
            }
        });
        });
// подбор фона для группы товаров исходя из начала названия
    var container = $('.product__group_link')
    container.each(function(){
        var text = $(this).text()
        if(text.startsWith('СОЛ-ПРО')){
            $(this).addClass('blue_light')
        }else if(text.startsWith('РУС-АГРО')){
            $(this).addClass('orange_light')
        }
    })



})