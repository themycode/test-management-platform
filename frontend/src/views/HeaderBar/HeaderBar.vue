<template>
    <div class="header-bar-wrapper">
        <!-- logo -->
        <div class="logo-wrapper left-nav-width" @click="clickLogo">
            <img class="logo-img" src="../../common/assets/logo.png" />
        </div>

        <!-- 导航菜单 -->
        <div class="nav-menu-wrapper">
            <el-menu
                :default-active="activeIndex"
                mode="horizontal"
                @select="handleSelect"
                background-color="#545c64"
                text-color="#fff"
                active-text-color="#ffd04b"
            >
                <!-- 动态加载顶部导航菜单 -->
                <header-bar-menu
                    class="custom-nav-menu-item"
                    v-for="item in navMenuData"
                    :key="item.id"
                    :menu="item"
                    :activeIndex="activeIndex"
                ></header-bar-menu>

                <!-- 工具栏\用户信息栏 -->
                <div class="right-nav-nav-wrapper">
                    <el-menu-item>
                        <!-- 用户信息 -->
                        <el-dropdown trigger="click" v-if="userName">
                            <span class="el-dropdown-link">
                                {{ userName }}
                                <i
                                    v-if="userName"
                                    class="el-icon-caret-bottom el-icon--right"
                                ></i>
                            </span>
                            <el-dropdown-menu v-if="userName" slot="dropdown">
                                <el-dropdown-item @click.native="modifyPassword">修改密码</el-dropdown-item>
                                <el-dropdown-item @click.native="bindAccount">关联账号</el-dropdown-item>
                                <!-- <el-dropdown-item>个人信息</el-dropdown-item> -->
                                <el-dropdown-item @click.native="logout">退出登录</el-dropdown-item>
                            </el-dropdown-menu>
                        </el-dropdown>
                        <el-button
                            v-if="userName == '' || userName == undefined || userName == null"
                            size="mini"
                            @click="login"
                        >登录</el-button>
                    </el-menu-item>
                </div>
            </el-menu>
        </div>

        <!-- 修改密码对话框 -->
        <modify-passwd-dialog
            v-if="modifyPasswdDlgVisible"
            :dialogVisible.sync="modifyPasswdDlgVisible"
        ></modify-passwd-dialog>

        <!-- 关联账号对话框 -->
        <related-account-dlg
            v-if="relatedAccountDlgVisible"
            :dialogVisible.sync="relatedAccountDlgVisible"
            :userId="userId"
        ></related-account-dlg>
    </div>
</template>

<script>
import { mapState } from "vuex";
import HeaderBarMenu from "@/common/components/HeaderBar/HeaderBarMenu";
import api from "@/common/network/api";
import ModifyPasswdDialog from "@/common/components/HeaderBar/ModifyPasswdDialog";
import RelatedAccountDlg from "@/views/System/SysUser/RelatedAccountDialog";

import Cookies from "js-cookie";

