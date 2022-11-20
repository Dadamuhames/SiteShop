$(".ship-type")[0].classList.add('active')



for(let btn of document.querySelectorAll(".ship-type")) {
    btn.onclick = () => {
        $('.ship-type').removeClass("active")
        btn.classList.add('active')
        $('input[name="ship_type"]').val($(btn).attr("data-ship-id"))        
    }

}