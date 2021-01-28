<template>
  <div>
    <!-- 遗留缺陷 -->
    <el-table
      :data="
        unclosedDefects.slice(
          (currentPage - 1) * pageSize,
          currentPage * pageSize
        )
      "
      border
      stripe
      highlight-current-row
    >
      <el-table-column
        prop="defectId"
        label="缺陷ID"
        min-width="8%"
        header-align="center"
        align="center"
        show-overflow-tooltip
      >
        <template slot-scope="scope"
          ><el-link v-if="scope.row.platform=='jira'"
            target="_blank"
            type="primary"
            :href="$appConfig.jiraIssueBrowseBaseUrl + scope.row.defectId"
            >{{ scope.row.defectId }}</el-link
          >
          <el-link v-else-if="scope.row.platform=='禅道'"
            target="_blank"
            type="primary"
            :href="$appConfig.zentaoBugBrowseBaseUrl + scope.row.defectId + '.html'"
            >{{ scope.row.defectId }}</el-link
          >          
        </template>
      </el-table-column>
      <el-table-column
        prop="title"
        label="缺陷名称"
        min-width="45%"
        show-overflow-tooltip
        header-align="center"
        align="left"
      >
        <template slot-scope="scope">{{
          convertEntityToString(scope.row.title)
        }}</template>
      </el-table-column>
      <el-table-column
        prop="severity"
        min-width="5%"
        label="严重级别"
        header-align="center"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="status"
        label="状态"
        min-width="5%"
        header-align="center"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="remark"
        label="补充说明"
        min-width="11%"
        header-align="center"
        align="left"
      ></el-table-column>
      <el-table-column
        prop="creater"
        label="提交人"
        min-width="5%"
        header-align="center"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="assignedTo"
        label="指派给"
        min-width="5%"
        header-align="center"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="personLiable"
        label="责任人"
        min-width="5%"
        header-align="center"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="resolver"
        label="处理人"
        min-width="5%"
        header-align="center"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="platform"
        label="所属平台"
        min-width="5%"
        header-align="center"
        align="center"
      ></el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      layout="total, sizes, prev, pager, next"
      :hide-on-single-page="false"
      :total="totalRows"
      prev-text="上一页"
      next-text="下一页"
      :current-page="currentPage"
      :page-sizes="pageSizes"
      :page-size="pageSize"
    ></el-pagination>
  </div>
</template>

<script>
export default {
  props: ["unclosedDefects"],
  data() {
    return {
      totalRows: this.unclosedDefects.length, // 查询获取的表格记录行总数
      pageSizes: [10, 20, 30, 40, 50, 100, 150], //每页显示记录数选择器的选项设置
      pageSize: 10, // 表格默认每页显示的记录数
      currentPage: 1 // 当前页页码
    };
  },

  methods: {
    // 切换表格页面大小
    handleSizeChange(pageSize) {
      this.currentPage = 1;
      this.pageSize = pageSize;
    },
    // 翻页
    handleCurrentChange(currentPage) {
      this.currentPage = currentPage;
    },
    // 转换字符串中的实体为html字符
    convertEntityToString(str) {
      var entitys = {
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&quot;": '"',
        "&apos;": "'"
      };
      for (let key in entitys) {
        str = str.replace(new RegExp(key, "gm"), entitys[key]);
      }
      return str;
    }
  }
};
</script>
