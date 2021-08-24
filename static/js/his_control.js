// 获取实时时间
function getnowtime() {
    $.ajax({
        url:"/time",
        data:{"name":"现在"},
        type:"post",            //HTTP请求类型
        timeout:10000,          //超时设置为10秒
        success:function(data) {
            $("#time_now").html("当前时间：" + data)
            console.log(data)
        },
        error:function(){
            alter("实时数据时间失败")
        },
    })
}

// 采用get方式， 获取默认数据
function get_data() {
    $.ajax({
        url:"/data",
        type:'get',            //HTTP请求类型
        timeout:10000,          //超时设置为10秒
        success:function(data) {
            $("#time_update").html(data.Today_data.Today_date)
            $("#city_name").html(data.Today_data.Today_city)
            $("#num").html(data.Today_data.Today_num)
            $("#status").html(data.Today_data.Today_status)
            $("#warn1").html(data.Today_data.Today_feature1)
            $("#warn2").html(data.Today_data.Today_feature2)
            $("#p_one").html(data.Today_data.Today_pollute.PM2_5)
            $("#p_two").html(data.Today_data.Today_pollute.CO)
            $("#p_three").html(data.Today_data.Today_pollute.SO2)
            $("#p_four").html(data.Today_data.Today_pollute.PM10)
            $("#p_five").html(data.Today_data.Today_pollute.OO)
            $("#p_six").html(data.Today_data.Today_pollute.NO2)
            option1.baseOption.timeline.data = Object.keys(data['year_dict'])
            var counter = 0
            for(var key in data['year_dict']){
                option1.options[counter].xAxis[0].data = data.year_dict[key].city_time
                option1.options[counter].series[0].data = data.year_dict[key].city_AQI
                counter++
            }
            echarts1.setOption(option1)
            option2.series[0].data = data.cate
            echarts2.setOption(option2)
        },
        error:function(){
            alter("更新数据失败")
        },
    })
}
// 表达提交，post方式请求数据
$("#form1").submit(function(e){
	e.preventDefault();             // 禁用表单的自动提交
    $.ajax({
        url:"/data",
        type:'POST',
        data: $(this).serialize(),   // 这个序列化传递很重要
        success:function(data) {
            $("#time_update").html(data.Today_data.Today_date)
            $("#city_name").html(data.Today_data.Today_city)
            $("#num").html(data.Today_data.Today_num)
            $("#status").html(data.Today_data.Today_status)
            $("#warn1").html(data.Today_data.Today_feature1)
            $("#warn2").html(data.Today_data.Today_feature2)
            $("#p_one").html(data.Today_data.Today_pollute.PM2_5)
            $("#p_two").html(data.Today_data.Today_pollute.CO)
            $("#p_three").html(data.Today_data.Today_pollute.SO2)
            $("#p_four").html(data.Today_data.Today_pollute.PM10)
            $("#p_five").html(data.Today_data.Today_pollute.OO)
            $("#p_six").html(data.Today_data.Today_pollute.NO2)

            option1.baseOption.timeline.data = Object.keys(data['year_dict'])
            var counter = 0
            for(var key in data['year_dict']){
                option1.options[counter].xAxis[0].data = data.year_dict[key].city_time
                option1.options[counter].series[0].data = data.year_dict[key].city_AQI
                counter++
            }
            echarts1.setOption(option1)
            option2.series[0].data = data.cate
            echarts2.setOption(option2)
        },
        error:function(){
            alter("更新数据失败")
        },
    })
});
setInterval(getnowtime,100)        //定时执行
get_data()          //初始时数据
echarts1.setOption(option1);
echarts2.setOption(option2);
window.onresize=function(){
    echarts1.resize();
    echarts2.resize();
}