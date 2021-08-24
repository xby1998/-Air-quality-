// 获取实时数据
function getnowtime() {
    $.ajax({
        url:"/time",
        data:{"name":"现在"},
        type:"post",            // HTTP请求类型
        timeout:10000,          // 超时设置为10秒
        success:function(data) {
            $("#time_now").html("当前时间：" + data) // 在网页中更新时间
        },
        error:function(){
            alter("实时数据时间失败")
        },
    })
}
// 表单提交，post获取数据
$("#form2").submit(function(e){
	e.preventDefault();             // 禁用表单的自动提交
    var province_name = $(this).serialize();
    $.ajax({
        url:"/data_country",
        type:'POST',
        data: $(this).serialize(),   // 这个序列化传递很重要
        success:function(data) {
            $("#time_update").html(data.Today_time)     //设置更新时间
            if(data.p_name == "全国"){                    // 如果是全国地图则直接绘制
                echarts1.setOption(drawMap('china',{},data.map_data));
            }
            else{
                // 省份地图需要先获取该省的数据
                updatemap(data.p_name,data.map_data)         // 先更新地图
            }
            option2.series[0].data=data.pie_data
            option2.title.text= data.p_name + "空气质量比例分布"
            echarts2.setOption(option2)

            option3.yAxis[0].data=data.rank_data.pro_name
            option3.yAxis[1].data=data.rank_data.data
            option3.series[0].data=data.rank_data.data
            echarts3.setOption(option3)
        },
        error:function(){
            alter("更新数据失败")
        },
    })
});
// 获取省份地图
function updatemap(geo_name,data1) {
    $.ajax({
        url:"/geo_map",
        type:'POST',
        data:{"province_name":geo_name},
        timeout:10000,          //超时设置为10秒
        success:function(data) {
            // 绘制省份地图
            op = drawMap(geo_name,data,data1)
            echarts1.setOption(op)
        },
        error:function(){
            alter("更新地图失败")
        },
    })
}
// 初始化地图，get方式获取默认全国数据
function init_map(){
    $.ajax({
        url:"/data_country",
        type:'get',
        success:function(data) {
            $("#time_update").html(data.Today_time)     //设置更新时间
            // 全国地图的调用方式
            echarts1.setOption(drawMap('china',{},data.map_data));
            option2.series[0].data=data.pie_data
            option2.title.text= data.p_name + "空气质量比例分布"
            echarts2.setOption(option2)

            option3.yAxis[0].data=data.rank_data.pro_name
            option3.yAxis[1].data=data.rank_data.data
            option3.series[0].data=data.rank_data.data
            echarts3.setOption(option3)
        },
        error:function(){
            alter("更新数据失败")
        },
    })
}
setInterval(getnowtime,100)     //定时执行
init_map()
// getnowtime()
window.onresize=function(){
    echarts1.resize();
    echarts2.resize();
    echarts3.resize();
}