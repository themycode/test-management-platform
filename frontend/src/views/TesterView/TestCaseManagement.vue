<template>
    <div class="view-wrapper">
        <div class="common-top-bar-wrapper">
            <span>产品</span>
            <el-select
                v-model="productSelected"
                filterable
                size="small"
                placeholder="输入搜索关键词"
                @change="onProductChange"
            >
                <el-option
                    v-for="item in products"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                ></el-option> </el-select
            >&nbsp;
            <span>迭代</span>
            <el-select
                v-model="sprintSelected"
                filterable
                clearable
                size="small"
                placeholder="输入搜索关键词"
                @clear="onClearSprintSelected"
                @change="onSprintChange"
            >
                <el-option
                    v-for="item in sprints"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                ></el-option>
            </el-select>
        </div>

        <!-- 产品测试用例套件 -->
        <sprint-case-suite-tree
            v-if="showSprintCaseSuiteTree"
            :sprintID="sprintSelected"
            :productID="productSelected"
            :currentModule="currentModule"
            class="sprint-case-suite-tree"
            ref="leftElement"
        ></sprint-case-suite-tree>

        <!-- 迭代测试用例列表(包含操作按钮及表单查询组件) -->
        <sprint-case-table
            class="sprint-case-table"
            :sprintID="sprintSelected"
            :productID="productSelected"
            :currentModule="currentModule"
            ref="rightElement"
        ></sprint-case-table>
    </div>
</template>

<script>
import SprintCaseSuiteTree from "./SprintCase/SprintCaseSuiteTree";
import SprintCaseTable from "./SprintCase/SprintCaseTable";
import { horizontalDragMixin } from "@/common/mixins/horizontalDragMixin";

