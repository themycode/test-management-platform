<template>
    <el-dialog
        title="关联菜单"
        width="60%"
        :visible="dialogVisible"
        :show-close="true"
        :close-on-click-modal="false"
        :close-on-press-escape="true"
        @close="onCloseDialog"
    >
        <div class="my-dialog-body" v-loading="menuBinding" element-loading-text="正在绑定">
            <sys-menu-tree
                ref="tree"
                class="sys-menu-tree"
                :relatedMenus.sync="relatedMenus"
                :roleID="roleID"
            ></sys-menu-tree>
        </div>
        <div class="dialog-footer">
            <el-button @click="closeDialog" size="small">关闭</el-button>
            <el-button type="primary" @click="bindMenu" size="small">保存</el-button>
        </div>
    </el-dialog>
</template>

<script>
import SysMenuTree from "./SysMenuTree";
import { elDialogMixin } from "@/common/mixins/elDialogMixin";

export default {
    props: ["dialogVisible", "roleID"],
    components: {
        SysMenuTree,
    },
    mixins: [elDialogMixin],

    data() {
        return {
            menuBinding: false, // 标识是否正在执行资源绑定//防极短时间内重复点击用
            relatedMenus: [], // 默认勾选的，即已绑定菜单ID的数组
        };
    },
    methods: {
        bindMenu() {
            try {
                this.menuBinding = true;

                let checkedNodes = this.$refs.tree.$refs.sysMenuTree.getCheckedNodes(
                    false,
                    true
                );
                let checkedNodeIDs = [];
                for (let i = 0; i < checkedNodes.length; i++) {
                    checkedNodeIDs.push(checkedNodes[i].id);
                }
                this.relatedMenus = checkedNodeIDs;

                this.$api.sysRole
                    .bindMenu({
                        roleId: this.roleID,
                        relatedMenus: this.relatedMenus,
                    })
                    .then((res) => {
                        if (res.success) {
                            this.$message({
                                message: res.msg,
                                type: "success",
                            });
                        } else {
                            this.$message.error(res.msg);
                        }
                        this.menuBinding = false;
                    })
                    .catch((res) => {
                        this.$message.error(res.msg || res.message);
                        this.menuBinding = false;
                    });
            } catch (error) {
                this.$message.error(error.message);
                this.menuBinding = false;
            }
        },
    },
};
</script>

<style lang="scss" scoped>
.sys-menu-tree {
    position: absolute;
    font-size: 14px;
    padding: 0px;
    width: 100%;
    top: 0px;
    bottom: 0px;
    overflow: auto;

    background: rgba(241, 239, 239, 0.4);
}

.my-dialog-body {
    height: 600px;
    padding-left: 0px;
    background: none;
}

.dialog-footer {
    text-align: center;
    position: relative;
}
</style>
