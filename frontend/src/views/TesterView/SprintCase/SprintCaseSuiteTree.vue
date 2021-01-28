<template>
    <div>
        <div class="tree-container" ref="treeContainer">
            <el-tree
                ref="tree"
                :props="defaultProps"
                :load="loadNode"
                lazy
                :empty-text="emptyText"
                node-key="id"
                @node-click="clickNode"
                @node-contextmenu="onNodeContextMenu"
                @node-expand="expandNode"
                @node-collapse="collapseNode"
                :render-content="renderContent"
                :expand-on-click-node="false"
                :default-expanded-keys="defaultExpandedKeys"
            ></el-tree>
        </div>

        <!--鼠标右键菜单面板（一个基于鼠标位置的模态框） -->
        <div v-show="contextMenuVisible">
            <ul id="contextMenu" class="context-menu">
                <li class="context-menu-item" @click="refreshNode">刷新测试集</li>
                <li
                    v-if="showPasteCasesCopiedMenu"
                    class="context-menu-item"
                    @click="pasteTestcasesCopied"
                >黏贴测试用例</li>
                <li
                    v-if="showPasteCasesCutMenu"
                    class="context-menu-item"
                    @click="pasteTestcasesCut"
                >黏贴测试用例</li>
                <li
                    v-if="showCopySuiteByStructureMenu"
                    class="context-menu-item"
                    @click="copySuiteByStructure"
                >按结构复制测试集</li>
                <li v-if="showCutSuiteMenu" class="context-menu-item" @click="cutSuite">剪切测试集</li>
                <li
                    v-if="showPasteSuiteCutMenu"
                    class="context-menu-item"
                    @click="pasteSuiteCut"
                >黏贴测试集</li>
                <li
                    v-if="showPasteSuiteByStructureMenu"
                    class="context-menu-item"
                    @click="pasteSuiteByStructure"
                >黏贴测试集</li>
                <li class="context-menu-item" @click="addNode">新增子测试集</li>
                <li class="context-menu-item" @click="editNode">重命名测试集</li>
                <li class="context-menu-item" @click="removeNode">删除测试集</li>
            </ul>
        </div>
        <!--删除套件确认弹窗-->
        <del-suite-confirm-dlg
            v-if="delSuiteConfirmDlgVisible"
            :dialogVisible.sync="delSuiteConfirmDlgVisible"
            :suiteTypeForDel="suiteTypeForDel"
            :suiteIdForDel="suiteIdForDel"
        ></del-suite-confirm-dlg>
    </div>
</template>

<script>
import { mapState } from "vuex";
import { elTreeMixin } from "@/common/mixins/elTreeMixin";

import DelSuiteConfirmDlg from "./DelSuiteConfirmDlg";

