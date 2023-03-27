const accardionHeaders = document.querySelectorAll('.header');
const plusBtn = document.querySelectorAll('.open-acrd');
const accard = document.querySelectorAll('.acrd');

for (let i = 0; i < accardionHeaders.length; i++) {
    accardionHeaders[i].onclick = () => {
        let op = ''
        for (let l = 0; l < accard.length; l++) {
            if(i != l && accard[l].classList.contains('active')) {
                op = plusBtn[l].dataset.oper
                plusBtn[l].dataset.oper = plusBtn[l].innerHTML 
                plusBtn[l].innerHTML = op  
                accard[l].classList.remove('active')                
            }

        }
        op = plusBtn[i].innerHTML
        plusBtn[i].innerHTML = plusBtn[i].dataset.oper
        plusBtn[i].dataset.oper = op
        console.log(plusBtn[i].innerHTML)
        accard[i].classList.toggle('active')

    }
}