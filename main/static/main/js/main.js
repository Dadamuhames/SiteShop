let prodCard2 = document.querySelectorAll('.product-card');
const imageBlock = document.querySelectorAll('.images-block');

for (let img of imageBlock) {
    img.children[0].classList.add('active')
}


function changeImg(crd) {
    for (let ch of crd.children) {
        if (ch.classList.contains('images-block')) {
            for (let child of ch.children) {
                child.classList.remove('active')
            }
            ch.children[1].classList.add('active')
        }
    }
}

const imgBack = (crd) => {
    for (let ch of crd.children) {
        if (ch.classList.contains('images-block')) {
            for (let child of ch.children) {
                child.classList.remove('active')
            }
            ch.children[0].classList.add('active')
        }
    }
}


for (let card of prodCard2) {
    if ($(card).find('.prod-img').length > 1) {
        card.onmouseover = () => { changeImg(card) }
        card.onmouseout = () => { imgBack(card) }
    }

}


let countBtn = document.querySelectorAll('.sw-count');

for (let btn of countBtn) {
    btn.onclick = () => {
        $('.sw-count').removeClass('active')
        btn.classList.add('active')
        nbm_inp = btn.parentNode.children[2]
    }

}


for (item of $('.mess-li')) {
    setTimeout(() => {
        $(item).css({ 'display': 'none' })
    }, 2000)
}


$('#nbm-inp').on('input', () => {
    let price = $('#price').html().substring(1)
    $('#total-inp').val((price * $('#nbm-inp').val()).toFixed(2))
})


$('.ext-modal').on('click', (e) => {
    if (e.target.classList.contains('ext-modal')) {
        window.location.reload()
    }
})


$('#search-down').on("click", () => {
    $('.big.serach-block').toggleClass('active')
})