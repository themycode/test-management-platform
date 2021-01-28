export const horizontalDragMixin = {
  data() {
    return {
      ifMouseDown: false, // 标记鼠标是否按下
      leftElementOffsetLeft: 0 // 左侧元素对象于整个文档的距离
    };
  },
  methods: {
    // 获取元素相对于整个文档的偏移坐标
    getOffsetLeft(element) {
      let offsetLeft = element.offsetLeft;
      let parent = element.offsetParent;
      while (parent != null) {
        offsetLeft += parent.offsetLeft;
        parent = parent.offsetParent;
      }
      return offsetLeft;
    },
    // 鼠标点击事件
    mousedown(e) {
      if (!this.$refs.leftElement) {
        return;
      }
      this.leftElementOffsetLeft = this.getOffsetLeft(
        this.$refs.leftElement.$el
      );
      let leftElement = this.$refs.leftElement.$el;

      let leftElementOffsetRight =
        this.leftElementOffsetLeft + leftElement.offsetWidth; // 左侧元素最右侧边框距离文档左侧的距离 // 左侧元素左边距离文档最左侧距离 + 左侧元素宽度

      if (
        leftElementOffsetRight - 10 <= e.pageX &&
        e.pageX <= leftElementOffsetRight + 10
      ) {
        this.ifMouseDown = true;
        document.body.style.cursor = "e-resize";
      } else {
        this.ifMouseDown = false;
        document.body.style.cursor = "auto";
      }
    },
    mousemove(e) {
      if (!this.$refs.leftElement) {
        return;
      }
      this.leftElementOffsetLeft = this.getOffsetLeft(
        this.$refs.leftElement.$el
      );
      let leftElement = this.$refs.leftElement.$el;
      let leftElementOffsetRight =
        this.leftElementOffsetLeft + leftElement.offsetWidth;

      if (
        leftElementOffsetRight - 10 <= e.pageX &&
        e.pageX <= leftElementOffsetRight + 10
      ) {
        document.body.style.cursor = "e-resize";
      } else {
        if (!this.ifMouseDown) {
          document.body.style.cursor = "auto";
        }
      }
      if (
        this.ifMouseDown &&
        e.pageX > this.leftElementOffsetLeft + 15 &&
        e.pageX < this.leftElementOffsetLeft + document.body.offsetWidth / 2
      ) {
        e.preventDefault(); // 防止拖拽时选中页面内容
        let temp_left_element_width = e.pageX - this.leftElementOffsetLeft;
        leftElement.style.width = temp_left_element_width + "px";
        let rightElement = this.$refs.rightElement.$el;
        rightElement.style.left = temp_left_element_width + 2 + "px";

        // 如果右侧是表格，自动调整高度，避免水平滚动条被分页组件遮挡
        if (this.$refs.rightElement.setTableBodySize) {
          this.$refs.rightElement.setTableBodySize();
        }
      }
    },
    mouseup() {
      this.ifMouseDown = false;
    }
  }
};
