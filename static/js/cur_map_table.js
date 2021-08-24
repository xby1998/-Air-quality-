var echarts1 = echarts.init(document.getElementById("chinaMap"));
// 绘制地图，mapName为地图名，geo_province为省份的地理数据，data1为需要可视化的数据
function drawMap(mapName,geo_province,data1) {
    if(mapName == "china"){
    }
    else{
        echarts.registerMap(mapName, geo_province);
    }
    var option1 = {
        tooltip: {
            trigger: 'item',
            formatter: '{b}<br/>{c}'
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
                dataView: {readOnly: false},
                restore: {},
                saveAsImage: {}
            }
        },
        visualMap: {
            min: 20,
            max: 100,
            text: ['High', 'Low'],
            realtime: false,
            calculable: true,
            inRange: {
                color: ['lightskyblue', 'yellow', 'orangered']
            }
        },
        series: [{
            type: 'map',
            map: mapName,
            label: {
                show: true
            },
            data: data1
        }]
    };
    return option1
}