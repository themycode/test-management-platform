<template>
    <div class="view-wrapper">
        <div class="common-top-bar-wrapper">
            <span class="span-font">产品</span>
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

        <sprint-table :productID="productSelected" v-if="showSprintTable" class="sprint-table"></sprint-table>
    </div>
</template>

<script>
import SprintTable from "./Sprint/SprintTable";

export default {
    data() {
        return {
            products: [], // 产品选取框下拉列表
            productSelected: "", // 存放用户选取的产品（productID）
            showSprintTable: false // 是否展示迭代数据表
        };
    },
    components: {
        SprintTable
    },
    methods: {
        getProductsDetails() {
            this.productSelected = "";
            // 请求产品列表
            this.$api.product
                .getProductsDetails()
                .then(res => {
                    if (res.success) {
                        this.products = res.data;
                        let productId = localStorage.getItem(
                            "productIdForSprint"
                        );
                        if (productId) {
                            productId = parseInt(productId);
                            let result = this.products.some(item => {
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
                            "productIdForSprint",
                            this.productSelected
                        );
                    } else {
                        this.$message.error(res.msg);
                        localStorage.setItem("productIdForSprint", "");
                    }
                    this.showSprintTable = false;
                    this.$nextTick(() => {
                        this.showSprintTable = true;
                    });
                })
                .catch(res => {
                    localStorage.setItem("productIdForSprint", "");
                    this.$message.error(res.msg || res.message);
                    this.showSprintTable = false;
                    this.$nextTick(() => {
                        this.showSprintTable = true;
                    });
                });
        },
        onProductChange(value) {
            if (!value) {
                this.productSelected = "";
            }

            localStorage.setItem("productIdForSprint", this.productSelected);
            this.showSprintTable = false;
            this.$nextTick(() => {
                this.showSprintTable = true;
            });
        }
    },
    created() {
        this.getProductsDetails();
    }
};
</script>

<style scoped lang="scss">
.sprint-table {
    top: 43px;
}
</style>
