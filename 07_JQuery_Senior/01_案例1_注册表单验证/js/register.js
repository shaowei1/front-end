$(function () {

    var bool_username = false
    var bool_pwd1 = false
    var bool_pwd2 = false
    var bool_email = false
    var bool_checkbox = true


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
            bool_username = true

        } else {
            // 格式不对
            $(this).next().show().html('请输入6-20位内容，数字、字母、下划线')
            bool_username = false

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
            bool_pwd1 = true

        } else {
            // 格式不对
            $(this).next().show().html('请输入6-20位内容，数字、字母、下划线')
            bool_pwd1 = false

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
            bool_pwd2 = true

        } else {
            // 格式不对
            $(this).next().show().html('两次密码不一致')
            bool_pwd2 = false

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
            bool_email = true
        } else {
            // 格式不对
            $(this).next().show().html('请输入正确的邮箱地址: explame@outlook.com')
            bool_email = false
        }

    })

    $("#allow").click(function () {
        if ($(this).prop("checked") === false) {
            $(this).next().next().show().html("请同意美多商城用户使用协议")
            bool_checkbox = false
        } else {
            $(this).next().next().hide()
            bool_checkbox = true
        }
        console.log(bool_username
            , bool_pwd1
            , bool_pwd2
            , bool_email
            , bool_checkbox)

    })

    $("form").submit(function (event) {

        var flag = (bool_checkbox && bool_email && bool_pwd2 && bool_pwd1 && bool_username)
        if (flag) {
            // return false
            alert("注册成功")
        } else {
            event.preventDefault()

        }

    })

    function is_empty(parse) {
        if ($(parse).val() == '') {
            $(parse).next().hide()
            return true
        }

    }


})
