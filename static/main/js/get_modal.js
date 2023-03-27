$(document).ready(function () {
    //Open modal
    $(".open-modal").on('click', (e) => {
        let modalBlock = $('.main-black')
        modalBlock.addClass('active')
        let url = $(e.target).attr('data-url')
        let href = $(e.target).parent().find('.images-block')[0].href

        $.ajax({
            url: url,
            datatype: 'json',
            type: 'GET',
            success: function(data) {
                fillModal(data)
                $('.more-detail-a')[0].href = href
                for (let l = 0; l < $('.dot').length; l++) {
                    $('.dot')[l].onclick = (e) => {
                        activeSLides(l)
                    }
                    $('#product-form').on("change", (e) => {
                        get_variant(e)
                    })
                }
            },
            error: function() {
                console.log('error')
            }
        })
    })


    function fillModal(data) {
        $('.none').removeClass('active')
        $('.slide').remove()
        $('.dot').remove()
        $('.atributs-wrapper').html("")

        for(img of data.imgs) {
            $('.slider-items-img')[0].innerHTML += `<img src="${img}" alt="" class="slide">`
            $('.dots')[0].innerHTML += `<span class="dot"></span>`
        }

        $('.slide')[0].classList.add('active')
        $('.dot')[0].classList.add('active')

        let url = '/del/'
        $('.del-btn').attr('data-delurl', url+data.scu)
        $('.del-btn').attr('data-id', data.scu)
        $('.name-inp').html(data.name)
        $('.price-inp').html('$' + data.price.toFixed(2))
        $('input[name="product"]').val(data.scu)
        $('input[name="variant"]').val(data.variant)
        $('#id_size').val(data.size)
        $('input[name="quantity"]').val(data.count)
        $('#total-inp').val(data.total.toFixed(2))
        $('#not_in_cart').addClass('active')

        $("#colors-select").html('<option value="">-----</option>')
        for(let color of data.colors) {
            $("#colors-select").html(
                 $("#colors-select").html() + `
                    <option value="${ color.id }">${ color.name }</option>
                `
            )
        }

        let atributs = data.atributs
        for (let key in atributs) {
            let id = key.split(' ')[0]
            $(".atributs-wrapper").html(
            $(".atributs-wrapper").html() + 
            `
                <br>
                <label class="form-label" id="ctg-label-for-data">${ key }</label><br><br>
                <select name="atribut_${id}" id='atribut_${id}' class="selected-select select-atribut" required></select>
                <br>
            `)
            for (let opt of atributs[String(key)]) {
                $(`#atribut_${id}`).html(
                    $(`#atribut_${id}`).html() +
                    `
                    <option value="${opt.id}">${opt.name}</option>
                `
                ) 
            }

        }
    }


    function activeSLides(i) {
        $('.slide.active').removeClass("active")
        $('.dot.active').removeClass('active')
        $('.dot')[i].classList.add('active')
        $('.slide')[i].classList.add('active')
    }

    function get_variant(e) {
        if (e.target.classList.contains('select-atribut')) {
            let url = $('#product-form').attr('data-url');
            let csrf = $('input[name="csrfmiddlewaretoken"]').val()
            let prod = $('input[name="product"]').val()
            let data = {}
            for (let input of document.querySelectorAll(".select-atribut")) {
                data[input.name] = input.value
            }

            data.id = prod
            data['csrfmiddlewaretoken'] = csrf;

            $.ajax({
                url: url,
                data: data,
                datatype: 'json',
                type: 'POST',
                success: (data) => {
                    console.log(data)
                    get_variant_render(data)
                },
                error: () => {
                    console.log('error')
                }
            })
        }
    }


    function get_variant_render(data) {
        console.log(data)
        if (Object.keys(data).length > 0) {
            $('input[name="variant"]').val(data.id)
            $("#price").html('$' + data.price.toFixed(2))
            $('#total-inp').val(
                (Number($('#nbm-inp').val()) * Number(data.price)).toFixed(2)
            )

            $('#prod-imgs').html('')
            for (let src of data.img) {
                $('#prod-imgs').html(
                    $('#prod-imgs').html() + `
                        <img src="${src}" alt="" class="slide">
                    `
                )
            }
            $(".slide")[0].classList.add('active')

            if (data.in_cart) {
                $(".btn-block").html(
                    `
                        <span id="in_cart" style="display: contents;">
                            <span class="span-btn sbm-btn btn-base qw change-prod" >Already in Cart</span>
                            <a data-delurl="" href="/del/${ data.id }" data-id=""
                                class="sbm-btn btn-base white del-btn">
                                <span class="material-symbols-outlined">
                                    delete
                                </span>
                            </a>
                        </span>
                    `
                )
            } else {
                $(".btn-block").html(
                    `
                        <span id="not_in_cart" style="display: contents;">
                            <input name="_cart" type="submit" class="sbm-btn btn-base" style="color: #fff;"
                                value="Add to Cart">
                        </span>
                    `
                )
            }

        } else {
            $('input[name="variant"]').val('')
            console.log('none')
            $(".btn-block").html(
                `
                    <span class="sbm-btn btn-base white change-prod" style="padding: 10px; opacity: 0.6; cursor: not-allowed;" style="display: contents;">Combination unavialable</span>
                `
            )
        }
    }

})