export const elTableMixin = {
  data() {
    return {
      tableData: [], // 存放表记录
      total: 0, // 表记录行总数
      pageSizes: [10, 20, 30, 40, 50, 100, 150], //每页显示记录数选择器的选项设置
      pageSize: 10, // 表格默认每页显示记录数
      pagerCount: 7, // 设置最大页码按钮数
      currentPage: 1, // 当前页页码
      emptyText: "未获取到数据，请尝试重新打开或者刷新页面",
      checkBoxColWidth: "39px", // 第一列复选框宽度
      row: {}, // 存放当前记录行对象
      rowsSelected: [], // 存放选取的记录行
      queryForm: {}, // 查询表单
      queryRowsAPI: undefined, // 查询表格记录api
      isQueryAllowed: true, // 是否允许查询
      isPagination: true // 是否采用分页
    };
  },
  methods: {
    queryRows(event) {
      this.tableData = [];
      //   this.total = 0; // 会导致分页那边所在分页一致保持在第一页

      if (!this.isQueryAllowed) {
        this.total = 0;
        return;
      }

      if (!this.queryRowsAPI) {
        this.total = 0;
        this.$message.error("未获取到查询API,无法查询表记录");
        return;
      }
      if (this.isPagination) {
        if (event == "clickQuery") {
          // 通过点击触发查询，重置当前页面为1
          this.currentPage = 1;
        }

        this.queryForm["pageSize"] = this.pageSize;
        this.queryForm["pageNo"] = this.currentPage;
      }

      this.queryRowsAPI(this.queryForm)
        .then(res => {
          if (res.success) {
            this.total = res.data.total ? res.data.total : 0;
            this.tableData = res.data.rows;
          } else {
            this.$message.error(res.msg);
          }
        })
        .catch(res => {
          this.$message.error("获取表记录出错： " + res.msg || res.message);
        });
    },
    // 切换表格页面大小
    handleSizeChange(pageSize) {
      this.currentPage = 1;
      this.pageSize = pageSize;
      this.queryRows();
    },

    // 表格列表翻页
    handleCurrentChange(currentPage) {
      this.currentPage = currentPage;
      this.queryRows();
    },

    // 勾选记录行发生改变时事件处理函数
    onSelectChange(selection) {
      this.rowsSelected = selection;
    },

    // 逐条删除记录
    deleteRow(index, row, deleteAPI) {
      this.$confirm("确定要删除该记录吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        cancelButtonClass: "btn-custom-cancel"
      })
        .then(() => {
          // 发送删除请求
          deleteAPI({
            id: row.id
          })
            .then(res => {
              if (res.success) {
                this.$message({
                  message: res.msg,
                  type: "success"
                });

                this.tableData.splice(index, 1); // 删除本行数据
                // 减少记录总数
                this.total = this.total - 1;
                if (!this.isPagination) {
                  // 未使用分页
                  return;
                }
                if (!this.tableData.length && this.total != 0) {
                  // 如果本页数据都被删除
                  let totalPages = Math.ceil(this.total / this.pageSize);
                  if (this.currentPage > totalPages) {
                    // 当前页位于最后一页，翻页到前一页
                    this.currentPage -= 1;
                  } else {
                    // 直接刷新当前页
                  }
                  this.queryRows();
                }
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

    // 批量删除行记录
    deleteRows(deleteAPI) {
      if (!this.rowsSelected.length) {
        this.$alert("未选择记录，请勾选至少一条记录", "提示", {
          confirmButtonText: "确定"
        });
        return;
      }
      this.$confirm("确定要删除选中记录吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        cancelButtonClass: "btn-custom-cancel"
      })
        .then(() => {
          let rowIDs = []; // 存放待删除记录ID
          for (let i = 0; i < this.rowsSelected.length; i++) {
            rowIDs.push(this.rowsSelected[i].id);
          }
          // 发送删除请求
          deleteAPI({
            rowIds: rowIDs
          })
            .then(res => {
              if (res.success) {
                this.$message.success(res.msg);

                for (let i = 0; i < this.rowsSelected.length; i++) {
                  this.tableData.splice(
                    this.tableData.indexOf(this.rowsSelected[i]),
                    1
                  );
                }

                // 减少记录总数
                this.total = this.total - this.rowsSelected.length;
                if (!this.isPagination) {
                  // 未使用分页
                  return;
                }
                if (!this.tableData.length && this.total != 0) {
                  // 如果本页数据都被删除
                  let totalPages = Math.ceil(this.total / this.pageSize);

                  if (this.currentPage > totalPages) {
                    // 当前页位于最后一页，翻页到前一页
                    this.currentPage -= 1;
                  } else {
                    // 啥也不做，直接刷新当前页
                  }
                  this.queryRows();
                }
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
    // 设置表格高度
    setTableBodySize() {
      if (this.idOfSetTimeOut) {
        clearTimeout(this.idOfSetTimeOut);
      }
      this.idOfSetTimeOut = setTimeout(() => {
        var tableContainer = this.$refs.viewWrapper; // 容器
        var myTable = this.$refs.myTable; // 表格
        let toolbar = this.$refs.tableToolbar; // 操作按钮
        let queryForm = this.$refs.queryForm; // 查询表单
        let pagination = this.$refs.tablePagination; // 分页栏

        let queryFormOffsetHeight = 0;
        let queryFormMarginTop = 0;
        let queryFormMarginBottom = 0;

        let toolbarOffsetHeight = 0;
        let toolbarMarginTop = 0;
        let toolbarMarginBottom = 0;

        let myTableMarginTop = 0;
        let myTableMarginBottom = 0;
        let myTableBorderTop = 0;
        let myTableBorderBottom = 0;
        let myTablePaddingTop = 0;
        let myTablePaddingBottom = 0;

        let paginationOffsetHeight = 0;
        let paginationMarginTop = 0;
        let paginationMarginBottom = 0;

        let tableContainerHeight = tableContainer
          ? tableContainer.offsetHeight
          : 0;

        if (myTable) {
          let elementStyle = window.getComputedStyle(myTable.$el);
          myTableMarginTop = parseInt(elementStyle.marginTop.replace("px", ""));

          myTableMarginBottom = parseInt(
            elementStyle.marginBottom.replace("px", "")
          );
          myTableBorderTop = parseInt(
            elementStyle.borderTopWidth.replace("px", "")
          );
          myTableBorderBottom = parseInt(
            elementStyle.borderBottomWidth.replace("px", "")
          );

          myTablePaddingTop = parseInt(
            elementStyle.paddingTop.replace("px", "")
          );
          myTablePaddingBottom = parseInt(
            elementStyle.paddingBottom.replace("px", "")
          );
        } else {
          return;
        }

        if (queryForm) {
          queryFormOffsetHeight = queryForm.offsetHeight;

          let elementStyle = window.getComputedStyle(queryForm);
          queryFormMarginTop = parseInt(
            elementStyle.marginTop.replace("px", "")
          );
          queryFormMarginBottom = parseInt(
            elementStyle.marginBottom.replace("px", "")
          );
        }

        if (toolbar) {
          toolbarOffsetHeight = toolbar.offsetHeight;

          let elementStyle = window.getComputedStyle(toolbar);
          toolbarMarginTop = parseInt(elementStyle.marginTop.replace("px", ""));
          toolbarMarginBottom = parseInt(
            elementStyle.marginBottom.replace("px", "")
          );
        }

        if (pagination) {
          paginationOffsetHeight = pagination.$el.offsetHeight;

          let elementStyle = window.getComputedStyle(pagination.$el);
          paginationMarginTop = parseInt(
            elementStyle.marginTop.replace("px", "")
          );
          paginationMarginBottom = parseInt(
            elementStyle.marginBottom.replace("px", "")
          );
        }

        let h =
          tableContainerHeight -
          queryFormOffsetHeight -
          queryFormMarginTop -
          Math.max(queryFormMarginBottom, toolbarMarginTop) -
          toolbarOffsetHeight -
          Math.max(toolbarMarginBottom, myTableMarginTop) -
          paginationOffsetHeight -
          Math.max(myTableMarginBottom, paginationMarginTop) -
          paginationMarginBottom -
          (myTablePaddingTop +
            myTablePaddingBottom +
            myTableBorderTop +
            myTableBorderTop);

        // 设置表格行记录区高度，表格去除表头的部分
        let temp = myTable.$el.getElementsByClassName(
          "el-table__header-wrapper"
        );
        if (temp.length) {
          let tableHeaderWrapper = temp[0];
          h -= parseInt(
            window.getComputedStyle(tableHeaderWrapper).height.replace("px", "") //
          );
        }

        temp = myTable.$el.getElementsByClassName("el-table__body-wrapper");
        if (temp.length) {
          let tableBodyWrapper = temp[0];
          tableBodyWrapper.style.height = h + "px";
        }
      }, 100);
    },
    //单元格类
    getCellClassName(object) {
      if (object.column.label === "操作") {
        return "operation-col-cell-class";
      }
    }
  }
};
