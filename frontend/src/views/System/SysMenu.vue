<template>
  <div class="system-menu-div">
    <el-tree
      ref="sysMenuTree"
      class="system-menu-tree"
      :props="defaultProps"
      :load="loadNode"
      empty-text="未获取到数据，请尝试刷新页面"
      lazy
      node-key="id"
      :expand-on-click-node="false"
      :render-content="renderContent"
      :default-expanded-keys="defaultExpandedKeys"
    ></el-tree>

    <sys-menu-dialog
      v-if="menuDialogVisible"
      :dialogVisible.sync="menuDialogVisible"
      :dialogTitle="menuDialogTitle"
      :dialogFormData="menuData"
      :menuNode="menuNode"
    ></sys-menu-dialog>
  </div>
</template>

<script>
import SysMenuDialog from "./SysMenu/SysMenuDialog";


export default {
  components: {
    SysMenuDialog
  },
  data() {
    return {
      defaultProps: {
        label: "name",
        children: "children",
        isLeaf: "isLeaf" // 是否叶子节点
      },
      defaultExpandedKeys: [], // 存放默认展开的节点ID
      menuDialogVisible: false, // 菜单对话框是否可见 true-可见，false-不可见
      menuDialogTitle: "", // 存放菜单对话框标题
      menuData: null, // 存放菜单数据
      menuNode: null // 存放当前节点
    };
  },

  methods: {
    loadNode(node, resolve) {
      // loadNode优先于mounted方法被调用
      if (node.level == 0) {
        this.$api.sysMenu
          .getSysMenuTree({ parentId: -1, recursive: false })
          .then(res => {
            if (res.success) {
              //展开所有顶级节点
              for (let i = 0; i < res.data.length; i++) {
                this.defaultExpandedKeys.push(res.data[i].id);
              }

              return resolve(res.data);
            } else {
              this.$message.error(res.msg);
              return resolve([]);
            }
          })
          .catch(res => {
            this.$message.error(res.msg || res.message);
            return resolve([]);
          });
      } else if (node.level >= 1) {
        // 如果加载的是非顶级菜单，根据菜单id，加载其一级子菜单
        this.$api.sysMenu
          .getSysMenuTree({
            parentId: node.data.id,
            recursive: false
          })
          .then(res => {
            if (res.success) {
              return resolve(res.data);
            } else {
              this.$message.error(res.msg);
              return resolve([]);
            }
          })
          .catch(res => {
            this.$message.error(res.msg || res.message);
            return resolve([]);
          });
      }
    },
    // 点击添加按钮事件处理函数
    addNode(node, data, store) {
      if (!this.menuDialogVisible) {
        this.menuDialogVisible = true;
        this.menuDialogTitle = "添加资源";

        this.menuData = {
          parentId: data.id,
          type: "菜单",
          name: "",
          desc: "",
          name: "",
          url: "",
          icon: "",
          perms: "",
          requireAuth: true,
          show: true,
          showWithoutAuth: true,
          collapsed: false,
          order: ""
        };

        this.menuNode = node;
      }
    },
    // 点击修改按钮事件处理函数
    editNode(node, data, store) {
      if (!this.menuDialogVisible) {
        this.menuDialogVisible = true;
        this.menuDialogTitle = "修改资源";

        this.menuData = {
          id: data.id,
          type: data.type,
          name: data.name,
          desc: data.desc,
          url: data.url,
          icon: data.icon,
          perms: data.perms,
          requireAuth: data.requireAuth,
          show: data.show,
          showWithoutAuth: data.showWithoutAuth,
          collapsed: data.collapsed,
          order: data.order
        };

        this.menuNode = node;
      }
    },
    removeNode(node, data, store) {
      // 删除节点
      this.$confirm(
        "'确定删除吗？ 删除该节点，将会删除其下所有子节点",
        "提示",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
          cancelButtonClass: "btn-custom-cancel"
        }
      )
        .then(() => {
          // 发送请求，执行删除操作
          this.$api.sysMenu
            .deleteSysMenu({
              id: data.id
            })
            .then(res => {
              if (res.success) {
                this.$refs.sysMenuTree.remove(node);
                this.$message({
                  message: res.msg,
                  type: "success"
                });
              } else {
                this.$message.error(res.msg);
              }
            })
            .catch(res => {
              this.$message.error(res.msg || res.message);
            });
        })
        .catch(() => {});
    },
    renderContent(h, { node, data, store }) {
      return h(
        "span",
        {
          style: {
            // color: "red"
          },
          //这里添加hover事件
          on: {
            // 鼠标进入
            mouseenter: () => {
              this.$set(data, "showOperationBtn", true);
              this.$set(data, "children", []);
            },
            //鼠标离开
            mouseleave: () => {
              this.$set(data, "showOperationBtn", false);
            }
          }
        },
        [
          h(
            "span",
            {
              //显示名称
            },
            node.label
          ),
          h(
            "span",
            {
              style: {
                display: data.showOperationBtn ? "" : "none"
              }
            },
            [
              h(
                "el-button",
                {
                  props: {
                    type: "text",
                    size: "small"
                  },
                  style: {
                    marginLeft: "10px"
                  },
                  on: {
                    click: () => {
                      this.addNode(node, data, store);
                    }
                  }
                },
                "添加"
              ),
              h(
                "el-button",
                {
                  props: {
                    type: "text",
                    size: "small"
                  },
                  style: {
                    display: data.id ? "" : "none" //  如果为根节点，则不显示修改
                  },
                  on: {
                    click: () => {
                      this.editNode(node, data, store);
                    }
                  }
                },
                "修改"
              ),
              h(
                "el-button",
                {
                  props: {
                    type: "text",
                    size: "small"
                  },
                  style: {
                    display: data.id ? "" : "none"
                  },
                  on: {
                    click: () => {
                      this.removeNode(node, data, store);
                    }
                  }
                },
                "删除"
              )
            ]
          )
        ]
      );
    }
  }
};
</script>

<style lang="scss" scoped>
.system-menu-div {
  height: 100%;
}

.system-menu-tree {
  position: absolute;
  top: 10px;
  bottom: 0px;
  left: 10px;
  width: 30%;
  overflow: auto;
  font-size: 14px;
  background: #e7e6e6;
  border-color: rgb(204, 206, 206);
  border-style: solid;
  border-width: 1px;
}
</style>
