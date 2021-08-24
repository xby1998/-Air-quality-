var echarts2 = echarts.init(document.getElementById("Pie"));

option2 = {
    title : {
        text: "空气质量比例分布",
        subtext:"质量分类",
        left: "center",
        textStyle: {
            color: "rgba(0,0,0,.9)",
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
            color: "rgba(0,0,0,.7)",
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
            data: [{'name': '中度污染', 'value': 2}, {'name': '良', 'value': 148}, {'name': '轻度污染', 'value': 35}, {'name': '优', 'value': 210}]
        }
    ]
};
