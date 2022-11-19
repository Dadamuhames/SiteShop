$(document).ready(function() {
    const countTotal = () => {
        let pricesBlock = $('p.price-nbm')
        let total = 0;
        for (let i = 0; i < pricesBlock.length; i++) {

            total += Number($('.count_input')[i].value) * parseFloat(pricesBlock[i].innerHTML.substring(1))

        }
        return total
    }
    let form = $('.delete-form')
    form.on('submit', function(e) {
        e.preventDefault()
        let url = $(e.target).attr('action')
            
            data = {}
            let csrf = form.find('input[name="csrfmiddlewaretoken"]').val()
            data['csrfmiddlewaretoken'] = csrf
            $.ajax({
                url: url,
                type: "POST",
                data: data,
                cashe: true,
                success: function () {
                    deleted(e.target, form)
                },
                error: function () {
                    console.log('error')
                }
            })
    })

    $(".del-btn").on('click', (e) => {
        e.preventDefault()
        let url = $('.del-btn').attr('data-delurl')
        $.ajax({
            url: url,
            success: function () {
                deleted($('.del-btn'), $('.delete-form'))
                $('#not_in_cart').addClass('active')
                $('#in_cart').removeClass("active")
                $('#id_size').val('')
                $('#total-inp').val($('.price-inp').html().substring(1))
                $('input[name="quantity"]').val(1)
            },
            error: function () {
                console.log('error')
            }
        })
    })

    function deleted(elem, btns) {
        $('.messages').html('<li class="mess-li success">Seccsesfuly deleted form your cart</li>' + $('.messages').html())
        setTimeout(() => {
            $('.mess-li').css({ 'display': 'none' })
        }, 2000)
        
        
        let parents = []
        for (let it of btns) {
            if ($(it).attr("data-id") == $(elem).attr('data-id')) {
                parents.push($(it).parent().parent())
                $(it).parent().remove()
                for (it of $('.tot-p')) {
                    $(it).html(countTotal() + '.0')
                }
            }
            if ($('.delete-form').length == 0) {
                for (item of parents) {
                    $(item).html('<p class="empty-text">Cart is empty</p>')
                }
                window.location = '/'

            }
        }
    }
})