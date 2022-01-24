console.log('foodUpdate.js ...');

function upd(id) {
    const res = confirm("确认修改吗?");  //在页面上弹出对话框
    if (!res) {
        return;
    }
    // 验证参数
    if (id === undefined || id === '') {
        alert('请选择修改的数据');
        return ;
    }

    // 封装参数
    let params = {
        food_id : $("input[name='food_id']").val(),
        food_name: $("input[name='food_name']").val(),
        food_cal: $("input[name='food_cal']").val(),
        taste: $("input[name='taste']").val(),
        location: $("input[name='location']").val()
    };
    console.log(params);
    $.ajax({
        type: "POST",
        url: "/food/update",
        dataType: "json",
        data: JSON.stringify(params),
        success: function(res){
            // console.log( res );
            alert("修改成功！");
            history.go(-1);
        }
    });
}