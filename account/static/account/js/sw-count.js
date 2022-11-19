$(document).ready(function () {
    let form = $(".sw-container")
    const countTotal = () => {
        let pricesBlock = $('p.price-nbm')
        let total = 0;
        for (let i = 0; i < pricesBlock.length; i++) {
            console.log(pricesBlock[i].innerHTML.substring(1))
            total += Number($('.count_input')[i].value) * parseFloat(pricesBlock[i].innerHTML.substring(1))

        }
        return total
    }
    $(".sw-container").on("submit", function (e) {
        e.preventDefault()
        let name = $(e.target).children('input[type="submit"].active')[0].name
        let id = $(e.target).find('input[type="number"]').attr('data-id')
        let inp_nbm = $(e.target).find('input[type="number"]')
        let active = $(e.target).find('input[name="active"]').val()
        console.log($(e.target).find('input[name="active"]'))
        let data = {}
        data.active = active
        data.btn = name;
        data.id = id;
        let csrf = $('.sw-container').find('input[name="csrfmiddlewaretoken"]').val()
        data['csrfmiddlewaretoken'] = csrf
        let url = $(e.target).attr('action')
        $.ajax({
            url: url,
            type: "POST",
            data: data,
            cashe: true,
            success: function () {
                for (it of $('.tot-p')) {
                    console.log($('.tot-p.plur'))
                    $(it).html(countTotal() + '.0')
                }

                if (name == '_up') {
                    $(inp_nbm).val(Number($(inp_nbm).val()) + 1)
                } else if (name == '_down') {
                    $(inp_nbm).val(Number($(inp_nbm).val()) - 1)
                }

                console.log('OK')
            },
            error: function () {
                console.log('error')
            }
        })
    })







})