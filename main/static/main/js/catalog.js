$(document).ready(function () {
    $('#category-select').change((e) => {
        let id = $(e.target).val()
        let url = '/get_categories/' + id

        $.ajax({
            url: url,
            type: 'GET',
            datatype: 'json',
            success: function(data) {
                console.log($("#post_ctg"))
                if ($('#post-part').length == 1) {
                    $('#post-part').html('<select name="post_category" id="post_ctg"></select>')
                }  
                $("#post_ctg").html(`<option value="">--- Post Category ---</option>`)
                for(let key in data.post_ctg) {
                    $("#post_ctg").html($("#post_ctg").html() + `<option value="${data.post_ctg[String(key)] }">${ key }</option>`)
                }
            },
            error: function() {
                console.log('error')
            }
        })
    })
})