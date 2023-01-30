window.addEventListener('load', function(){

// появление попапа для изменения названия группы продуктов
    $('.js_edit_group').on('click', function(e){
        e.preventDefault()
        var text =$(this).prev().text()
        var id = $(this).attr('data-value')
        $('#popup_edit').val(text)
        $('#popup_edit').attr("data-value", id)
        $('.popup_erorrs').html('')
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
        $('.popup_delete_group').fadeIn()
        $('#name_group').html(text)
        $('#popup__btn_delete_yes').attr('data-value', id)
    });

// скрыть попап для удаление группы продуктов
        $(document).mouseup(function (e) {
            var container = $(".popup_delete_group");
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

})