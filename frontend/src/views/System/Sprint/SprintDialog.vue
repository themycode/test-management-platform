<template>
  <el-dialog
    :title="sprintDialogTitle"
    width="30%"
    :visible="sprintDialogVisible"
    :show-close="true"
    :close-on-click-modal="false"
    :close-on-press-escape="true"
    @close="onCloseDialog"
  >
    <div class="user-dialog-div">
      <el-form
        :model="sprintForm"
        :rules="rules"
        ref="sprintForm"
        label-width="120px"
      >
        <el-form-item label="名称" prop="name">
          <el-input
            v-model="sprintForm.name"
            style="width:99%"
          ></el-input>
        </el-form-item>
        <!-- <el-form-item label="版本" prop="version">
                    <el-input v-model="sprintForm.version" size="small"></el-input>
                </el-form-item>-->
        <el-form-item label="预估开始时间" prop="beginTime">
          <el-date-picker
            v-model="sprintForm.beginTime"
            type="date"
            size="small"
            placeholder="预估开始时间"
            value-format="yyyy-MM-dd"
            style="width:99%"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="预估结束时间" prop="endTime">
          <el-date-picker
            v-model="sprintForm.endTime"
            type="date"
            size="small"
            placeholder="预估结束时间"
            value-format="yyyy-MM-dd"
            style="width:99%"
          ></el-date-picker>
        </el-form-item>

        <el-form-item label="描述" prop="desc">
          <el-input
            v-model="sprintForm.desc"
            type="textarea"
            style="width:99%"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="是否启用"
          prop="isActive"
          v-if="sprintDialogTitle == '修改迭代项目'"
        >
          <el-radio-group v-model="sprintForm.isActive">
            <el-radio
              v-for="item in statusOptions"
              :key="item.value"
              :label="item.value"
              >{{ item.label }}</el-radio
            >
          </el-radio-group>
        </el-form-item>
        <el-form-item>
            <el-button @click="closeDialog" style>取消</el-button>
            <el-button type="primary" @click="save('sprintForm')" style
              >保存</el-button
            >
        </el-form-item>
      </el-form>
    </div>
  </el-dialog>
</template>

<script>
export default {
  props: [
    "sprintDialogVisible",
    "sprintDialogTitle",
    "sprintData",
    "tableData",
    "statusOptions",
    "row",
    "total",
    "pageSize"
  ],
  data() {
    return {
      sprintForm: Object.assign({}, this.sprintData),
      productOptions: [], // 存放关联产品下拉选项
      rules: {
        name: [
          {
            type: "string",
            required: true,
            message: "请填写迭代项目名称",
            trigger: "blur"
          },
          {
            min: 1,
            max: 50,
            message: "长度在 1 到 50 个字符",
            trigger: "blur"
          }
        ],
        // version: [
        //     {
        //         type: "string",
        //         required: true,
        //         message: "请填写迭代项目版本",
        //         trigger: "blur"
        //     },
        //     {
        //         min: 1,
        //         max: 50,
        //         message: "长度在 1 到 50 个字符",
        //         trigger: "blur"
        //     }
        // ],
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
        isActive: [
          {
            type: "boolean",
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
      this.$emit("update:sprintDialogVisible", false); // 关闭对话框
    },

    // 新增
    addSprint() {
      this.$api.sprint
        .addSprint(this.sprintForm)
        .then(res => {
          if (res.success) {
            this.tableData.splice(0, 0, res.data);
            this.$emit("update:total", this.total + 1);

            // 如果当前页面记录数超过页面大小，则删除最后一条记录
            if (this.tableData.length > this.pageSize) {
              this.tableData.splice(-1, 1);
            }

            this.closeDialog();
            this.$message.success(res.msg);
          } else {
            this.$message.error(res.msg);
          }
        })
        .catch(res => {
          this.$message.error(res.msg || res.message);
        });
    },
    // 修改
    updateSprint() {
      this.$api.sprint
        .updateSprint(this.sprintForm)
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
            this.sprintForm.beginTime.replace(/-/g, "/")
          ).getTime();

          const endTime = new Date(
            this.sprintForm.endTime.replace(/-/g, "/")
          ).getTime();

          if (beginTime > endTime) {
            this.$message.error("开始时间不能晚于结束时间");
            return;
          }

          if (!this.sprintForm.sprintId) {
            this.addSprint();
          } else {
            this.updateSprint();
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
.user-dialog-div {
  border-style: solid;
  border-width: 1px;
  border-style: solid;
  background: rgba(241, 239, 239, 0.438);
  border-color: rgb(204, 206, 206);
  padding: 0px 0px 0px 0px;
}

</style>
