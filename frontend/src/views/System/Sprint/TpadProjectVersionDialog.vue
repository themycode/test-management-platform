<template>
  <el-dialog
    :title="tpadProjectVersionDlgTitle"
    width="30%"
    :visible="tpadProjectVersionDlgVisible"
    :show-close="true"
    :close-on-click-modal="false"
    :close-on-press-escape="true"
    @close="onCloseDialog"
    v-loading="loading"
    :element-loading-text="loadingText"
  >
    <div class="user-dialog-div">
      <el-form
        :model="tpadProjectVersionForm"
        :rules="rules"
        label-width="120px"
        ref="tpadProjectVersionForm"
      >
        <el-form-item label="版本名称" prop="versionName">
          <el-input
            v-model="versionName"
            size="small"
            style="width:99%"
            disabled
          ></el-input>
        </el-form-item>
        <el-form-item label="发布日期" prop="publishDate">
          <el-date-picker
            v-model="tpadProjectVersionForm.publishDate"
            type="date"
            size="small"
            placeholder="实际发布日期"
            value-format="yyyy-MM-dd"
            style="width:99%"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <div class="dialog-footer">
            <el-button @click="closeDialog" style>取消</el-button>
            <el-button
              type="primary"
              @click="save('tpadProjectVersionForm')"
              style
              >保存</el-button
            >
          </div>
        </el-form-item>
      </el-form>
    </div>
  </el-dialog>
</template>

<script>
export default {
  props: ["tpadProjectVersionDlgVisible", "tpadProjectVersionDlgTitle", "row"],
  data() {
    return {
      loading: false, // 防短时间内重复点击，遮罩加载表示
      loadingText: "",
      tpadProjectVersionForm: {
        name: this.row.name,
        publishDate: this.row.publishDate
      },
      rules: {
        publishDate: [
          {
            type: "string",
            required: true,
            message: "请选择实际发布时间",
            trigger: "change"
          }
        ]
      }
    };
  },
  methods: {
    onCloseDialog() {
      this.closeDialog();
    },
    closeDialog() {
      this.$emit("update:tpadProjectVersionDlgVisible", false); // 关闭对话框
    },

    // 新增
    createTpadProjectVersion() {
      try {
        this.loading = true;
        this.loadingText = "正在请求创建tpad项目版本";
        let data = {
          sprintId: this.row.id,
          // projectId: 22877401,
          name: this.versionName, //名称
          publishDate: this.tpadProjectVersionForm.publishDate,
          description: this.row.desc
        };
        this.$api.tpadProject
          .addTpadProjectVersion(data)
          .then(res => {
            if (res.success) {
              this.$message.success(res.msg);
              for (let key in res.data) {
                if (key in this.row) {
                  // 以防后续表单字段有变更，仅保存对应key的值
                  this.row[key] = res.data[key];
                }
              }
            } else {
              this.$message.error(res.msg);
            }
            this.closeDialog();
            this.loading = false;
          })
          .catch(res => {
            this.loading = false;
            this.$message.error(res.msg || res.message);
          });
      } catch (err) {
        this.$message.error("请求创建tpad项目版本失败：" + err.message);
        this.loading = false;
      }
    },
    // 修改
    updateTpadProjectVersion() {
      try {
        this.loading = true;
        this.loadingText = "正在请求修改tpad项目版本";
        let data = {
          sprintId: this.row.id,
          versionId: this.row.tpadProjectVersionId,
          // projectId: 22877401,
          name: this.versionName,
          publishDate: this.tpadProjectVersionForm.publishDate,
          description: this.row.desc
        };
        this.$api.tpadProject
          .updateTpadProjectVersion(data)
          .then(res => {
            if (res.success) {
              this.$message.success(res.msg);
              for (let key in res.data) {
                if (key in this.row) {
                  this.row[key] = res.data[key];
                }
              }

              this.closeDialog();
            } else {
              this.$message.error(res.msg);
            }

            this.loading = false;
          })
          .catch(res => {
            this.loading = false;
            this.$message.error(res.msg || res.message);
          });
      } catch (err) {
        this.$message.error("请求修改tpad项目版本失败：" + err.message);
        this.loading = false;
      }
    },
    // 保存
    save(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          if (!this.row.tpadProjectVersionId) {
            this.createTpadProjectVersion();
          } else {
            this.updateTpadProjectVersion();
          }
        } else {
          // 校验失败
        }
      });
    }
  },
  computed: {
    versionName() {
      if (this.tpadProjectVersionForm.publishDate) {
        return (
          this.row.name +
          "(发布于" +
          this.tpadProjectVersionForm.publishDate +
          ")"
        );
      } else {
        return this.row.name;
      }
    }
  }
};
</script>

<style scoped>
.user-dialog-div {
  border-style: solid;
  border-width: 1px;
  border-style: solid;
  background: rgba(241, 239, 239, 0.438);
  border-color: rgb(204, 206, 206);
  padding: 0px 0px 0px 0px;
}
.dialog-footer {
  text-align: center;
  margin-left: -120px; /* 表单 .el-form-item__content margin-left 100px */
}
</style>
