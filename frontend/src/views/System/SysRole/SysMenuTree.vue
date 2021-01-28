<template>
        <el-tree
            ref="sysMenuTree"
            empty-text="emptyText"
            :data="treeData"
            :props="defaultProps"
            :expand-on-click-node="false"
            show-checkbox
            node-key="id"
            default-expand-all
            check-strictly
        ></el-tree>
</template>

<script>

export default {
    props: ["roleID", "relatedMenus"],

    data() {
        return { defaultProps: {
        label: "name",
        children: "children",
        isLeaf: "isLeaf" // 是否叶子节点
      },
      treeData: [], // 存放树结点数据
      emptyText: "未获取到数据，请重新打开或刷新页面重试",};
    },
    created() {
        // 请求菜单
        this.$api.sysMenu
            .getSysMenuTree({ parentId: -1, recursive: true })
            .then((res) => {
                if (res.success) {
                    this.treeData = res.data;

                    // 请求角色关联的菜单ID
                    this.$api.sysRole
                        .getRoleRelatedMenus({ roleId: this.roleID })
                        .then((res) => {
                            if (res.success) {
                                this.$emit("update:relatedMenus", res.data);

                                // 设置默认选中的节点
                                for (let i = 0; i < res.data.length; i++) {
                                    this.$refs.sysMenuTree.setChecked(
                                        res.data[i],
                                        true,
                                        false
                                    );
                                }
                            } else {
                                this.$message.error(res.msg);
                            }
                        })
                        .catch((res) => {
                            this.$message.error(res.msg || res.message);
                        });
                } else {
                    this.$message.error(res.msg);
                }
            })
            .catch((res) => {
                this.$message.error(res.msg || res.message);
            });
    },
};
</script>

<style lang="scss" scoped>
</style>
