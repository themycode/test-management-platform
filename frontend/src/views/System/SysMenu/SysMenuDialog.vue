<template>
    <el-dialog
        :title="dialogTitle"
        width="50%"
        :visible="dialogVisible"
        :show-close="showClose"
        :close-on-click-modal="closeOnClickModal"
        :close-on-press-escape="closeOnPressEscape"
        @close="onCloseDialog"
    >
        <div class="my-dialog-body">
            <el-form
                :model="dialogForm"
                :rules="rules"
                ref="dialogForm"
                :label-width="dialogFormLabeWidth"
            >
                <el-form-item label="资源类型" prop="type">
                    <el-radio-group v-model="dialogForm.type">
                        <el-radio
                            v-for="item in typeOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="资源名称" prop="name">
                    <el-input v-model="dialogForm.name"></el-input>
                </el-form-item>
                <el-form-item label="资源描述" prop="desc">
                    <el-input v-model="dialogForm.desc" type="textarea"></el-input>
                </el-form-item>

                <el-form-item
                    label="资源URL"
                    prop="url"
                    v-if="(dialogForm.type == '菜单') | (dialogForm.type == '按钮')"
                >
                    <el-input v-model="dialogForm.url"></el-input>
                </el-form-item>
                <el-form-item label="资源图标" prop="icon">
                    <el-input v-model="dialogForm.icon"></el-input>
                </el-form-item>
                <el-form-item label="权限标识" prop="perms">
                    <el-input v-model="dialogForm.perms"></el-input>
                </el-form-item>
                <el-form-item label="登录验证" prop="requireAuth">
                    <el-radio-group v-model="dialogForm.requireAuth">
                        <el-radio
                            v-for="item in requireAuthOptions"
                            :key="item.value"
                            :label="item.value"
                        >{{ item.label }}</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="前端是否显示" prop="show" v-if="dialogForm.type != '按钮'">
                    <el-radio-group v-model="dialogForm.show">
                        <el-radio
                            v-for="item in showOptions"
                            :key="item.value"
                            :label="item.value"
                        >{{ item.label }}</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="未登录是否显示" prop="showWithoutAuth" v-if="dialogForm.type != '按钮'">
                    <el-radio-group v-model="dialogForm.showWithoutAuth">
                        <el-radio
                            v-for="item in showOptions"
                            :key="item.value"
                            :label="item.value"
                        >{{ item.label }}</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="是否折叠" prop="collapsed" v-if="dialogForm.type != '按钮'">
                    <el-radio-group v-model="dialogForm.collapsed">
                        <el-radio
                            v-for="item in collapsedOptions"
                            :key="item.value"
                            :label="item.value"
                        >{{ item.label }}</el-radio>
                    </el-radio-group>
                </el-form-item>
                <!--仅修改时提供输入排序-->
                <el-form-item label="排序" prop="order" v-if="dialogForm.id">
                    <el-input v-model="dialogForm.order"></el-input>
                </el-form-item>
                <el-form-item class="dialog-footer-form-item">
                    <div class="my-dialog-footer">
                        <el-button @click="closeDialog">取消</el-button>
                        <el-button type="primary" @click="save('dialogForm')">保存</el-button>
                    </div>
                </el-form-item>
            </el-form>
        </div>
    </el-dialog>
</template>

<script>
import { elDialogMixin } from "@/common/mixins/elDialogMixin";

