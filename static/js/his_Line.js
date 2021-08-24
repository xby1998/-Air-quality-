var echarts1 = echarts.init(document.getElementById("Line"));
var option1 = {
    //timeline基本配置都写在baseoption 中
    baseOption: {
        timeline: {
            //loop: false,
            axisType: 'category',
            show: true,
            autoPlay: true,
            playInterval: 10000,
            data: ['1', '2', '3','4', '5', '6','7', '8', '9','10', '11', '12']
        },
        grid: {containLabel: true},
        xAxis: [{
            type: 'category',
            name: 'time',
        },],
        yAxis: {type: 'value'},
        series: [
            {
                type: 'line',
            },
        ],
        tooltip: {},
        title: {
                text: '城市月份变化图',
                subtext: 'AQI'
            },

    },
    //变量则写在options中
    options: [{xAxis: [{data: []}],series: [{data: []},]},
        {xAxis: [{data: []}],series: [{data: []},]},
        {xAxis: [{data: []}],series: [{data: []},]},
        {xAxis: [{data: []}],series: [{data: []},]},
        {xAxis: [{data: []}],series: [{data: []},]},
        {xAxis: [{data: []}],series: [{data: []},]},
        {xAxis: [{data: []}],series: [{data: []},]},
        {xAxis: [{data: []}],series: [{data: []},]},
        {xAxis: [{data: []}],series: [{data: []},]},
        {xAxis: [{data: []}],series: [{data: []},]},
        {xAxis: [{data: []}],series: [{data: []},]},
        {xAxis: [{data: []}],series: [{data: []},]},
    ]
}
