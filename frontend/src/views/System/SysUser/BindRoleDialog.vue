<template>
    <div>
        <el-dialog
            title="分配角色"
            :visible="dialogVisible"
            :append-to-body="true"
            :width="dialogWidth"
            :show-close="showClose"
            :close-on-click-modal="closeOnClickModal"
            :close-on-press-escape="closeOnPressEscape"
        >
            <div class="my-dialog-body">
                <el-form
                    :label-width="dialogFormLabeWidth"
                >
                    <el-form-item label="阶段名称" >
                        <el-select
                            v-model="rolesSelected"
                            value-key="id"
                            multiple
                            filterable
                            clearable
                            size="medium"
                            placeholder="请选择角色"
                        >
                            <el-option
                                v-for="item in roleOptions"
                                :key="item.id"
                                :label="item.name"
                                :value="item"
                            ></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item class="dialog-footer-form-item">
                        <div class="my-dialog-footer">
                            <el-button @click="closeDialog">取消</el-button>
                            <el-button type="primary" @click="save">保存</el-button>
                        </div>
                    </el-form-item>
                </el-form>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import { elDialogMixin } from "@/common/mixins/elDialogMixin";

export default {
    props: ["dialogVisible", "row"],
    mixins: [elDialogMixin],
    data() {
        return {
            roleOptions: [], // role下拉选项
            rolesSelected: [], // 选取的role
        };
    },
    methods: {
        save() {
            const len = this.rolesSelected.length;
            if (!len) {
                // 未选择role
                return;
            }
            let roleIds = [];
            for (let i = 0; i < len; i++) {
                roleIds.push(this.rolesSelected[i].id);
            }
            this.$api.sysUser
                .bindRoles({
                    userId: this.row.id,
                    roleIds: roleIds,
                })
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);

                        // 更新列表数据
                        // this.row.roles = this.row.roles.concat(this.rolesSelected); // 如果添加了重复的角色，前端会报错，key重复

                        for (let i = 0; i < this.rolesSelected.length; i++) {
                            var roleExists = this.row.roles.some((item) => {
                                if (item.id == this.rolesSelected[i].id) {
                                    return true;
                                }
                            });

                            if (!roleExists) {
                                this.row.roles.push(this.rolesSelected[i]);
                            }
                        }
                        this.closeDialog();
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },

        // 获取用户未关联的角色
        getUnRelatedRoles() {
            this.$api.sysUser
                .getUnRelatedRoles({
                    userId: this.row.id,
                })
                .then((res) => {
                    if (res.success) {
                        this.roleOptions = res.data;
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
    },
    created() {
        this.getUnRelatedRoles();
    },
};
</script>

<style scoped lang="scss">
</style>
