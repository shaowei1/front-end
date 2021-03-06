window.onload = function () {
    // 需求1: 页面中的图片，自动轮播。
    // 需求2: 点击按钮，改变方向。
    // 需求3: 鼠标进入停止定时器，移开再次开启。
    // 无缝滚动原理: 1.复制5张图片。     2.定时器设置left的值，负值。   3.超过5张图片的宽，要归零。

    // 需求2: 点击按钮，改变方向。
    var btn01 = document.getElementById('btn01')
    var btn02 = document.getElementById('btn02')
    var ul = document.getElementById('list')
    var num = 0
    var step = 2

    ul.innerHTML += ul.innerHTML

    setInterval(function () {
        num -= step

        // 1000等与图片宽度＋margin+ padding
        if (num < -1000) {
            num = 0
        }
        if (num > 0) {
            num = -1000
        }

        ul.style.left = num + 'px'
    }, 10)


    // 需求2: 点击按钮，改变方向。(改变方向: step正负切换)
    btn01.onclick = function () {
        // alert(1)
        // 点击左侧按钮，步长应该变为: 负数;
        step = 2;
    }
    btn02.onclick = function () {
        // alert(2)
        // 点击右侧按钮，步长应该变为: 正数;
        step = -2;
    }


}