<template>
  <div class="testplan-case-detail-content-div">
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header>
        <keep-alive>
          <header-bar :currentModule="currentModule"></header-bar>
        </keep-alive>
      </el-header>

      <!-- 主内容区 -->
      <div class="plan-case-detail-content">
        <div class="case-detail-div">
          <el-button size="small" @click="editCase" v-if="!caseEditing">
            <i class="fa fa-edit" aria-hidden="true"></i>编辑
          </el-button>
          <el-button size="small" @click="cancelCaseEditing" v-else>
            <i class="fa fa-edit" aria-hidden="true"></i>取消
          </el-button>
          <el-button size="small" @click="saveCase" v-if="caseEditing">
            <i class="fa fa-floppy-o" aria-hidden="true"></i>保存
          </el-button>
        </div>
        <div class="case-detail-div">
          <span>用例编号：</span>
          <span v-if="!caseEditing" style="font-weight:bold;">{{
            caseInfo.customNo
          }}</span>
          <el-input
            v-else
            placeholder="请输入用例唯一编号"
            v-model="caseInfo.customNo"
            minlength="1"
            maxlength="60"
            size="small"
            clearable
          ></el-input>

          <br />
          <span>用例名称：</span>
          <span v-if="!caseEditing" style="font-weight:bold;">{{
            caseInfo.name
          }}</span>

          <el-input
            v-else
            placeholder="请输入用例名称"
            v-model="caseInfo.name"
            minlength="1"
            maxlength="60"
            size="small"
            clearable
          ></el-input>
        </div>
        <div class="case-detail-div">
          <div style="display:inline-block; margin-right:20px">
            <span>创建人：{{ caseInfo.createrName }}</span>
          </div>
          <div style="display:inline-block; margin-right:20px">
            <span>更新人：{{ caseInfo.updaterName }}</span>
          </div>

          <div
            style="display:inline-block; padding-left: 20px;padding-right:20px"
          >
            <span>优先级</span>：
            <span v-if="!caseEditing">{{ caseInfo.priority }}</span>
            <el-select
              v-else
              ref="casePrioritySelect"
              v-model="caseInfo.priority"
              clearable
              style="width: 100px;"
              size="mini"
            >
              <el-option label="P1" value="P1"></el-option>
              <el-option label="P2" value="P2"></el-option>
              <el-option label="P3" value="P3"></el-option>
              <el-option label="P4" value="P4"></el-option>
            </el-select>
          </div>
          <div
            style="display:inline-block; padding-left: 20px;padding-right:40px"
          >
            <span>用例类型：</span>
            <span v-if="!caseEditing">{{ caseInfo.type }}</span>
            <el-select
              v-else
              ref="typeSelect"
              v-model="caseInfo.type"
              clearable
              style="width: 100px;"
              size="mini"
            >
              <el-option label="功能" value="功能"></el-option>
              <el-option label="接口" value="接口"></el-option>
              <el-option label="自动化" value="自动化"></el-option>
            </el-select>
          </div>
          <div style="display:inline-block">
            <span>测试集：{{ caseInfo.suitePath }}</span>
          </div>
        </div>

        <div class="case-detail-div">
          <span>前置条件：</span>
          <span v-if="!caseEditing">{{ caseInfo.precondition }}</span>
          <el-input
            v-else
            ref="preconditionInput"
            type="textarea"
            placeholder="请输入前置条件"
            v-model="caseInfo.precondition"
            maxlength="30"
            show-word-limit
          ></el-input>
        </div>

        <div class="case-detail-div">
          测试步骤：
          <!-- 操作按钮 -->
          <el-row v-if="caseEditing">
            <el-button-group>
              <el-button size="mini" @click="addCaseStep">新增</el-button>
              <el-button size="mini" @click="deleteCaseStepsInBatch"
                >删除</el-button
              >
            </el-button-group>
            <span>说明：双击以下步骤行可以进入编辑状态</span>
          </el-row>

          <!-- 表格 -->
          <el-table
            :data="caseStepTableData"
            style="width: 100%;margin-bottom: 0px; overflow:auto"
            border
            @row-dblclick="dblclickStepRow"
            @selection-change="onSelectChange"
          >
            <!--多选复选框-->
            <el-table-column
              type="selection"
              width="35px"
              align="center"
              :resizable="false"
            ></el-table-column>
            <el-table-column
              type="index"
              align="center"
              :resizable="false"
            ></el-table-column>
            <!-- 展示索引列 -->
            <el-table-column
              prop="id"
              label="ID"
              width="65px"
              header-align="center"
              align="center"
              :resizable="false"
            ></el-table-column>
            <el-table-column
              prop="action"
              label="步骤动作"
              min-width="250px"
              show-overflow-tooltip
              header-align="center"
              align="left"
            >
              <template slot-scope="scope">
                <span v-if="scope.row.editing">
                  <el-input
                    type="textarea"
                    size="small"
                    placeholder="请输入步骤动作"
                    v-model="scope.row.action"
                  ></el-input>
                </span>
                <span v-else>{{ scope.row.action }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="expection"
              label="预期结果"
              min-width="250px"
              header-align="center"
              align="center"
            >
              <template slot-scope="scope">
                <span v-if="scope.row.editing">
                  <el-input
                    type="textarea"
                    size="small"
                    placeholder="请输入步骤预期结果"
                    v-model="scope.row.expection"
                  ></el-input>
                </span>
                <span v-else>{{ scope.row.expection }}</span>
              </template>
            </el-table-column>

            <el-table-column
              label="操作"
              align="center"
              width="220px"
              :resizable="false"
              v-if="caseEditing"
            >
              <template slot-scope="scope">
                <el-button
                  v-if="!scope.row.editing"
                  size="mini"
                  @click="editCaseStep(scope.$index, scope.row)"
                  >编辑</el-button
                >
                <el-button
                  v-if="scope.row.editing"
                  size="mini"
                  @click="finishCaseStepEditing(scope.$index, scope.row)"
                  >完成</el-button
                >
                <el-button
                  v-if="scope.row.editing"
                  size="mini"
                  @click="cancelCaseStepEditing(scope.$index, scope.row)"
                  >取消</el-button
                >
                <el-button
                  v-if="!scope.row.editing"
                  size="mini"
                  @click="insertCaseStep(scope.$index, scope.row)"
                  >插入</el-button
                >

                <el-button
                  size="mini"
                  type="danger"
                  @click="deleteOneCaseStep(scope.$index, scope.row)"
                  >删除</el-button
                >
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div class="case-detail-div">
          <span>后置条件：</span>
          <span v-if="!caseEditing">{{ caseInfo.postcondition }}</span>
          <el-input
            v-else
            ref="postconditionInput"
            type="textarea"
            placeholder="请输入后置条件"
            v-model="caseInfo.postcondition"
            maxlength="30"
            show-word-limit
          ></el-input>
        </div>

        <div class="case-detail-div">
          <span style="margin-right:10px">用例标签：</span>
          <el-tag
            :key="tag"
            v-for="tag in this.caseInfo.tags"
            :closable="caseEditing"
            :disable-transitions="true"
            @close="onCloseTag(tag)"
            >{{ tag }}</el-tag
          >
          <el-input
            class="input-new-tag"
            v-if="tagInputVisible"
            v-model="tagInputValue"
            ref="saveTagInput"
            size="small"
            @keyup.enter.native="handleTagInputConfirm"
            @blur="handleTagInputConfirm"
          ></el-input>

          <el-button
            v-else-if="caseEditing"
            class="button-new-tag"
            size="small"
            @click="showTagInput"
            >+点击新增标签</el-button
          >
        </div>
        <div class="case-detail-div">
          <span>用例描述：</span>
          <span v-if="!caseEditing" style="padding-right:20px">{{
            caseInfo.desc
          }}</span>
          <el-input
            v-else
            type="textarea"
            ref="descInput"
            placeholder="请输入用例描述"
            v-model="caseInfo.desc"
            maxlength="1000"
            show-word-limit
          ></el-input>
        </div>
        <div class="case-detail-div">
          <el-upload
            class="upload-demo"
            :action="urlForCaseAttachmentUpload"
            :on-success="onAttachmentUploadSuccess"
            :on-error="onAttachmentUploadError"
            :before-upload="beforeAttachmentUpload"
            :file-list="caseAttachmentList"
            :on-remove="onRemoveCaseAttachment"
            :limit="caseAttachmentNumlimit"
            :on-exceed="onAttachmentUploadNumExceed"
            :with-credentials="true"
          >
            <el-button size="small" type="primary">上传附件</el-button>
            <!-- <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div> -->
          </el-upload>
        </div>

        <div
          class="case-detail-div"
          v-if="!caseEditing && currentModule != 'testPlanCaseTable'"
        >
          <el-button size="mini">
            关联缺陷&nbsp;
            <i class="fa fa-link" aria-hidden="true"></i>
          </el-button>
        </div>
      </div>

      <!-- 底部区 -->
      <el-footer>
        <keep-alive>
          <Footer></Footer>
        </keep-alive>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import HeaderBar from "@/views/HeaderBar/HeaderBar";
import Footer from "@/views/Footer/Footer";
import constant from "@/common/constant";

export default {
  data() {
    return {
      planID: 0, // 计划ID
      caseCustomNo: "", // 用例自定义编号
      currentModule: "testPlanCaseDetail", // 当前模块
      caseEditing: false, // 标识是否在编辑测试用例
      caseInfo: {},
      caseStepTableData: [], // 存放测试步骤表数据信息
      caseStepOeration: "viewCaseStep", // 测试用例步骤操作类型 删除步骤deleteCaseStep 新增步骤newCaseStep 编辑步骤editCaseStep
      stepRowData: [], // 存储步骤行数据信息(编辑前的记录信息)
      caseStepRowSelected: [], // 存放用户勾选的记录行数据
      caseStepIDsDeleted: [], // 存放被删除的，且非当前新增的(即从数据库加载出来的)测试用例步骤ID
      tagInputVisible: false, // 控制测试用例标签输入对话框是否可见 false 不可见 true 可见
      tagInputValue: "", // 测试用例标签输入框的值
      urlForCaseAttachmentUpload: constant.urlForCaseAttachmentUpload, // 附件上传地址
      caseAttachmentNumlimit: constant.caseAttachmentNumlimit, // 测试用例附件上传数量限制
      caseAttachmentList: [] // 存放测试用例附件
    };
  },
  components: {
    HeaderBar,

    Footer
  },
  methods: {
    // 编辑用例
    editCase() {
      if (!this.caseEditing) {
        this.caseEditing = true;
      }
    },
    // 取消编辑用例
    cancelCaseEditing() {
      this.$confirm("当前内容没保存，确认取消吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        cancelButtonClass: "btn-custom-cancel"
      })
        .then(() => {
          // 设置对话框全局编辑状态为非编辑状态
          this.caseEditing = false;
        })
        .catch(() => {});
    },
    // 用例基础信息校验
    caseInfoCheck() {
      if (!this.caseInfo.name) {
        this.$message.error("用例名称不能为空");
        return false;
      }
      return true;
    },
    // 保存用例
    saveCase() {
      this.$confirm("确定提交吗?", "提示", {
        type: "info"
      })
        .then(() => {
          if (!this.caseInfoCheck()) {
            return;
          }

          this.caseInfo["suiteType"] = "testPlan";
          // 发送更新用例请求
          this.$api.sprintCaseDialog
            .updateTestCase({
              caseInfo: this.caseInfo,
              caseSteps: this.caseStepTableData,
              attachmentList: this.caseAttachmentList
            })
            .then(res => {
              if (res.success) {
                this.$message({
                  message: res.msg,
                  type: "success"
                });
                // 设置对话框整体编辑状态为false
                this.caseEditing = false;
              } else {
                this.$message.error(res.msg);
              }
            })
            .catch(res => {
              this.$message.error("更新用例失败：" + res.msg || res.message);
            });
        })
        .catch(() => {});
    },
    // 双击测试用例步骤行
    dblclickStepRow(row, column, event) {
      this.editCaseStep(null, row);
    },
    // 点击”编辑“按钮时的事件处理函数
    editCaseStep(index, row) {
      if (!row.editing && this.caseEditing) {
        this.stepRowData = Object.assign({}, row);
        row.editing = true;
        this.caseStepOeration = "editCaseStep";
      }
    },
    // 点击测试步骤"完成"事件处理函数
    finishCaseStepEditing(index, row) {
      if (row.editing) {
        row.editing = false;
      }
    }, // 取消编辑用例步骤
    cancelCaseStepEditing(index, row) {
      if (row.editing) {
        row.editing = false;
      }

      if (this.caseStepOeration == "newCaseStep") {
        // 删除添加的测试用例步骤
        this.caseStepTableData.splice(index, 1);
        // 还原旧值
      } else if (this.caseStepOeration == "editCaseStep") {
        for (let key in row) {
          if (key in this.stepRowData) row[key] = this.stepRowData[key];
        }
      }
    },
    // 新增测试用例步骤公用方法
    // caseStep 测试用例步骤对象
    // index 测试用例步骤插入的位置
    addStep(index, caseStep) {
      this.caseStepOeration = "newCaseStep";

      this.caseStepTableData.splice(index, 0, caseStep);
    },
    // 新增测试用例步骤
    addCaseStep() {
      let caseStep = {
        action: "",
        expection: "",
        editing: true
      };

      this.addStep(this.caseStepTableData.length, caseStep);
    },
    // 插入测试用例步骤
    insertCaseStep(index, row) {
      let caseStep = {
        action: "",
        expection: "",
        editing: true
      };
      this.addStep(index + 1, caseStep);
    },
    // 逐条删除用例步骤
    deleteOneCaseStep(index, row) {
      this.$confirm("确定要删除该步骤吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        cancelButtonClass: "btn-custom-cancel"
      })
        .then(() => {
          this.caseStepTableData.splice(index, 1);

          if (row.id) {
            this.caseStepIDsDeleted.push(row.id);
          }
        })
        .catch(() => {});
    },
    // 勾选记录行发生改变时事件处理函数
    onSelectChange(selection) {
      this.caseStepRowSelected = selection;
    },
    // 批量删除用例步骤
    deleteCaseStepsInBatch() {
      this.$confirm("确定要删除选中步骤吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        cancelButtonClass: "btn-custom-cancel"
      })
        .then(() => {
          if (!this.caseStepRowSelected.length) {
            this.$alert("未选择步骤，请勾选至少一条步骤", "提示", {
              confirmButtonText: "确定"
            });
            return;
          }

          for (let i = 0; i < this.caseStepRowSelected.length; i++) {
            for (let x = 0; x < this.caseStepTableData.length; x++) {
              if (this.caseStepTableData[x] == this.caseStepRowSelected[i]) {
                this.caseStepTableData.splice(x, 1);
                if (this.caseStepRowSelected[i].id) {
                  this.caseStepIDsDeleted.push(this.caseStepRowSelected[i].id);
                }
              }
            }
          }
        })
        .catch(() => {});
    },
    // 删除tag
    onCloseTag(tag) {
      this.caseInfo.tags.splice(this.caseInfo.tags.indexOf(tag), 1);
    },
    // 点击按钮时加载tag输入框
    showTagInput() {
      this.tagInputVisible = true;
      this.$nextTick(_ => {
        this.$refs.saveTagInput.$refs.input.focus();
      });
    },
    // tag输入框失去焦点、或者未失去焦点的情况下，回车键事件处理函数
    handleTagInputConfirm() {
      let tagInputValue = this.tagInputValue;
      // 输入标签不为空，且不存在当前tags中才可以添加
      if (tagInputValue && this.caseInfo.tags.indexOf(tagInputValue) == -1) {
        this.caseInfo.tags.push(tagInputValue);
      }
      this.tagInputVisible = false;
      this.tagInputValue = "";
    },
    // 附件上传前的处理
    beforeAttachmentUpload(file) {
      if (!file.size) {
        // file.size默认字节为单位
        this.$message({
          message: "待上传附件内容为空，请重新选择文件",
          type: "warning"
        });
        return false;
      }
      return true;
    },
    // 附件上传成功时的事件处理函数
    onAttachmentUploadSuccess(response, file, fileList) {
      for (let i = 0; i < fileList.length; i++) {
        if (fileList[i].uid == file.uid) {
          fileList.splice(i, 1);
          break;
        }
      }

      if (response.success) {
        this.$message({
          message: response.msg,
          type: "success"
        });
        this.caseAttachmentList.push(response.data);
        // 上传成功后，让对话框进入编辑状态，因为对附件的管理操作，必须点击 保存 按钮才生效
        if (!this.caseEditing) {
          this.caseEditing = true;
        }
      } else {
        this.caseAttachmentList = fileList;
        this.$message.error(response.msg);
      }
    },
    // 附件上传失败时的事件处理函数
    onAttachmentUploadError(err, file, fileList) {
      this.$message.error("上传附件失败");
      console.log(err);
    },
    // 附件上传数量超过限制时的事件处理函数
    onAttachmentUploadNumExceed(files, fileList) {
      this.$message.error(
        "上传附件失败，最多只能上传" + this.caseAttachmentNumlimit + "个附件"
      );
    },
    // 移除附件时事件处理函数
    onRemoveCaseAttachment(file, fileList) {
      this.caseAttachmentList = fileList;

      if (!this.caseEditing) {
        // 删除列表附件时，进入编辑状态，因为对附件的管理操作，必须点击 保存 按钮才生效
        this.caseEditing = true;
      }
    }
  },
  created() {
    // 获取计划ID和用例自定义编号url参数信息
    if (JSON.stringify(this.$route.query) == "{}") {
      this.$message({
        message: "程序错误，获取url参数信息失败",
        type: "error"
      });
      return;
    } else {
      this.planID = this.$route.query.planID;
      this.caseCustomNo = this.$route.query.caseCustomNo;

      if (!this.planID) {
        this.$message({
          message: "程序错误，获取的url参数(planID)为空",
          type: "error"
        });
        return;
      }

      if (!this.caseCustomNo) {
        this.$message({
          message: "程序错误，获取的url参数(caseCustomNo)为空",
          type: "error"
        });
        return;
      }
    }

    // 发送获取测试用例详情信息
    this.$api.testPlanBugTable
      .getPlanRelatedCase({
        planID: this.planID,
        caseCustomNo: this.caseCustomNo
      })
      .then(res => {
        if (res.success) {
          this.caseInfo = res.data;
        } else {
          this.$message.error(res.msg);
        }
      })
      .catch(res => {
        this.$message.error("获取用例信息失败" + res.msg || res.message);
      });
  }
};
</script>

<style scoped>
.testplan-case-detail-content-div {
  position: absolute;
  top: 0px;
  left: 0px;
  right: 0px;
  bottom: 0px;
  overflow: hidden;
}

.plan-case-detail-content {
  margin: 10px 10px 10px 10px;
  position: absolute;
  top: 60px;
  left: 0px;
  right: 0px;
  bottom: 40px;
  overflow-y: auto;
}

.case-detail-div {
  border-style: solid;
  border-width: 1px;
  border-style: solid;
  background: rgba(241, 239, 239, 0.438);
  border-color: rgb(204, 206, 206);
  margin: 5px 0px 5px 0px;
  padding: 10px 0px 10px 0px;
}

/* 测试用例步骤表 */
.case-step-table {
  overflow: "auto";
}

/* 测试用例标签 */
.el-tag {
  margin-right: 10px;
}

/* 新增测试用例标签按钮 */
.button-new-tag {
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}

/* 测试用例标签编辑输入框 */
.input-new-tag {
  width: 90px;
  vertical-align: bottom;
}
</style>