export default {
    props: ["sprintID", "productID", "planID", "currentModule"],
    components: { DelSuiteConfirmDlg },
    mixins: [elTreeMixin],
    data() {
        return {
            oldNameForNodeEditing: "", // 编辑节点前的测试集名称
            type: "sprint", // type: 节点分类  base  基线测试套件 sprint 迭代测试套件 testplan-测试计划关联的套件
            suiteIdCopiedByStructure: "", // 存放按结构拷贝的基线套件ID
            currNodeDataObjectCut: null, // 存放被剪切的套件结点数据对象
            nodeObjectCut: null, // 存放被剪切的测试套件
            delSuiteConfirmDlgVisible: false, // 控制是否弹出删除测试套件确认弹窗
            suiteIdForDel: null, // 存放待删除套件id
            suiteTypeForDel: null, // 存放待删除套件类型
        };
    },

    methods: {
        loadNode(node, resolve) {
            if (!this.productID) {
                return resolve([]);
            }
            // loadNode优先于mounted方法被调用
            if (node.level === 0) {
                // 如果是顶级节点，加载一级测试用例套件
                this.$api.sprintCaseSuite
                    .getSprintCaseSuiteTree({
                        parentId: -1,
                        productId: this.productID,
                        sprintId: this.sprintID,
                        planId: this.planID,
                        sort: "id",
                        level: "topSuite",
                        recursive: 0, // 是否递归查找
                    })
                    .then((res) => {
                        if (res.success) {
                            // 获取sprint测试套件ID-根测试套件ID
                            let rootSuites = res.data.filter(
                                (item) => item.type == "sprint"
                            );

                            if (rootSuites.length < 1) {
                                // 获取base测试套件ID-根测试套件ID
                                rootSuites = res.data.filter(
                                    (item) => item.type == "base"
                                );
                            }

                            let rootSuiteID = -1;
                            if (rootSuites.length > 0) {
                                rootSuiteID = rootSuites[0].id;
                                this.defaultExpandedKeys.push(rootSuiteID); // 默认展开第一个sprint根测试套件，如果sprint根测试套件不存在，则展开base根测试套件

                                // 先重置当前套件信息，然后再重新设置当前套件信息，以便右侧表格重新加载、加载被右键节点关联的测试用例
                                this.updateCurrentSuite(-1, -1, -2, "", "");

                                // 如果不延迟执行，右侧表格数据不会重新加载，因为程序执行速度过快，导致其它模块对suiteId的监听“无感知”
                                let suitePath = "/" + rootSuites[0].name;
                                setTimeout(() => {
                                    this.updateCurrentSuite(
                                        rootSuiteID,
                                        rootSuites[0].productId,
                                        rootSuites[0].parentId,
                                        rootSuites[0].type,
                                        suitePath
                                    );
                                }, 5);
                            } else {
                                // 迭代为空，没有套件树
                                setTimeout(() => {
                                    this.updateCurrentSuite(-2, -1, -1, "", "");
                                }, 5);

                                this.updateCurrentSuite(-1, -1, -1, "", "");
                            }
                            return resolve(res.data);
                        } else {
                            this.$message.error(res.msg);
                            return resolve([]);
                        }
                    })
                    .catch((res) => {
                        this.$message.error(res.msg || res.message);
                        return resolve([]);
                    });
            } else if (node.level >= 1) {
                // 加载非一级测试用例套件,即子测试套件
                this.$api.sprintCaseSuite
                    .getSprintCaseSuiteTree({
                        parentId: node.data.id,
                        planId: this.planID,
                        productId: this.productID,
                        sort: "-id",
                        level: "subSuite",
                        recursive: 0, // 是否递归查找
                    })
                    .then((res) => {
                        if (res.success) {
                            return resolve(res.data);
                        } else {
                            this.$message.error(res.msg);

                            return resolve([]);
                        }
                    })
                    .catch((res) => {
                        this.$message.error(res.msg || res.message);
                        return resolve([]);
                    });
            }
        },
        // 右键测试套件节点
        onNodeContextMenu(event, dataObject, node, vueComponent) {
            if (this.currentModule == "planCaseListTab") {
                //处于测试计划管理-计划详情-测试用例tab页面
                return;
            }
            if (dataObject.editing) {
                // 如果右键的节点正处于编辑状态，则不显示右键菜单
                return;
            }

            this.type = dataObject.type; // 存储测试套件节点类型
            this.oldNameForNodeEditing = dataObject.name; // 记录节点名称，供修改失败还原旧值使用

            this.rightClickNode(event, dataObject, node, vueComponent);
        },

        // 展开节点
        expandNode(dataObject, node, vueComponent) {
            // this.hideContextMenu();
            // this.defaultExpandedKeys.push(dataObject.id);
        },

        // 收起节点
        collapseNode(dataObject, node, vueComponent) {
            // let index = this.defaultExpandedKeys.indexOf(dataObject.id);
            // if (index != -1) {
            //     this.defaultExpandedKeys.splice(index, 1);
            // }
        },
        // 更新当前套件信息（套件id，产品ID，套件类型，套件路径,关联组别id）
        updateCurrentSuite(suiteID, productID, parentID, suiteType, suitePath) {
            let suiteInfo = {
                suiteID: suiteID,
                productID: productID,
                parentID: parentID,
                suiteType: suiteType,
                suitePath: suitePath,
            };
            this.$store.commit("updateCurrentSuite", suiteInfo);
        },
        // // 获取当前测试套件所在的父级测试套件路径
        // getParentSuitePath(parentSuiteId, suitePath = "") {
        //     let nodeObj = this.$refs.tree.getNode(parentSuiteId);

        //     if (nodeObj) {
        //         let suiteName = nodeObj.data.name;
        //         let parentId = nodeObj.data.parentId;
        //         if (parentId != -1) {
        //             // 存在上级测试套件
        //             return this.getParentSuitePath(parentId) + "/" + suiteName;
        //         } else {
        //             return "/" + suiteName;
        //         }
        //     }
        //     return "";
        // },
        // 处理鼠标左键节点事件
        handleNodeLeftClickEvent(dataObject) {
            // 获取节点路径
            let suitePath =
                this.getParentSuitePath(dataObject.parentId) +
                "/" +
                dataObject.name;
            this.updateCurrentSuite(
                dataObject.id,
                dataObject.productId,
                dataObject.parentId,
                dataObject.type,
                suitePath
            );
            this.hideContextMenu();
        },

        // 点击节点
        clickNode(dataObject, node, vueComponent) {
            this.currNodeDataObject = dataObject;
            this.currNode = node;
            this.type = dataObject.type;
            this.oldNameForNodeEditing = dataObject.name;

            this.handleNodeLeftClickEvent(dataObject);
        },

        // 新增子节点
        addNode() {
            const isLeafByUser = this.currNode.isLeafByUser;
            this.currNode.isLeafByUser = false; // 先设置当前节点为非叶子节点，否则无法添加子节点

            const newChild = {
                parentId: this.currNodeDataObject.id, // 父节点ID
                type: this.currNodeDataObject.type, // 父节点类型
                productId: this.currNodeDataObject.productId, // 父节点关联的产品ID
                sprintId: this.currNodeDataObject.sprintId, // 父节点关联的迭代ID
            };

            if (!this.currNode.expanded) {
                // 如果节点未展开，先展开节点
                if (!this.currNode.expanded) {
                    this.currNode.expanded = true;
                }

                // 加载子节点
                this.$api.sprintCaseSuite
                    .getSprintCaseSuiteTree({
                        parentId: this.currNodeDataObject.id,
                        productId: this.currNodeDataObject.productId,
                        sort: "-id",
                        level: "subStuie",
                        recursive: 0, // 是否递归查找
                    })
                    .then((res) => {
                        if (res.success) {
                            // this.currNodeDataObject.children = res.data; //这里不能这么做，会导致数据重复加载
                            let children = res.data;

                            // 添加子节点
                            this.$api.sprintCaseSuite
                                .addSprintCaseSuite(newChild)
                                .then((res) => {
                                    if (res.success) {
                                        children.splice(0, 0, res.data);
                                        this.oldNameForNodeEditing =
                                            res.data.name;

                                        this.currNode.childNodes = [];
                                        this.currNodeDataObject.children = children;
                                        this.$refs.tree.updateKeyChildren(
                                            this.currNodeDataObject.id,
                                            this.currNodeDataObject.children
                                        );
                                    } else {
                                        // 新增失败
                                        if (isLeafByUser) {
                                            // 如果被点击节点为叶子节点，则还原为叶子节点
                                            this.currNode.isLeafByUser = true;
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
                // 先获取被右键节点（即待新增节点的父节点）的子节点数据对象
                let children = [];
                for (let i = 0; i < this.currNode.childNodes.length; i++) {
                    children.push(this.currNode.childNodes[i].data);
                }
                this.$api.sprintCaseSuite
                    .addSprintCaseSuite(newChild)
                    .then((res) => {
                        if (res.success) {
                            this.oldNameForNodeEditing = res.data.name;
                            // 给节点数据对象添加子节点数据
                            children.splice(0, 0, res.data);

                            // 给节点对象添加子节点，如果缺少这一步，相同节点重复执行新增操作时，第二次新增操作，节点树中只会显示第二次新增的节点
                            this.$refs.tree.updateKeyChildren(
                                this.currNodeDataObject.id,
                                children
                            );
                        } else {
                            // 新增失败
                            if (isLeafByUser) {
                                // 如果被点击节点为叶子节点，则还原为叶子节点
                                this.currNode.isLeafByUser = true;
                            }
                            this.$message.error(res.msg);
                        }
                    })
                    .catch((res) => {
                        this.$message.error(res.msg || res.message);
                    });
            }
        },
        // 修改节点
        editNode() {
            this.$set(this.currNodeDataObject, "editing", true);
        },

        // 移除当前被点击的结点// 删除迭代测试集时被调用
        removeCurrNodeClicked() {
            this.$refs.tree.remove(this.currNode);
        },

        // 删除子节点
        removeNode() {
            const node = this.currNode;

            if (node.level == 1) {
                // 一级节点，不让删除
                this.$message.error("不能删除一级测试集");
            } else {
                this.delSuiteConfirmDlgVisible = true;
                this.suiteIdForDel = this.currNodeDataObject.id;
                this.suiteTypeForDel = this.currNodeDataObject.type;

                // this.$confirm(
                //     "确定要删除该测试集吗？ 删除该测试集将会删除其所有子测试集及对应的基线测试集",
                //     "提示",
                //     {
                //         confirmButtonText: "确定",
                //         cancelButtonText: "取消",
                //         type: "warning",
                //         cancelButtonClass: "btn-custom-cancel"
                //     }
                // )
                //     .then(() => {
                //         // 发送请求，执行删除操作
                //         this.$api.sprintCaseSuite
                //             .deleteSprintCaseSuite({
                //                 suiteId: this.currNodeDataObject.id,
                //                 type: this.currNodeDataObject.type
                //             })
                //             .then(res => {
                //                 if (res.success) {
                //                     this.$refs.tree.remove(node);
                //                     this.$message.success(res.msg);
                //                 } else {
                //                     this.$message.error(res.msg);
                //                 }
                //             })
                //             .catch(res => {
                // this.$message.error(res.msg||res.message);                //             });
                //     })
                //     .catch(() => {});
            }
        },
        // 刷新节点
        refreshNode(operation) {
            return new Promise((resolve, reject) => {
                // 如果节点未展开，先展开节点
                if (!this.currNode.expanded) {
                    this.currNode.expanded = true;
                }

                // 加载子节点
                this.$api.sprintCaseSuite
                    .getSprintCaseSuiteTree({
                        parentId: this.currNodeDataObject.id,
                        productId: this.currNodeDataObject.productId,
                        sort: "-id",
                        level: "subStuie",
                        recursive: 0, // 是否递归查找
                    })
                    .then((res) => {
                        if (res.success) {
                            let children = res.data;

                            this.currNode.childNodes = [];
                            this.currNodeDataObject.children = children;
                            this.$refs.tree.updateKeyChildren(
                                this.currNodeDataObject.id,
                                this.currNodeDataObject.children
                            );
                            if (operation != "pasteSuiteCut") {
                                this.$message.success("刷新成功");
                            }
                            resolve("success");
                        } else {
                            this.$message.error(res.msg);
                            reject(res.msg);
                        }
                    })
                    .catch((res) => {
                        this.$message.error(res.msg || res.message);
                        reject(res.msg);
                    });
            });
        },
        onBlur(event, data) {
            if (!data.editing) {
                // 已经修改//避免回车事件触发失去焦点事件，引发重复修改
                return;
            }

            if (event.keyCode != undefined && event.keyCode != 13) {
                // 如果不是失去焦点事件，也不是回车事件，停止执行
                return;
            }

            // 编辑框失去焦点时的事件处理函数\保存节点信息
            const $input =
                event.target.parentNode.querySelector("input") ||
                event.target.parentElement.querySelector("input");
            if (!$input) {
                this.$message.error("获取节点输入框对象失败，保存节点名称失败");
                this.currNodeDataObject.name = this.oldNameForNodeEditing;
                return false;
            } else {
                data.name = $input.value; // 保存输入框的值为节点的值
                if (data.name.trim() == "") {
                    this.$message.error("操作失败，测试集名称不能为空");
                    return;
                }
                // 发送后台请求，更新节点名称
                this.$api.sprintCaseSuite
                    .updateSprintCaseSuite({
                        suiteId: data.id,
                        name: data.name,
                        type: data.type,
                    })
                    .then((res) => {
                        if (res.success) {
                            data.editing = false;
                            this.$message.success(res.msg);
                        } else {
                            this.currNodeDataObject.name = this.oldNameForNodeEditing;
                            data.editing = false;
                            this.$message.error(res.msg);
                        }
                    })
                    .catch((res) => {
                        data.name = this.oldNameForNodeEditing;
                        data.editing = false;
                        this.$message.error(res.msg || res.message);
                    });
            }
        },
        displayOrEdit(data) {
            // 展示或编辑节点
            if (data.editing) {
                // 正在编辑，则返回以节点名称为value值的输入框
                return (
                    <span>
                        <input
                            type="text"
                            value={data.name}
                            on-keyup={(event) => this.onBlur(event, data)}
                            on-blur={(event) => this.onBlur(event, data)}
                            v-focus // 自动聚焦
                            ref="input"
                        />
                    </span>
                );
            } else {
                // 否则，返回节点名称为元素内容的span元素
                return (
                    <span
                        class="span-font"
                        tabindex="1"
                        on-keyup={(event) => this.onTreeNoInsertKeyUp(event)}
                    >
                        {data.name}
                    </span>
                );
            }
        },
        renderContent(h, { node, data, store }) {
            return (
                <span>
                    <span>{this.displayOrEdit(data)}</span>
                </span>
            );
        },
        onTreeNoInsertKeyUp(event) {
            if (event.code === "Insert") {
                this.addNode();
            }
        },
        // 黏贴拷贝的用例到目标测试集
        pasteTestcasesCopied() {
            this.$api.sprintCaseSuite
                .pasteTestcasesCopied({
                    suiteId: this.currNodeDataObject.id,
                    testcases: this.testcasesCopied,
                })
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                        this.$store.commit("setTestcasesCopied", []); // 重置拷贝的测试用例为[]

                        // 先重置当前套件信息，然后再重新设置当前套件信息，以便右侧表格重新加载、加载被右键节点关联的测试用例
                        this.updateCurrentSuite(-1, -1, -2, "", "");

                        // 如果不延迟执行，右侧表格数据不会重新加载，因为程序执行速度过快，导致其它模块对suiteId的监听“无感知”
                        setTimeout(() => {
                            this.handleNodeLeftClickEvent(
                                this.currNodeDataObject
                            );
                        }, 5);
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        // 黏贴剪切的用例到目标测试集
        pasteTestcasesCut() {
            // 获取第一个用例的所在套件类型，作为所有待剪切用例的套件类型（目前不可能通过界面同时批量选取基线用例和迭代用例），当然，后台遍历用例时，也做过滤，自动过滤实际套件类型和所选的套件类型不符的用例
            let srcSuiteType = undefined;
            if (this.testcasesCut.length) {
                srcSuiteType = this.testcasesCut[0].suiteType;
            } else {
                this.$message.error("黏贴失败，请先剪切用例");
                return;
            }

            if (srcSuiteType == this.currNodeDataObject.type) {
            } else {
                this.$message.error(
                    "黏贴失败，请选择和被剪切用例所属套件类型相同的套件"
                );
                return;
            }

            this.$api.sprintCaseSuite
                .pasteTestcasesCut({
                    suiteId: this.currNodeDataObject.id,
                    productId: this.currNodeDataObject.productId,
                    testcases: this.testcasesCut,
                })
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                        this.$store.commit("setTestcasesCut", []); // 重置剪切的测试用例为[]

                        // 先重置当前套件信息，然后再重新设置当前套件信息，以便右侧表格重新加载、加载被右键节点关联的测试用例
                        this.updateCurrentSuite(-1, -1, -2, "", "");

                        // 如果不延迟执行，右侧表格数据不会重新加载，因为程序执行速度过快，导致其它模块对suiteId的监听“无感知”
                        setTimeout(() => {
                            this.handleNodeLeftClickEvent(
                                this.currNodeDataObject
                            );
                        }, 5);
                    } else {
                        this.$message.error(res.msg);
                    }
                })
                .catch((res) => {
                    this.$message.error(res.msg || res.message);
                });
        },
        // 按结构复制测试套件
        copySuiteByStructure() {
            this.suiteIdCopiedByStructure = this.currNodeDataObject.id;
            this.currNodeDataObjectCut = null; // 避免对用户造成干扰，清空剪切的测试集
            this.nodeObjectCut = null;
            this.$message.success("复制成功，请右键迭代任意测试集进行黏贴");
        },
        // 剪切测试套件
        cutSuite() {
            this.currNodeDataObjectCut = this.currNodeDataObject;
            this.nodeObjectCut = this.currNode;
            this.suiteIdCopiedByStructure = ""; // 避免对用户造成干扰，清空按结构复制的测试集
            this.$message.success("剪切成功，请右键同类型测试集进行黏贴");
        },
        // 黏贴剪切的测试套件
        pasteSuiteCut() {
            if (this.currNodeDataObjectCut.id == this.currNodeDataObject.id) {
                this.$message.error("黏贴失败，不能黏贴至被剪切的测试集");
                return;
            }
            if (
                this.currNodeDataObjectCut.type != this.currNodeDataObject.type
            ) {
                this.$message.error("黏贴失败，请右键同类型测试集进行黏贴");
                return;
            }

            this.$confirm(
                "确定要黏贴到" + this.currNodeDataObject.name + "测试集下吗？",
                "提示",
                {
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    type: "warning",
                    cancelButtonClass: "btn-custom-cancel",
                }
            )
                .then(() => {
                    this.$api.sprintCaseSuite
                        .pasteSuiteCut({
                            suiteId: this.currNodeDataObjectCut.id,
                            targetSuiteId: this.currNodeDataObject.id,
                            srcSuiteType: this.currNodeDataObjectCut.type,
                            targetSuiteType: this.currNodeDataObject.type,
                            // sprintId: this.sprintID,
                            productId: this.productID,
                        })
                        .then((res) => {
                            if (res.success) {
                                this.$refs.tree.remove(this.nodeObjectCut);

                                if (res.data.relatedSrcSuite) {
                                    // 移除被剪切套件关联的基线测试套件
                                    this.$refs.tree.remove(
                                        res.data.relatedSrcSuite
                                    );
                                }

                                if (res.data.relatedTargetSuite) {
                                    let tempcurrNodeDataObject = Object.assign(
                                        {},
                                        this.currNodeDataObject
                                    );

                                    // 获取黏贴至目标测试套件关联的基线测试套件
                                    let tempcurrNode = this.$refs.tree.getNode(
                                        res.data.relatedTargetSuite
                                    );
                                    if (tempcurrNode && tempcurrNode.expanded) {
                                        this.currNode = tempcurrNode;
                                        // 套件已经展开的情况下才刷新套件
                                        this.currNodeDataObject = this.currNode.data;
                                        this.refreshNode("pasteSuiteCut").then(
                                            () => {
                                                this.currNode = this.$refs.tree.getNode(
                                                    tempcurrNodeDataObject
                                                );
                                                this.currNodeDataObject = this.currNode.data;

                                                this.refreshNode(
                                                    "pasteSuiteCut"
                                                );

                                                // 如果不延迟执行，右侧表格数据不会重新加载，因为程序执行速度过快，导致其它模块对suiteId的监听“无感知”
                                                setTimeout(() => {
                                                    this.handleNodeLeftClickEvent(
                                                        this.currNodeDataObject
                                                    );
                                                }, 5);

                                                this.currNodeDataObjectCut = null;
                                                this.nodeObjectCut = null;
                                                this.$message.success(res.msg);
                                            }
                                        ); // 刷新当前节点
                                    } else {
                                        // 不存在黏贴至目标测试套件关联的基线测试套件、或者存在，但是未展开
                                        this.refreshNode("pasteSuiteCut"); // 刷新当前节点

                                        // 如果不延迟执行，右侧表格数据不会重新加载，因为程序执行速度过快，导致其它模块对suiteId的监听“无感知”
                                        setTimeout(() => {
                                            this.handleNodeLeftClickEvent(
                                                this.currNodeDataObject
                                            );
                                        }, 5);
                                        this.currNodeDataObjectCut = null;
                                        this.nodeObjectCut = null;
                                        this.$message.success(res.msg);
                                    }
                                } else {
                                    this.refreshNode("pasteSuiteCut"); // 刷新当前节点

                                    // 如果不延迟执行，右侧表格数据不会重新加载，因为程序执行速度过快，导致其它模块对suiteId的监听“无感知”
                                    setTimeout(() => {
                                        this.handleNodeLeftClickEvent(
                                            this.currNodeDataObject
                                        );
                                    }, 5);
                                    this.currNodeDataObjectCut = null;
                                    this.nodeObjectCut = null;
                                    this.$message.success(res.msg);
                                }
                            } else {
                                this.$message.error(res.msg);
                            }
                        })
                        .catch((res) => {
                            this.$message.error(res.msg || res.message);
                        });
                })
                .catch(() => {});
        },
        // 黏贴按结构复制的测试套件
        pasteSuiteByStructure() {
            this.$api.sprintCaseSuite
                .pasteSuiteByStructure({
                    baseSuiteId: this.suiteIdCopiedByStructure,
                    productId: this.currNodeDataObject.productId,
                    sprintId: this.currNodeDataObject.sprintId,
                })
                .then((res) => {
                    if (res.success) {
                        this.$message.success(res.msg);
                        this.suiteIdCopiedByStructure = "";
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
        this.$store.commit("setTestcasesCopied", []); // 重新加载套件，说明有切换到其它页面或者其它迭代项目，清空已拷贝内容
        this.$store.commit("setTestcasesCut", []);
    },
    computed: {
        ...mapState({
            testcasesCopied: (state) => state.sprintCaseTable.testcasesCopied, // 存放拷贝的用例
            testcasesCut: (state) => state.sprintCaseTable.testcasesCut, // 存放剪切的用例
        }),
        showPasteCasesCopiedMenu() {
            return (
                this.testcasesCopied.length &&
                this.currNode &&
                this.currNode.level > 1
            );
        },
        showPasteCasesCutMenu() {
            return (
                this.testcasesCut.length &&
                this.currNode &&
                this.currNode.level > 1
            );
        },
        showCutSuiteMenu() {
            return (
                this.currNodeDataObject &&
                this.currNode &&
                this.currNode.level > 1
            );
        },
        showPasteSuiteCutMenu() {
            if (this.currNodeDataObjectCut) {
                let temArray = this.currNodeDataObject.allUpperNodeIds.split(
                    ","
                );
                return (
                    this.currNodeDataObjectCut &&
                    this.currNodeDataObjectCut.type ==
                        this.currNodeDataObject.type &&
                    this.currNodeDataObjectCut.id !=
                        this.currNodeDataObject.id &&
                    this.currNodeDataObjectCut.parentId !=
                        this.currNodeDataObject.id &&
                    temArray.indexOf(
                        this.currNodeDataObjectCut.id.toString()
                    ) == -1
                );
            } else {
                return false;
            }
        },
        showCopySuiteByStructureMenu() {
            return (
                this.currNodeDataObject &&
                this.currNodeDataObject.type == "base" &&
                this.currNode.level > 1
            );
        },
        showPasteSuiteByStructureMenu() {
            return (
                this.currNodeDataObject &&
                this.currNodeDataObject.type == "sprint" &&
                this.suiteIdCopiedByStructure
            );
        },
    },
};
</script>
<style lang="scss" scoped>
.tree-container {
    position: absolute;
    top: 0px;
    bottom: 5px;
    left: 0px;
    right: 5px;
    overflow: auto;
    .el-tree {
        height: 100%;
    }
}
</style>
