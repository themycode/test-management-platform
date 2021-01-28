<template>
    <div :id="elementID"></div>
</template>

<script>
import uuidv1 from "uuid/v1"; // 引入uuid文件
export default {
    name: "stacked-line-chart",
    props: [
        "seriesData",
        "xAxisData",
        "lineColor",
        "lineTitle",
        "yAxisAxisLabel",
        "tooltipFormatter",
        "echartPicIdDict",
        "keyForEchartId",
        "yAxisMax"
    ],
    data() {
        return {
            elementID: "", // 图表ID
            color: [], // 图标颜色
            legendData: [] // 图例数据
        };
    },
    created() {
        this.elementID = uuidv1(); //获取随机id
        this.echartPicIdDict[this.keyForEchartId] = this.elementID;

        if (this.lineColor) {
            // 设置图例数据和折线图颜色
            for (let i = 0; i < this.seriesData.length; i++) {
                this.legendData.push({
                    name: this.seriesData[i].name
                });

                // 获取饼图数据块颜色
                this.color.push(this.lineColor[this.seriesData[i].name]);
            }
        } else {
            // 设置图例数据和折线图颜色
            for (let i = 0; i < this.seriesData.length; i++) {
                this.legendData.push({
                    name: this.seriesData[i].name
                });
            }
        }
    },
    mounted() {
        let option = {
            title: {
                text: this.lineTitle || ""
            },
            tooltip: {
                trigger: "axis"
            },
            legend: {
                orient: "horizontal", // 图例列表的布局朝向
                icon: "circle", // 设置图例形状
                top: "5%", // 图例组件离容器上侧的距离
                data: this.legendData
            },
            grid: {
                left: "3%", //grid 组件离容器左侧的距离。
                right: "2%", // grid 组件离容器y右侧的距离。
                bottom: "2%", // grid 组件离容器下侧的距离。
                containLabel: true // grid 区域是否包含坐标轴的刻度标签
            },
            xAxis: {
                type: "category",
                boundaryGap: false, // 坐标轴两边留白策略
                data: this.xAxisData,
                axisLabel: {
                    interval: 0, // 显示全部
                    rotate: 30 // 设置坐标轴标签倾斜
                }
            },
            yAxis: {
                type: "value",
                max:this.yAxisMax
            },
            series: this.seriesData
        };

        if (this.color.length) {
            option["color"] = this.color;
        }

        if (this.tooltipFormatter) {
            option["tooltip"]["formatter"] = this.tooltipFormatter;
        }

        if (this.yAxisAxisLabel) {
            option["yAxis"]["axisLabel"] = this.yAxisAxisLabel;
        }

        const chartObj = this.$echarts.init(
            document.getElementById(this.elementID)
        );
        chartObj.setOption(option);
        window.addEventListener("resize", function() {
            chartObj.resize();
        });
    }
};
</script>
