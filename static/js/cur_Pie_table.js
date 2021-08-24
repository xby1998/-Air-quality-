var echarts2 = echarts.init(document.getElementById("Pie"));
option2 = {
    title : {
        text: "全国空气质量比例分布",
        left: "center",
        textStyle: {
            color: "rgba(255,255,255,.9)",
            fontSize: "20"
        }
    },
    tooltip: {
        trigger: 'item'
    },
    legend: {
        top: '5%',
        orient: 'vertical',
        left: 'left',
        textStyle: {
            color: "rgba(255,255,255,.7)",
            fontSize: "12"
      }
    },
    series: [
        {
            name: '部分',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
            },
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '40',
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: []
        }
    ]
};