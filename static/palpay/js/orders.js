let ordLnks = document.querySelectorAll('.filter-links');
let ordPage = document.querySelectorAll('.orders-page');

$($('.orders-page')[0]).addClass('active')

const deActive = () => {
    for(let i = 0; i < ordLnks.length; i++) {
        ordLnks[i].classList.remove('active')
        ordPage[i].classList.remove('active')
    }
}


ordLnks.forEach((e, i) => {
    e.onclick = () => {
        if (ordPage[i].classList.contains('order-product-card')) {
            $(ordPage[i]).find('.slide').removeClass('active')
            $(ordPage[i]).find('.img-dot').removeClass('active')
            $($(ordPage[i]).find('.slide')[0]).addClass('active')
            $($(ordPage[i]).find('.img-dot')[0]).addClass('active')
        }
        
        deActive()
        ordLnks[i].classList.add('active')
        ordPage[i].classList.add('active')
    }
}) 




const stBtn = document.querySelectorAll(".status-btn");
const hidenForm = document.querySelectorAll('.hidden-form');


stBtn.forEach((e,i) => {
    e.onclick = () => {
        for(let l = 0; l < hidenForm.length; l++) {
            if(l != i) {
                hidenForm[l].classList.remove('active')                
            }

        }
        hidenForm[i].classList.toggle('active')
    }
})
