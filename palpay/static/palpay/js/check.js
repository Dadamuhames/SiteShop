const nbmInput = document.getElementById('nbm-input');
const fields = document.querySelectorAll('.field');
const btnOrder = document.querySelector('.buy-btn');


nbmInput.oninput = () => {
    let vl = nbmInput.value;
    let bol = true;
    nbms = '1234567890+'
    for(let n of vl) {
        if(!nbms.includes(n)) {
            bol = false
            break;
        }
    }

    if(vl.includes('+998') && vl.length == 13 && bol) {
        nbmInput.classList.remove('error')
        btnOrder.classList.remove('disabled')
    } else {
        nbmInput.classList.add('error')
        btnOrder.classList.add('disabled')
    }

}


const paymentTyps = document.querySelectorAll('.choose-payment');


for(let type of paymentTyps) {
    type.onclick = () => {
        for (let tp of paymentTyps) {
            tp.checked = false
        }
        type.checked = true
    }
}