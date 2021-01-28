<template>
    <div :id="elementID"></div>
</template>

<script>
import uuidv1 from "uuid/v1"; // 引入uuid文件
export default {
    name: "nightingale-rose-diagram-chart",
    props: [
        "pieData",
        "pieColor",
        "pieTitle",
        "echartPicIdDict",
        "keyForEchartId",
        "showLegend"
    ],
    data() {
        return {
            elementID: "", // 图表ID
            color: [], // 图标颜色
            legendData: [], // 图例数据
            centerTextLeft: 0, // 饼图中间文字左侧距离容器最左边的宽度
            centerTextTop: 0 // 饼图中间文字顶部侧距离容器最上边的宽度
        };
    },
    methods: {
        // 获取单行文本的像素宽度
        getTextPixelWith(text, fontStyle) {
            var canvas = document.createElement("canvas"); // 创建 canvas 画布
            var context = canvas.getContext("2d"); // 获取 canvas 绘图上下文环境
            context.font = fontStyle; // 设置字体样式，使用前设置好对应的 font 样式才能准确获取文字的像素长度
            var dimension = context.measureText(text); // 测量文字
            return dimension.width;
        }
    },
    created() {
        this.elementID = uuidv1(); //获取随机id
        this.echartPicIdDict[this.keyForEchartId] = this.elementID;

        if (this.pieColor) {
            // 设置图例数据和饼图数据块颜色
            for (let i = 0; i < this.pieData.seriesData.length; i++) {
                this.legendData.push({
                    name: this.pieData.seriesData[i].name,
                    // 设置图例文字颜色
                    textStyle: {
                        color: this.pieColor[this.pieData.seriesData[i].name]
                    }
                });

                // 获取饼图数据块颜色
                this.color.push(this.pieColor[this.pieData.seriesData[i].name]);
            }
        } else {
            for (let i = 0; i < this.pieData.seriesData.length; i++) {
                this.legendData.push(this.pieData.seriesData[i].name);
            }
        }
    },

    mounted() {
        // 获取饼图容器高度和宽度
        let pieContainer = document.getElementById(this.elementID);
        let pieContainerWidth = window.getComputedStyle(pieContainer).width;
        pieContainerWidth = parseFloat(pieContainerWidth.split("px")[0]);
        let pieContainerHeight = window.getComputedStyle(pieContainer).height;
        pieContainerHeight = parseFloat(pieContainerHeight.split("px")[0]);

        let centerTextFontSize = 13; // 饼图中间文字大小
        let centerTextFontFamily = "Microsoft YaHei"; // 饼图中间文字family

        // 获取文本行最大像素宽度
        let lines = this.pieData.centerText.split("\n");
        let max_line_pixel_width = 0;
        for (let i = 0; i < lines.length; i++) {
            // 获取字符串行占用的像素宽度
            let textLinePixelWidth = this.getTextPixelWith(
                lines[i],
                centerTextFontSize + "px " + '"' + centerTextFontFamily + '"'
            );
            if (max_line_pixel_width < textLinePixelWidth) {
                max_line_pixel_width = textLinePixelWidth;
            }
        }

        // 计算饼图中间文字相对于饼图容器的左上角坐标
        // 饼图圆心相对于容器的x坐标 - 饼图中心文本行最大像素宽度 / 2
        this.centerTextLeft =
            pieContainerWidth * 0.45 - max_line_pixel_width / 2;
        // top：饼图圆心相对于容器的y坐标 - 饼图中心文本行像素高度 * 文本行数大像素宽度 / 2  //fontSize定义的其实就是字体高度
        this.centerTextTop =
            pieContainerHeight * 0.6 - (centerTextFontSize * lines.length) / 2;

        let option = {
            title: {
                // 饼图标题
                text: this.pieTitle, //主题文本
                subtext:"",
                textStyle: {
                    fontSize: "14", // 字体大小
                    color: "grey" // 字体颜色
                },
                left: "3%", // 组件离容器左侧的距离
                top: "5%" // 组件离容器上侧的距离。
            },
            // color // 调色盘颜色列表。如果系列没有设置颜色，则会依次循环从该列表中取颜色作为系列颜色。
            // 默认为：
            // ['#c23531','#2f4554', '#61a0a8', '#d48265', '#91c7ae','#749f83',  '#ca8622', '#bda29a','#6e7074', '#546570', '#c4ccd3']
            // color: this.color,
            // 提示框组件。
            tooltip: {
                trigger: "item", // 触发类型 item 数据项图形触发
                // formatter 提示框浮层内容格式器，支持字符串模板和回调函数两种形式。从左到右别表示 系列名 数据名 数据值 百分比
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            graphic: {
                //饼图中间添加文字
                type: "text",
                left: this.centerTextLeft, // left、top可以是百分比值，也可以是center，也可以时number像素
                top: this.centerTextTop,
                style: {
                    text: this.pieData.centerText, // 饼图中间
                    textAlign: "center", // 文字水平对齐方式
                    textVerticalAlign: "middle", // 文字纵向对其方式
                    fill: "#000", //文字的颜色
                    fontSize: centerTextFontSize, // 文字大小
                    fontFamily: centerTextFontFamily
                }
            },

            legend: {
                show:this.showLegend, // 是否显示图例
                orient: "vertical", // 图例列表的布局朝向
                // icon: 'circle', // 设置图例形状
                itemHeight: 10, // 图例标记的图形宽度。
                itemWidth: 10, // 图例标记的图形高度
                top: "3%", // 图例组件离容器上侧的距离
                right: "0", // 图例组件离容器右侧的距离
                x: "right", // 水平方向的安放位置
                // 格式化图例文本
                formatter: name => {
                    let target;
                    for (let i = 0; i < this.pieData.seriesData.length; i++) {
                        if (this.pieData.seriesData[i].name == name) {
                            target = this.pieData.seriesData[i].value;
                        }
                    }
                    let arr = ["{a|" + name + "}", target];
                    return arr.join(" ");
                },
                data: this.legendData,
                textStyle: {
                    rich: {
                        a: {
                            color: "black" //还原图例格式化前的文本的颜色
                        }
                    }
                }
            },
            calculable: true,
            series: [
                {
                    name: this.pieTitle, // 系列名称 //用于tooltip的显示，legend 的图例筛选，在 setOption 更新数据和配置
                    type: "pie",
                    radius: ["20%", "60%"], // 内半径，外半径（可视区尺寸（容器高宽中较小一项）的百分比）
                    center: ["45%", "60%"], // 图形中心点坐标
                    roseType: "area",
                    data: this.pieData.seriesData, // 饼图数据

                    avoidLabelOverlap: true, // 是否启用防止标签重叠策略，默认开启，在标签拥挤重叠的情况下会挪动各个标签的位置，防止标签间的重叠。饼图中，要强制所有标签放在中心位置，可以将该值设为 false
                    label: {
                        // 饼图图形上的文本标签，可用于说明图形的一些数据信息，比如值，名称等
                        normal: {
                            show: true, // true -显示标签，false-隐藏标签
                            position: "outside", // 标签的位置。
                            formatter: "{b} {c}({d}%)", // 标签内容格式化器
                            fontSize: centerTextFontSize // 设置字体 //设置为和图形中间的文本字体一样大小
                        }
                    },
                    // 标签的视觉引导线样式
                    labelLine: {
                        normal: {
                            show: true
                        }
                    },

                    enableMouseTracking: false,
                    shadow: false
                    // animation: false
                }
            ]
        };

        if (this.color.length) {
            option["color"] = this.color;
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