export default {
    name: "HeaderBar",
    components: {
        HeaderBarMenu,
        ModifyPasswdDialog,
        RelatedAccountDlg,
    },
    data() {
        return {
            user: { userName: "" }, // 存储用户姓名，为了加速，直接从浏览器sessionSorage读取
            relatedAccountDlgVisible: false, // 标识关联账号对话框是否可见
            modifyPasswdDlgVisible: false, // 修改密码对话框是否可见标识
        };
    },
    watch: {
        navMenuData: function () {
            this.activeDefaultNavMenu();
        },
    },
    methods: {
        // 点击事件处理函数，存放通用处理操作
        _handleClick(index, menuUrl, clickLogo, visitOtherNav) {
            if (index == this.activeIndex) {
                // 如果当前页已经是默认菜单页面，则不往下执行代码
                return;
            }

            // 查找顶部导航当前选中菜单的url
            let navMenuUrl = undefined;
            let simulatedClick = false; // 标记是否模拟点击
            if (menuUrl) {
                navMenuUrl = menuUrl;
                simulatedClick = true;
            } else {
                // 查找顶部导航当前选中菜单的url
                for (var i = 0; i < this.navMenuData.length; i++) {
                    if (this.navMenuData[i].id + "" == index) {
                        navMenuUrl = this.navMenuData[i].url;
                        break;
                    }
                }
                if (!navMenuUrl) {
                    // 没找到菜单url或者找到的url为空
                    return;
                }
            }

            if (this.activeIndex || visitOtherNav) {
                // 如果this.activeIndex有非空值，说明不是执行浏览器刷新操作 // visitOtherNav为真，标识访问其它导航菜单
                this.$store.commit("updateMainTabs", []); // 关闭所有tab页
                sessionStorage.removeItem("indexOfLeftNavMenuActive"); // 移除左侧导航当前选中菜单的索引
                sessionStorage.removeItem("urlOfLeftNavMenuActive"); // 移除左侧导航当前选中菜单的url
            }

            // 存储顶部导航当前选中菜单的索引，url(// 程序设计把菜单id的值设计为索引值)
            sessionStorage.setItem("indexOfTopNavMenuActive", index); // 设置顶部导航当前选中菜单的自定义索引,程序设计把菜单id的值设计为索引值
            sessionStorage.setItem("urlOfTopNavMenuActive", navMenuUrl);

            this.$store.commit("onSelectTopNavMenu", index);

            /* 设置侧边导航栏是否展开还是折叠(如果不添加以下代码，会导致切换顶部导航菜单时，
            不同顶部导航菜单的侧边栏折叠/展开状态不一致，因为需要重新加载的组件)*/
            let navBarCollapsed = JSON.parse(
                sessionStorage.getItem("navBarCollapsed")
            );
            if (
                navBarCollapsed != null &&
                navBarCollapsed != this.$store.state.app.isCollapsed
            ) {
                this.$store.commit("onCollapse");
            }

            if (simulatedClick) {
                this.$router.push(navMenuUrl);
            }
        },
        // 激活默认菜单
        activeDefaultNavMenu() {
            let navMenus = this.navMenuData;
            let index = sessionStorage.getItem("indexOfTopNavMenuActive");
            var navMenuUrl = ""; // 存放顶部导航菜单url
            let metaIndex = "" + this.$router.history.current.meta.index;
            let metaIsTopNav = this.$router.history.current.meta.isTopNav;

            if (index && index == metaIndex && metaIsTopNav) {
                // 存在被点击过的顶部导航菜单，执行刷新操作--访问的就是该导航菜单
                navMenuUrl = sessionStorage.getItem("urlOfTopNavMenuActive");
                // 模拟点击导航菜单
                this._handleClick(index, navMenuUrl);
            } else if (metaIndex && metaIsTopNav) {
                // 访问其它导航菜单，比如直接浏览器输入地址，回车
                this._handleClick(
                    metaIndex,
                    this.$router.history.current.fullPath,
                    false,
                    true
                );
            } else if (index) {
                // 存在被点击过的顶部导航菜单，并且访问的是该导航菜单下的子菜单
                navMenuUrl = sessionStorage.getItem("urlOfTopNavMenuActive");
                // 模拟点击导航菜单
                this._handleClick(index, navMenuUrl);
            } else {
                /*不存在被点击的顶部导航菜单，也不是切换到其它顶部导航菜单,获取菜单资源数据数组中指定索引位置的菜单作为默认选中的导航菜单，并设置其url为默认访问的url*/
                index = this.$appConfig.indexOfTopNavMenuActive;
                this.activeIndex = ""; //重置索引，避免登录-退出-再登录时，_handleClick(index, menuUrl, clickLogo, visitOtherNav)     index = this.activeIndex，则不往下执行代码，导致左侧导航菜单为空

                if (navMenus.length >= index + 1) {
                    navMenuUrl = navMenus[index].url;
                    index = "" + navMenus[index].id;
                    this._handleClick(index, navMenuUrl);
                } else {
                    console.log(
                        "默认导航菜单索引配置错误或者是获取菜单资源数组为空数组[]"
                    );
                }
            }
        },
        // 点击导航栏菜单
        handleSelect(index, indexPath) {
            this._handleClick(index);
        },
        clickLogo: function () {
            let index = this.$appConfig.indexOfTopNavMenuActive;
            if (this.navMenuData.length >= index + 1) {
                let activeIndex = "" + this.navMenuData[index].id;
                let navMenuUrl = this.navMenuData[index].url;
                this._handleClick(activeIndex, navMenuUrl, true);
            }
        },
        // 退出登录
        logout: function () {
            let taskAfterLogout = () => {
                sessionStorage.clear();
                Cookies.remove("token");
                this.$store.commit("setUserId", undefined);
                this.$store.commit("setIsSuperUser", undefined); // 保存是否超级管理员用户标识
                this.$store.commit("setUserName", ""); // 保存用户姓名
                this.$store.commit("setMenuRouteLoadStatus", false); // 重置导航菜单加载状态为false
                this.$store.commit("updateMainTabs", []); // 关闭所有tab页
                // this.activeIndex = ""; // 重置索引，避免登录-退出-再登录时，_handleClick(index, menuUrl, clickLogo, visitOtherNav)     index = this.activeIndex，则不往下执行代码，导致左侧导航菜单为空// 改成在_handleClick函数中统一处理
                this.$router.push("/login");
            };

            this.$confirm("确认退出吗?", "提示", {
                type: "warning",
            })
                .then(() => {
                    this.$api.login
                        .logout()
                        .then((res) => {
                            if (res.success) {
                                taskAfterLogout();
                            } else {
                                this.$message.error(res.msg);
                            }
                        })
                        .catch(res => {
                            this.$message.error(res.msg || res.message);
                        });
                })
                .catch(() => {});
        },
        // 登录
        login: function () {
            this.$router.push("/login");
        },
        // 修改密码
        modifyPassword() {
            if (!this.modifyPasswdDlgVisible) {
                this.modifyPasswdDlgVisible = true;
            }
        },
        // 关联账号
        bindAccount() {
            if (!this.relatedAccountDlgVisible) {
                this.relatedAccountDlgVisible = true;
            }
        },
        // 获取当前登录用户个人信息
        getUserPersonalInfo() {
            new Promise(this.$customUtils.userInfo.getCurrentUserInfo)
                .then((res) => {
                    if (JSON.stringify(res.data) != "{}") {
                        this.$store.commit("setUserId", res.data.id);
                        this.$store.commit(
                            "setIsSuperUser",
                            res.data.isSuperuser
                        ); // 保存是否超级管理员用户标识
                        this.$store.commit("setUserName", res.data.name); // 保存用户姓名
                        this.$store.commit(
                            "setUserGroups",
                            res.data.userGroups
                        ); // 用户用户关联的组别
                        this.$store.commit("setUserPerms", res.data.perms); // 保存用户权限标识
                    }
                })
                .catch((err) => {
                    this.$message.error(res.msg || res.message);
                });
        },
    },
    created() {
        if (this.userId == undefined) {
            this.getUserPersonalInfo();
        }
    },
    mounted() {
        // 访问默认导航菜单
        this.activeDefaultNavMenu();
    },
    computed: {
        ...mapState({
            navMenuData: (state) => state.menu.navMenuData,
            userId: (state) => state.user.userId,
            userName: (state) => state.user.userName,
        }),
        activeIndex: {
            get() {
                return this.$store.state.app.indexOfTopNavMenuActive;
            },
            set(val) {
                this.$store.commit("setIndexOfTopNavMenuActive", val);
            },
        },
    },
};
</script>

<style lang="scss" scoped>
.header-bar-wrapper {
    height: 100%;

    /* 页面顶部导航左侧logo */
    .logo-wrapper {
        height: calc(
            100% - 2px
        ); // -2是为了在“视觉上”让logo top和bottom边框和导航菜单上下边界对齐
        display: inline-block;
        .logo-img {
            height: 100%;
            width: 100%;
        }
        cursor: pointer;
        border-top: solid 1px rgb(84, 92, 100);
        border-bottom: solid 1px rgb(84, 92, 100);
    }

    /* 页面顶部导航菜单容器 */
    .nav-menu-wrapper {
        display: inline-block;
        position: absolute;
        float: right;
        height: 100%;
        width: calc(100% - 198px); // 198为左侧logo占用宽度
        overflow: hidden; // 取巧//不让导航菜单换行

        /* 页面顶部导航右侧栏 */
        .right-nav-nav-wrapper {
            float: right;
            .el-dropdown {
                color: #fff; //el-dropdown的color覆盖了菜单的文字颜色
            }
        }
    }

    .custom-nav-menu-item {
        border-right-style: solid;
        border-right-width: 1px;
        border-right-color: #b6939356;
    }
}
</style>
