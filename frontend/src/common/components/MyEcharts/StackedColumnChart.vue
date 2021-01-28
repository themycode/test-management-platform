<template>
    <div :id="elementID" style="height: 0px"></div>
</template>

<script>
import uuidv1 from "uuid/v1"; // 引入uuid文件
export default {
    name: "stacked-column-chart",
    props: [
        "barData",
        "barColor",
        "barTitle",
        "echartPicIdDict",
        "keyForEchartId",
        "yAxisType",
        "xAxisType",
    ],
    data() {
        return {
            elementID: "", // 图表ID
            color: [], // 图标颜色
            legendData: [], // 图例数据
            axisYType: this.yAxisType, // y轴类型
            axisXType: this.xAxisType, // x轴类型
        };
    },
    created() {
        this.elementID = uuidv1(); //获取随机id
        this.echartPicIdDict[this.keyForEchartId] = this.elementID;
        // // 设置图例数据和柱状图颜色
        for (let i = 0; i < this.barData.seriesData.length; i++) {
            this.legendData.push(this.barData.seriesData[i].name);

            if (this.barColor) {
                // 获取柱状图颜色
                this.color.push(this.barColor[this.barData.seriesData[i].name]);
            }
        }
    },
    mounted() {
        if (!this.axisXType) {
            this.axisXType = "category";
        }

        if (!this.axisYType) {
            this.axisYType = "value";
        }

        let option = {
            title: {
                text: this.barTitle, //主题文本
                textStyle: {
                    fontSize: "14", // 字体大小
                    color: "grey", // 字体颜色
                },
                left: "3%", // 离容器左侧的距离
                top: "5%", // 离容器上侧的距离。
            },
            // color: this.color,
            tooltip: {
                trigger: "axis", // 坐标轴触发
                formatter: function (params, ticket, callback) {
                    let total = 0; // 存放总缺陷数
                    for (let i = 0; i < params.length; i++) {
                        total += params[i].data;
                    }
                    let obj = params.map((item, index) => {
                        let percent = total
                            ? ((item.value / total) * 100).toFixed(1)
                            : "0.0%";

                        // 小圆点显示
                        let dotColor =
                            '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' +
                            item.color +
                            '"></span>';
                        return (
                            dotColor +
                            item.seriesName +
                            ": " +
                            item.value +
                            "(" +
                            percent +
                            "%" +
                            ")" +
                            "</br>"
                        );
                    });
                    return obj.join(""); // 去除','
                },

                axisPointer: {
                    // 坐标轴指示器，坐标轴触发有效// 坐标轴指示器是指示坐标轴当前刻度的工具
                    type: "line", // 默认为直线，可选为：'line' | 'shadow'
                },
            },
            legend: {
                top: "2%", // 图例组件离容器上侧的距离,
                data: this.legendData,
            },
            grid: {
                left: "0.3%", //grid 组件离容器左侧的距离。
                right: "2%", // grid 组件离容器右侧的距离。
                bottom: "1%", // grid 组件离容器下侧的距离。
                containLabel: true, // grid 区域是否包含坐标轴的刻度标签
            },
            // 直角坐标系 grid 中的 x 轴
            xAxis: {
                type: this.axisXType, // x轴类型，未给定的情况下，为 'category' 类目轴，适用于离散的类目数据，为该类型时必须通过 data 设置类目数据。
                data: this.barData.xAxisData,
                axisLabel: {
                    interval: 0, // 显示全部
                    rotate: 30, // 设置坐标轴标签倾斜
                    // formatter: function(value) {
                    //     // 设置坐标轴纵向显示
                    //     return value.split("").join("\n");
                    // }
                },
            },
            // 直角坐标系 grid 中的 y 轴
            yAxis: [
                {
                    type: this.axisYType, // y轴类型，未给定的情况下 数值轴，适用于连续数据。
                    data: this.barData.yAxisData,
                    axisLabel: {
                        interval: 0, // 显示全部
                        rotate: 30, // 设置坐标轴标签倾斜
                        // formatter: function(value) {
                        //     // 设置坐标轴纵向显示
                        //     return value.split("").join("\n");
                        // }
                    },
                },
            ],
            series: this.barData.seriesData,
        };

        if (this.color.length) {
            option["color"] = this.color;
        }

        let chartDom = document.getElementById(this.elementID);
        const chartObj = this.$echarts.init(chartDom);

        if (this.axisXType == "value") {
            option["xAxis"]["max"] = function (value) {
                if (value) {
                    if (value.max > 1000) {
                        return value.max + 150; // 给最大值增加一个数值，防止柱状图右侧的数值统计文案被截断
                    } else if (value.max > 500) {
                        return value.max + 100;
                    } else if (value.max > 100) {
                        return value.max + 50;
                    } else if (value.max > 50) {
                        return value.max + 20;
                    } else {
                        return value.max + 10;
                    }
                } else {
                    return 0;
                }
            };
        let barHeight = this.barData.seriesData.length * 30 + 100; // 自动调整高度
        chartDom.style.height = barHeight + "px";

        }

        chartObj.setOption(option);
        chartObj.resize();

        window.addEventListener("resize", function () {
            chartObj.resize();
        });
    },
};
</script>
