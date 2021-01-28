<template>
  <el-dialog
    :title="ztProjectDialogTitle"
    width="30%"
    :visible="ztProjectDialogVisible"
    :show-close="true"
    :close-on-click-modal="false"
    :close-on-press-escape="true"
    @close="onCloseDialog"
  >
    <div class="zentao-project-dialog-div">
      <el-form
        :model="ztProjectForm"
        :rules="rules"
        ref="ztProjectForm"
        label-width="120px"
      >
        <el-form-item label="名称" prop="name">
          <el-input
            v-model="ztProjectForm.name"
            size="small"
            style="width:99%"
            disabled
          ></el-input>
        </el-form-item>
        <el-form-item label="关联产品" prop="productIds">
          <el-select
            v-model="ztProjectForm.productIds"
            :multiple="true"
            clearable
            filterable
            placeholder="请选择需要关联的产品"
            style="width:99%"
          >
            <el-option
              v-for="item in productOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="预估开始时间" prop="beginTime">
          <el-date-picker
            v-model="ztProjectForm.beginTime"
            type="date"
            size="small"
            placeholder="预估开始时间"
            value-format="yyyy-MM-dd"
            style="width:99%"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="预估结束时间" prop="endTime">
          <el-date-picker
            v-model="ztProjectForm.endTime"
            type="date"
            size="small"
            placeholder="预估结束时间"
            value-format="yyyy-MM-dd"
            style="width:99%"
          ></el-date-picker>
        </el-form-item>

        <el-form-item label="描述" prop="desc">
          <el-input
            v-model="ztProjectForm.desc"
            type="textarea"
            style="width:99%"
          ></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="ztProjectStatus">
          <el-radio-group v-model="ztProjectForm.ztProjectStatus">
            <el-radio
              v-for="item in ztProjectStatusOptions"
              :key="item.value"
              :label="item.value"
              >{{ item.label }}</el-radio
            >
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <div class="dialog-footer">
            <el-button @click="closeDialog" style>取消</el-button>
            <el-button type="primary" @click="save('ztProjectForm')" style
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
  props: [
    "ztProjectDialogVisible",
    "ztProjectDialogTitle",
    "ztProjectData",
    "row"
  ],
  data() {
    return {
      ztProjectForm: Object.assign({}, this.ztProjectData),
      productOptions: [], // 存放关联产品下拉选项
      ztProjectStatusOptions: [
        // 禅道项目状态选项
        { label: "未开始", value: "wait" },
        { label: "进行中", value: "doing" },
        { label: "已完成", value: "done" }
      ],
      rules: {
        productIds: [
          {
            type: "array",
            required: true,
            message: "请选择迭代要关联的产品",
            trigger: "change"
          }
        ],
        beginTime: [
          {
            type: "string",
            required: true,
            message: "请选择预估起始时间",
            trigger: "change"
          }
        ],
        endTime: [
          {
            type: "string",
            required: true,
            message: "请选择预估结束时间",
            trigger: "change"
          }
        ],
        desc: [
          {
            min: 0,
            max: 500,
            message: "不能超过 500 个字符",
            trigger: "blur"
          }
        ],
        ztProjectStatus: [
          {
            type: "string",
            required: true,
            message: "请选是否启用",
            trigger: "blur"
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
      this.$emit("update:ztProjectDialogVisible", false); // 关闭对话框
    },

    // 新增
    createZtProject() {
      this.$api.zentaoProject
        .addZtProject(this.ztProjectForm)
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
        })
        .catch(res => {
          this.$message.error(res.msg || res.message);
        });
    },
    // 修改
    updateZtProject() {
      this.$api.zentaoProject
        .updateZtProject(this.ztProjectForm)
        .then(res => {
          if (res.success) {
            this.$message.success(res.msg);
            for (let key in res.data) {
              if (key in this.row) {
                // 以防后续表单字段有变更，仅保存对应key的值
                this.row[key] = res.data[key];
              }
            }
            this.closeDialog();
          } else {
            this.$message.error(res.msg);
          }
        })
        .catch(res => {
          this.$message.error(res.msg || res.message);
        });
    },
    // 保存
    save(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          const beginTime = new Date(
            this.ztProjectForm.beginTime.replace(/-/g, "/")
          ).getTime();

          const endTime = new Date(
            this.ztProjectForm.endTime.replace(/-/g, "/")
          ).getTime();

          if (beginTime > endTime) {
            this.$message.error("开始时间不能晚于结束时间");
            return;
          }

          if (!this.ztProjectForm.ztProjectId) {
            this.createZtProject();
          } else {
            this.updateZtProject();
          }
        } else {
          // 校验失败
        }
      });
    }
  },
  created() {
    // 获取禅道产品
    this.$api.zentaoProduct
      .queryProductsDetails()
      .then(res => {
        if (res.success) {
          this.productOptions = res.data;
        } else {
          this.$message.error(res.msg);
        }
      })
      .catch(res => {
        this.$message.error(res.msg || res.message);
      });
  }
};
</script>

<style scoped>
.zentao-project-dialog-div {
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
