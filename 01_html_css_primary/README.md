# HTML
xhtml	严谨1.0，2.0失败<br>
html5	向下兼容，松散，

## 两种结尾
.htm	.html

## 单标签可以不闭合
```html
<h1>
<img>单标签	<img src="./1.jpg">也可以<img/>
```

## tools
visual studio code<br>
webstorm<br>
vscode	

## the latest simple
！tab 补全
```html
<DOCTYPE html>	#文档声明 默认html5标准来解析的
<html lang='en'>	# 中文
<html>
	<head>
		<meta charset='UTF-8'>
		<title>
		</title>
	</head>
        <body>
	</body>
</html>
```

## 注释
<meta3 IE8, edge>
注释部分单行多行
```html
<!-- -->
```

## element
1. <块级元素：html有些标签能够独占一行, 双标签元素，有开启、闭合
    ```html
    <p>人到中年不得已，保温杯里加枸杞</p> # 段落中间有段落距离
    <p>一到中年岁月推，加完当归加枸杞</p>
    ```

2. 单标签，自己独立
    不识别换行，只给一个空格
    使用\<br> 换行，行距没有
    查看元素使用select
    ```html
    <input type="text"> <br><br>
    ```

3. 带属性的标签
    \<img src="path" alt="" width="100px" heigth="100"> #alt图片路径不存在时显示信息,
    宽高只设置一个，自适应
    1366*768	--> 横着1366个像素点
    ```html
    <a href="http://www.baidu.com">百度</a>
    <a href="http://www.baidu.com" tartget="_self"/"_blank">百度</a>
    ```

4. 标签的嵌套
    ```html
    <div></div> # 相当于一个收纳箱，盒子
    层叠样式表
    div + css + js ==	html + css
    
    <div>
        <p>
            <img src="">
            <a href="">name</name>
        </p>
    </div>
    
    单位px, em
    一个字长&emsp; 一个空额&nbsp; 
    ```


## someone else
01. 块级标签，内联
    ```html
    <h1></h1>　# 标签没有h1->h6	批量操作
    h1-h6是标题标签，独占一行
    
    h1一般作为logo

    ```
    
02. <p>
    独占一行、css属性做开头缩进

03.  <div>

04. 行级元素 
    ```html
    <img>
    不独占一行
    <a href="#"></a>	# 跳转到最顶端 ,不写刷新, # 卯点　# javascript:;点了也白点
    
    <span></span>	没有任何风格的标签
    ```

05. 字符实体（有些内容不能直接输入，需要转意符号）
    ```html
    <div>
        我认为$lt;<h1>$lt;</h1>可以做网站ｌｏｇｏ
        我认为$lt;h1>$lt;/h1>可以做网站ｌｏｇｏ
        小于号	&lt;
        大于号	&gt;
        空格	&nbsp;
    </div>

    ```

06. CSS<br>
cascading style sheets