export default {
    props: ["dialogVisible", "dialogTitle", "dialogFormData", "menuNode"],
    mixins: [elDialogMixin],

    data() {
        return {
            dialogFormLabeWidth:'130px',
            dialogForm: Object.assign({}, this.dialogFormData),
            // 资源类型
            typeOptions: [
                { label: "菜单", value: "菜单" },
                { label: "目录", value: "目录" },
                { label: "按钮", value: "按钮" },
            ],
            requireAuthOptions: [
                { label: "登录后才可访问", value: true },
                { label: "不需要登录也可以访问", value: false },
            ],
            showOptions: [
                { label: "显示", value: true },
                { label: "隐藏", value: false },
            ],
            collapsedOptions: [
                { label: "是", value: true },
                { label: "否", value: false },
            ],

            rules: {
                type: [
                    {
                        required: true,
                        message: "请选择资源类型",
                        trigger: "blur",
                    },
                ],
                name: [
                    {
                        required: true,
                        message: "请输入资源名称",
                        trigger: "blur",
                    },
                    {
                        min: 1,
                        max: 50,
                        message: "长度在 1 到 50 个字符",
                        trigger: "blur",
                    },
                ],
                desc: [
                    {
                        min: 0,
                        max: 300,
                        message: "资源描述不能超过 300 个字符",
                        trigger: "blur",
                    },
                ],
                url: [
                    {
                        min: 0,
                        max: 100,
                        message: "资源url不能超过 100 个字符",
                        trigger: "blur",
                    },
                ],
                icon: [
                    {
                        min: 0,
                        max: 30,
                        message: "资源图标不能超过 30 个字符",
                        trigger: "blur",
                    },
                ],
                perms: [
                    {
                        min: 0,
                        max: 50,
                        message: "权限标识不能超过 50 个字符",
                        trigger: "blur",
                    },
                ],
                requireAuth: [
                    {
                        required: true,
                        message: "请选择是否登录验证",
                        trigger: "blur",
                    },
                ],
                show: [
                    {
                        required: true,
                        message: "请选择前端是否显示",
                        trigger: "blur",
                    },
                ],
                showWithoutAuth: [
                    {
                        required: true,
                        message: "请选择未登录是否显示",
                        trigger: "blur",
                    },
                ],
                collapsed: [
                    {
                        required: true,
                        message: "请选择是否折叠",
                        trigger: "blur",
                    },
                ],
            },
        };
    },
    methods: {
        add() {
            const isLeafByUser = this.menuNode.isLeafByUser;
            this.menuNode.isLeafByUser = false; // 先设置当前节点为非叶子节点，否则无法添加子节点

            if (!this.menuNode.expanded) {
                // 如果节点未展开，说明还未加载其子节点，先加载子节点
                this.$api.sysMenu
                    .getSysMenuTree({
                        parentId: this.menuNode.data.id,
                        recursive: false,
                    })
                    .then((res) => {
                        if (res.success) {
                            // 先清空子节点
                            if (!this.menuNode.childNodes) {
                                this.$set(this.menuNode, "childNodes", []);
                            }
                            this.$parent.$refs.sysMenuTree.updateKeyChildren(
                                this.menuNode.data.id,
                                res.data
                            );

                            // 展开节点
                            if (!this.menuNode.expanded) {
                                this.menuNode.expanded = true;
                            }

                            //  添加子节点
                            this.$api.sysMenu
                                .addSysMenu(this.dialogForm)
                                .then((res) => {
                                    if (res.success) {
                                        let length = this.menuNode.childNodes
                                            .length;
                                        if (length) {
                                            // 如果存在子节点，则在最后一个节点之后插入新节点
                                            this.$parent.$refs.sysMenuTree.insertAfter(
                                                res.data,
                                                this.menuNode.childNodes[
                                                    length - 1
                                                ]
                                            );
                                        } else {
                                            // 否则，追加节点
                                            this.$parent.$refs.sysMenuTree.append(
                                                res.data,
                                                this.menuNode
                                            );
                                        }
                                        this.closeDialog();
                                        this.$message({
                                            message: res.msg,
                                            type: "success",
                                        });
                                    } else {
                                        // 新增失败
                                        if (isLeafByUser) {
                                            // 如果被点击节点为叶子节点，则还原为叶子节点
                                            this.menuNode.isLeafByUser = true;
                                        }
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
            } else {
                this.$api.sysMenu
                    .addSysMenu(this.dialogForm)
                    .then((res) => {
                        if (res.success) {
                            let length = this.menuNode.childNodes.length;
                            if (length) {
                                this.$parent.$refs.sysMenuTree.insertAfter(
                                    res.data,
                                    this.menuNode.childNodes[length - 1]
                                );
                            } else {
                                this.$parent.$refs.sysMenuTree.append(
                                    res.data,
                                    this.menuNode
                                );
                            }
                            this.closeDialog();
                            this.$message({
                                message: res.msg,
                                type: "success",
                            });
                        } else {
                            // 新增失败
                            if (isLeafByUser) {
                                // 如果被点击节点为叶子节点，则还原为叶子节点
                                this.menuNode.isLeafByUser = true;
                            }
                            this.$message.error(res.msg);
                        }
                    })
                    .catch((res) => {
                        this.$message.error(res.msg || res.message);
                    });
            }
        },
        update() {
            this.$api.sysMenu
                .updateSysMenu(this.dialogForm)
                .then((res) => {
                    if (res.success) {
                        // 更新树节点
                        for (let key in res.data) {
                            if (key in this.menuNode.data) {
                                // 以防后续表单字段有变更，仅保存对应key的值
                                this.menuNode.data[key] = res.data[key];
                            }
                        }
                        this.closeDialog();
                        this.$message({
                            message: res.msg,
                            type: "success",
                        });
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        // 保存
        save(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    if (!this.dialogForm.id) {
                        this.add();
                    } else {
                        this.update();
                    }
                } else {
                    // 校验失败
                }
            });
        },
    },
};
</script>

<style scoped>
.my-dialog-footer {
  text-align: center;
  margin-left: -130px;
}
</style>
