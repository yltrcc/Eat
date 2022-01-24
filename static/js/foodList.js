console.log('foodList.js ...');

function del(food_id) {
    const ok = confirm("确认删除吗？");
    if (!ok) {
        return ;
    }

    // 验证参数
    if (food_id === undefined || food_id == '') {
        alert('请选择删除的数据');
        return ;
    }

    // 封装参数
    let params = {
        id : food_id
    };
    console.log(params);
    $.ajax({
        type: "POST",
        url: "/food/delete",
        dataType: "json",
        data: JSON.stringify(params),
        success: function(res){
            // console.log( res );
            location.reload();
        }
    });
}