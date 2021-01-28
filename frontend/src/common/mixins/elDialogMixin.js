export const elDialogMixin = {
  data() {
    return {
      dialogWidth: "35%", // 对话框默认宽度
      showClose: true, // 是否显示对话框关闭按钮
      closeOnClickModal: false, // 点击对话框之外的区域是否关闭对话框
      closeOnPressEscape: true, // 按Esc键盘是否关闭对话框
      dialogFormLabeWidth: "120px", // 对话框表单标签宽度
      requestData: null // 通过对话框提交的请求数据
    };
  },
  methods: {
    onCloseDialog() {
      this.closeDialog();
    },
    closeDialog() {
      this.$emit("update:dialogVisible", false);
    },

    add(addAPI) {
      if (!this.requestData) {
        this.requestData = this.dialogForm;
      }
      addAPI(this.requestData)
        .then(res => {
          if (res.success) {
            this.$message.success(res.msg);
            this.closeDialog();

            this.tableData.splice(0, 0, res.data);
            this.$parent.total += 1;

            if (!this.$parent.isPagination) {
              // 未使用分页
              return;
            }
            if (this.tableData.length > this.$parent.pageSize) {
              // 如果当前页面记录数超过页面大小，则删除最后一条记录
              this.tableData.splice(-1, 1);
            }
          } else {
            this.$message.error(res.msg);
          }
        })
        .catch(res => {
          this.$message.error(res.msg || res.message);
        });
    },
    update(updateAPI) {
      if (!this.requestData) {
        this.requestData = this.dialogForm;
      }
      updateAPI(this.requestData)
        .then(res => {
          if (res.success) {
            this.$message.success(res.msg);
            this.closeDialog();

            for (let key in res.data) {
              if (key in this.row) {
                this.row[key] = res.data[key];
              }
            }
          } else {
            this.$message.error(res.msg);
          }
        })
        .catch(res => {
          this.$message.error("修改失败： " + res.msg || res.message);
        });
    }
  }
};
