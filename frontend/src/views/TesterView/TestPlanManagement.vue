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
                ></el-option>
            </el-select>
        </div>

        <sprint-test-plan-table
            :productID="productSelected"
            v-if="showTestPlanTable"
            class="sprint-test-plan-table"
        ></sprint-test-plan-table>
    </div>
</template>

<script>
import SprintTestPlanTable from "./SprintTestPlan/SprintTestPlanTable";

export default {
    data() {
        return {
            products: [], // 产品选取框下拉列表
            productSelected: "", // 存放用户选取的产品（productID）
            showTestPlanTable: false, // 是否展示测试计划表
        };
    },
    components: {
        SprintTestPlanTable,
    },

    methods: {
        getProductsDetails() {
            // 请求产品列表
            this.$api.product
                .getProductsDetails()
                .then((res) => {
                    if (res.success) {
                        this.products = res.data;
                        let productId = localStorage.getItem("productIdForTP");
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
                                } else {
                                    this.productSelected = "";
                                }
                            }
                        } else {
                            if (this.products.length) {
                                this.productSelected = this.products[0].id;
                            } else {
                                this.productSelected = "";
                            }
                        }
                        localStorage.setItem(
                            "productIdForTP",
                            this.productSelected
                        );
                    } else {
                        this.productSelected = "";
                        localStorage.setItem("productIdForTP", "");
                        this.$message.error(res.msg);
                    }
                    this.showTestPlanTable = false;
                    this.$nextTick(() => {
                        this.showTestPlanTable = true;
                    });
                })
                .catch((res) => {
                    this.productSelected = "";
                    localStorage.setItem("productIdForTP", "");
                    this.$message.error(res.msg || res.message);

                    this.showTestPlanTable = false;
                    this.$nextTick(() => {
                        this.showTestPlanTable = true;
                    });
                });
        },
        onProductChange(value) {
            if (!value) {
                this.productSelected = "";
            }

            localStorage.setItem("productIdForTP", this.productSelected);
            // 重新加载测试计划表
            this.showTestPlanTable = false;
            this.$nextTick(() => {
                this.showTestPlanTable = true;
            });
        },
    },
    created() {
        this.getProductsDetails();
    },
};
</script>

<style scoped lang="scss">
.sprint-test-plan-table {
    top: 43px;
}
</style>