export default {
    mixins: [horizontalDragMixin],
    data() {
        return {
            products: [], // 产品选取框下拉列表
            productSelected: "", // 存放用户选取的产品（productID）
            sprints: [], // sprint版本选取框下拉列表
            sprintSelected: "", // 存放用户选取的sprint（sprintID）
            showSprintCaseSuiteTree: true, // 是否展示sprintCaseSuiteTree组件
            currentModule: "testCaseManagement", //用于标识测试当前在哪个页面模块操作用例集树&测试用例表组件
        };
    },
    components: {
        SprintCaseSuiteTree,
        SprintCaseTable,
    },

    methods: {
        getProductsDetails() {
            this.productSelected = "";
            this.sprintSelected = "";
            this.sprints = [];
            // 请求产品列表
            this.$api.product
                .getProductsDetails()
                .then((res) => {
                    if (res.success) {
                        this.products = res.data;
                        let productId = localStorage.getItem(
                            "productIdForTCMg"
                        );
                        if (productId) {
                            productId = parseInt(productId);
                            let result = this.products.some((item) => {
                                if (item.id == productId) {
                                    return true;
                                }
                            });
                            if (result) {
                                this.productSelected = productId;
                            } else {
                                if (this.products.length) {
                                    this.productSelected = this.products[0].id;
                                }
                            }
                        } else {
                            if (this.products.length) {
                                this.productSelected = this.products[0].id;
                            }
                        }
                        localStorage.setItem(
                            "productIdForTCMg",
                            this.productSelected
                        );

                        if (this.productSelected) {
                            this.getSprintsDetails();
                        }
                    } else {
                        localStorage.setItem(
                            "productIdForTCMg",
                            this.productSelected
                        );
                        this.$message.error(res.msg);

                        this.$store.commit(
                            "updateSprintID",
                            this.sprintSelected
                        );
                        this.showSprintCaseSuiteTree = false;
                        this.$nextTick(() => {
                            this.showSprintCaseSuiteTree = true;
                        });
                    }
                })
                .catch((res) => {
                    localStorage.setItem("productIdForTCMg", "");
                    this.$message.error(res.msg || res.message);
                    this.$store.commit("updateSprintID", this.sprintSelected);
                    this.showSprintCaseSuiteTree = false;
                    this.$nextTick(() => {
                        this.resetRightElmentLeftPost();
                        this.showSprintCaseSuiteTree = true;
                    });
                });
        },
        resetRightElmentLeftPost() {
            this.$refs.rightElement.$el.style.left = "322px"; // 重置表格边界
        },
        getSprintsDetails() {
            this.sprintSelected = "";
            this.sprints = [];
            this.$api.product
                .getProductSprintsDetails({
                    productId: this.productSelected,
                })
                .then((res) => {
                    if (res.success) {
                        this.sprints = res.data;
                        let sprintId = localStorage.getItem("sprintIdForTCMg");
                        if (sprintId) {
                            sprintId = parseInt(sprintId);
                            let result = this.sprints.some((item) => {
                                if (item.id == sprintId) {
                                    return true;
                                }
                            });
                            if (result) {
                                this.sprintSelected = sprintId;
                            } else {
                                if (this.sprints.length) {
                                    this.sprintSelected = this.sprints[0].id;
                                }
                            }
                        } else {
                            if (this.sprints.length) {
                                this.sprintSelected = this.sprints[0].id;
                            }
                        }

                        localStorage.setItem(
                            "sprintIdForTCMg",
                            this.sprintSelected
                        );
                    } else {
                        this.$message.error(res.msg);
                    }

                    this.$store.commit("updateSprintID", this.sprintSelected);

                    // 重新加载树节点
                    this.showSprintCaseSuiteTree = false;
                    this.$nextTick(() => {
                        this.resetRightElmentLeftPost();
                        this.showSprintCaseSuiteTree = true;
                    });
                })
                .catch((res) => {
                    this.$store.commit("updateSprintID", this.sprintSelected);
                    localStorage.setItem(
                        "sprintIdForTCMg",
                        this.sprintSelected
                    );
                    this.$message.error(res.msg || res.message);
                    // 重新加载树节点
                    this.showSprintCaseSuiteTree = false;
                    this.$nextTick(() => {
                        this.resetRightElmentLeftPost();
                        this.showSprintCaseSuiteTree = true;
                    });
                });
        },
        onProductChange(value) {
            if (!value) {
                this.productSelected = "";
            }

            localStorage.setItem("productIdForTCMg", this.productSelected);
            this.getSprintsDetails();
        },
        onSprintChange(value) {
            if (!value) {
                this.sprintSelected = "";
            }

            this.$store.commit("updateSprintID", this.sprintSelected);
            localStorage.setItem("sprintIdForTCMg", this.sprintSelected);

            // 重新加载树节点
            this.showSprintCaseSuiteTree = false;
            this.$nextTick(() => {
                this.resetRightElmentLeftPost();
                this.showSprintCaseSuiteTree = true;
            });
        },
        onClearSprintSelected() {
            this.$store.commit("updateSprintID", "");
            localStorage.setItem("sprintIdForTCMg", "");
        },
    },
    created() {
        this.getProductsDetails();
    },
    mounted() {
        document.body.addEventListener("mousedown", this.mousedown, false);
        document.body.addEventListener("mousemove", this.mousemove, false);
        document.body.addEventListener("mouseup", this.mouseup, false);
    },
    beforeDestroy() {
        document.body.removeEventListener("mousedown", this.mousedown);
        document.body.removeEventListener("mousemove", this.mousemove);
        document.body.removeEventListener("mouseup", this.mouseup);
    },
};
</script>

<style scoped lang="scss">
// 测试集树样式
.sprint-case-suite-tree {
    position: absolute;
    top: 47px; // 顶部筛选栏占用高度42 + 5px
    bottom: 0px;
    padding: 0px;
    width: 320px;
    margin-right: 2px;
    border-right: solid;
    border-right-color: rgba(172, 167, 167, 1);
    border-right-width: 1px;
}

// 测试用例表样式
.sprint-case-table {
    position: absolute;
    left: 322px; // 左侧套件树占用宽度
    right: 0px;
    top: 47px;
    bottom: 0px;
    border-left: solid;
    border-left-color: rgba(172, 167, 167, 1);
    border-left-width: 1px;
}
</style>
