$('#order_server').change(function () {
    var env_id = $(this).val()
    $.ajax({
        url: '../get_monitor_operator_info/',
        type: 'GET',
        data: {
            'env_id': env_id
        },
        dataType: "json",
        success: function (ret) {
            console.log(ret)
            var content = ''
            $.each(ret, function (i, item) {
                console.log(i)
                console.log(item)
                content += '<option value=' + item.engineer_id + '>' + item.username + '</option>'
            })
            $('#id_operator').html(content)
        }
    })
})