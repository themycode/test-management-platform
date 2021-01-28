<template>
  <div class="view-wrapper">
    <!--项目选择面板-->
    <div class="common-top-bar-wrapper">
      <span class="span-font">项目名称</span>
      <el-select
        v-model="projectSelected"
        filterable
        clearable
        value-key="id"
        size="small"
        placeholder="输入搜索关键词"
        @change="onProjectChange"
      >
        <el-option
          v-for="item in projects"
          :key="item.id"
          :label="item.name"
          :value="item"
        ></el-option>
      </el-select>
    </div>

    <!-- 项目版本表 -->
    <project-version-table
      :project="projectSelected"
      v-if="showProjectVersionTable"
      class="project-version-table"
    ></project-version-table>
  </div>
</template>

<script>
import ProjectVersionTable from "./ProjectVersion/ProjectVersionTable";

export default {
  data() {
    return {
      projects: [], // 项目选取框下拉列表
      projectSelected: "", // 存放用户选取的项目
      showProjectVersionTable: true
    };
  },
  components: {
    ProjectVersionTable
  },

  methods: {
    onProjectChange(value) {
      let tempValue = "";
      if (!value) {
        this.projectSelected = "";
      } else {
        tempValue = JSON.stringify(this.projectSelected);
      }
      sessionStorage.setItem("projectForVersionPage", tempValue);
      this.showProjectVersionTable = false;
      this.$nextTick(() => {
        this.showProjectVersionTable = true;
      });
    }
  },
  created() {
    // 请求项目列表
    this.$api.project
      .getProjectsDetails({ fields: "id,name,product_id" })
      .then(res => {
        if (res.success) {
          this.projects = res.data;

          if (this.projects.length) {
            let projectSelected = sessionStorage.getItem(
              "projectForVersionPage"
            );
            if (projectSelected) {
              projectSelected = JSON.parse(projectSelected);
              var result = this.projects.some(item => {
                if (item.id == projectSelected.id) {
                  return true;
                }
              });
              if (result) {
                this.projectSelected = projectSelected;
              } else {
                this.projectSelected = "";
                sessionStorage.setItem(
                  "projectForVersionPage",
                  this.projectSelected
                );
              }
            } else {
              this.projectSelected = this.projects[0];
              sessionStorage.setItem(
                "projectForVersionPage",
                JSON.stringify(this.projectSelected)
              );
            }
            this.showProjectVersionTable = false;
            this.$nextTick(() => {
              this.showProjectVersionTable = true;
            });
          } else {
            this.projectSelected = "";
          }
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

<style scoped lang="scss">
.project-version-table {
    top: 43px;
}
</style>
