export const elTreeMixin = {
  data() {
    return {
      defaultProps: {
        label: "name",
        children: "children",
        isLeaf: "isLeaf" // 是否叶子节点
      },
      treeData: [], // 存放树结点数据
      emptyText: "未获取到数据，请重新打开或刷新页面重试",
      contextMenuVisible: false, // 控制右键菜单是否显示 true-显示 false-不显示
      currNodeDataObject: null, // 存放当前节点数据对象
      currNode: null, // 存放当前节点对象
      defaultExpandedKeys: [] // 存放默认展开的节点ID
    };
  },
  methods: {
    // 左键点击节点
    clickNode(dataObject, node, vueComponent) {
      this.handleNodeLeftClickEvent(dataObject);
    },
    // 处理鼠标左键点击节点事件
    handleNodeLeftClickEvent(dataObject) {
      this.hideContextMenu();
    },

    // 右键点击树结点
    rightClickNode(event, dataObject, node, vueComponent) {
      this.contextMenuVisible = false; // 关闭右键菜单模态对话框
      this.currNodeDataObject = dataObject;
      this.currNode = node;

      //   let scrollTop =
      //     document.documentElement.scrollTop || document.body.scrollTop;
      //   let scrollLeft =
      //     document.documentElement.scrollLeft || document.body.scrollLeft;

      this.contextMenuVisible = true; // 显示模态对话框，跳出自定义菜单面板
      let menu = document.querySelector("#contextMenu");
      if (!menu) {
        return;
      }

      //   menu.style.left = (event.clientX + scrollLeft) + "px"; // 滚动条位置 + 鼠标指针相对于客户区的位置
      //   let menuStyleTop = event.clientY + scrollTop;

      menu.style.left = event.pageX + "px"; // 滚动条位置 + 鼠标指针相对于客户区的位置
      menu.style.top = event.pageY + "px";
      let menuStyleTop = event.pageY;

      // 点击的位置到tree所在容器底部距离小于菜单高度，菜单top位置上移一个菜单的高度，保证菜单不被遮挡 // 未设置菜单style.top值时，获取的菜单高度为0
      this.$nextTick(() => {
        let menuOffsetHeight = menu.offsetHeight;
        if (
          this.$refs.treeContainer.offsetHeight -
            (menuStyleTop -
              this.$refs.treeContainer.getBoundingClientRect().top) <
          menuOffsetHeight
        ) {
          // menu.style.top = event.clientY + scrollTop - menuOffsetHeight + "px";
          menu.style.top = (event.pageY - menuOffsetHeight) + "px";
        } else {
          //   menu.style.top = (event.clientY + scrollTop) + "px";
          menu.style.top = event.pageY + "px";
        }
      });

      document.addEventListener("click", this.hideContextMenu); // 给整个document添加监听鼠标事件，点击任何位置，隐藏右键菜单
    },
    // 隐藏右键菜单
    hideContextMenu() {
      this.contextMenuVisible = false;
      document.removeEventListener("click", this.hideContextMenu); // 取消鼠标监听事件
    },

    // 获取当前结点所在父结点的路径
    getParentSuitePath(parentNodeId) {
      let nodeObj = this.$refs.tree.getNode(parentNodeId);

      if (nodeObj) {
        let suiteName = nodeObj.data.name;
        let parentId = nodeObj.data.parentId;
        if (parentId != -1) {
          // 存在上级分类
          return this.getParentSuitePath(parentId) + "/" + suiteName;
        } else {
          return "/" + suiteName;
        }
      }
      return "";
    }
  }
};
