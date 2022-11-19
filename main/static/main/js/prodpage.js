function click() {
    const slideItems = document.querySelectorAll('.slide');
    const imgDots = document.querySelectorAll('.img-dot');


    slideItems[0].classList.add('active');
    imgDots[0].classList.add('active');


    for (let i = 0; i < imgDots.length; i++) {
        imgDots[i].onclick = () => {
            for (let slide of slideItems) {
                slide.classList.remove('active')
            }
            for (let dot of imgDots) {
                dot.classList.remove('active')
            }
            slideItems[i].classList.add('active')
            imgDots[i].classList.add('active')
        }

    }
}

if ($(".slide").length > 0) {
    click()
}



const reply = document.querySelectorAll('.pull-right');
const replInp = document.querySelectorAll('.reply');


for(let i = 0; i < reply.length; i++) {
    reply[i].onclick = () => {
        replInp[i].classList.toggle('active')
    }
}


$('.cansel-adding').on('click', (e) => {
    e.preventDefault()
    $($(e.target).parent().parent()).find('textarea').val('')
})

$('.big-slide')[0].classList.add('active')


$('.ext-galery').on("click", () => {
    $(".original-images-slider").removeClass('active')
})

$(".slide").on('click', () => {
    $(".original-images-slider").addClass('active')
})



let ind = 0
const activateSlide = (i) => {
    $(".big-slide").removeClass("active")
    $('.big-slide')[i].classList.add('active')
}

$('#prev').on('click', () => {
    if (ind > 0) {
        ind--;
    } else {
        ind = $(".big-slide").length - 1
    }
    activateSlide(ind);
})


$('#next').on('click', () => {
    if(ind < $('.big-slide').length - 1 && ind >= 0) {
        ind++;
    } else {
        ind = 0
    } activateSlide(ind);
})


$('#product-form').on("change", (e) => {
    if(e.target.classList.contains('select-atribut')) {
        //let selects = $(".select-atribut").val()
        let url = $('#product-form').attr('data-url');
        let csrf = $('input[name="csrfmiddlewaretoken"]').val()
        let prod = $('input[name="product"]').val()
        let data = {}
        for (let input of document.querySelectorAll(".select-atribut")) {
            console.log(input.name + " | " + input.value)
            data[input.name] = input.value
            console.log(input)
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
                if(Object.keys(data).length > 0) {
                    $('input[name="variant"]').val(data.id)
                    $("#price").html('$' + data.price.toFixed(2))
                    $('#total-inp').val(
                        (Number($('#nbm-inp').val()) * Number(data.price)).toFixed(2)
                    )

                    $('#prod-imgs').html('')
                    $('.img-dots').html('')
                    console.log($('#prod-imgs'))
                    for(let src of data.img) {
                        $('#prod-imgs').html(
                            $('#prod-imgs').html() + `
                                <img src="${ src }" alt="" class="slide">
                            `
                        )

                        $('.img-dots').html(
                            $('.img-dots').html() + `
                                <button class="img-dot">
                                    <img src="${ src }" alt="">
                                </button>
                            `
                        )
                    } 
                    $(".slide")[0].classList.add('active')
                    $('.img-dot')[0].classList.add('active')
                    click()

                    if (data.in_cart) {
                        $("#add-to-cart-btns").html(
                            `
                                <button class="sbm-btn btn-base white change-prod" style="padding: 0;">Combination already in Cart</button>
                                <a href="/del/${ data.id }" class="sbm-btn btn-base white">
                                    <span class="material-symbols-outlined">
                                        delete
                                    </span>
                                </a>
                            `
                        )                        
                    } else {
                        $("#add-to-cart-btns").html(
                            `
                            <input type="submit" class="sbm-btn btn-base white" name="_cart" value="Add to Cart">

                            `
                        )   
                    }

                } else {
                    $('input[name="variant"]').val('')
                    $("#add-to-cart-btns").html(
                        `
                            <span class="sbm-btn btn-base white change-prod" style="padding: 10px; opacity: 0.6; cursor: not-allowed;">Combination unavialable</span>
                        `
                    )  
                }
            }
        })        
    }




})



