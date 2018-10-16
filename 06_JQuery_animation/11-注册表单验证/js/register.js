$(function () {
    // 失去焦点的时候，判断内容是否符合正则表达式。
    $("#user_name").blur(function () {
        // 空字符串特殊处理

        if (is_empty(this)) {
            return
        }

        // 通过正则
        if (/^\w{6,20}$/.test($(this).val())) {
            // 满足条件
            $(this).next().hide()
        } else {
            // 格式不对
            $(this).next().show().html('请输入6-20位内容，数字、字母、下划线')
        }

    })


    $("#pwd").blur(function () {
        if (is_empty(this)) {
            return
        }

        var rePass = /^[\w!@#$%^&*]{6,20}$/;

        // 通过正则
        if (rePass.test($(this).val())) {
            // 满足条件
            $(this).next().hide()
        } else {
            // 格式不对
            $(this).next().show().html('请输入6-20位内容，数字、字母、下划线')
        }

    })

    $("#cpwd").blur(function () {
        if (is_empty(this)) {
            return
        }

        // 通过正则
        if ($(this).val() == $("#pwd").val()) {
            // 满足条件
            $(this).next().hide()
        } else {
            // 格式不对
            $(this).next().show().html('两次密码不一致')
        }

    })

    $("#email").blur(function () {
        if (is_empty(this)) {
            return
        }

        var reMail = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/i;
        // 通过正则
        if (reMail.test($(this).val())) {
            // 满足条件
            $(this).next().hide()
        } else {
            // 格式不对
            $(this).next().show().html('请输入正确的邮箱地址: explame@outlook.com')
        }

    })

    $("#allow").click(function(){
        if ($(thist).prop("checked") === false){
            $(this).next().next().show().html("请同意美多商城用户使用协议")
        }else{
            $(this).next().next().hide()
        }

    })

    $("form").submit(function (event) {

        if ($("#allow").prop("checked")) {
            // 取消提交1
            // return false;

            // 取消提交2: 取消默认行为
            // console.log(event)
            alert("ok")
        } else {

            alert('请同意美多商城用户使用协议')
            event.preventDefault()

        }

    })

    function is_empty(parse) {
        if ($(parse).val() == '') {
            $(parse).next().hide()
            $(parse).next().show().html($(parse).prev().html() + 'is empty')
            return true
        }

    }


})
