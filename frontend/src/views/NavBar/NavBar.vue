<template>
    <div
        class="left-nav-wrapper"
        :class="isCollapsed ? 'left-nav-width-collapsed' : 'left-nav-width'"
    >
        <!--展开/折叠开关-->
        <div class="menu-toggle collapse-toggle" @click.prevent="onCollapse">
            <i class="fa fa-outdent" v-show="!isCollapsed" title="收起"></i>
            <i class="fa fa-indent" v-show="isCollapsed" title="展开"></i>
        </div>

        <el-menu
            ref="navMenu"
            :default-openeds="openeds"
            :default-active="activeIndex"
            :collapse="isCollapsed"
            :collapse-transition="false"
            :unique-opened="true"
            @open="handleOpen"
            @close="handleClose"
            @select="handleSelect"
        >
            <!-- 动态加载导航菜单-->
            <nav-bar-menu
                v-for="menuItem in navMenuData"
                :key="menuItem.id"
                :menu="menuItem"
                :isCollapsed="isCollapsed"
            ></nav-bar-menu>
        </el-menu>
    </div>
</template>

<script>
import { mapState } from "vuex";
import NavBarMenu from "@/common/components/navBarMenu";

export default {
    name: "NavBar",
    data() {
        return {
            openeds: [],
        };
    },
    components: {
        NavBarMenu,
    },
    watch: {
        indexOfTopNavMenuActive: function () {
            this.activeDefaultLeftNavMenu();
        },
    },
    computed: {
        ...mapState({
            isCollapsed: (state) => state.app.isCollapsed,
            indexOfTopNavMenuActive: (state) =>
                state.app.indexOfTopNavMenuActive,
            navMenuData: (state) => {
                let navMenuData = state.menu.navMenuData;
                // 根据父级菜单查找子菜单
                for (var i = 0; i < navMenuData.length; i++) {
                    let parentMenu = navMenuData[i];
                    let parentMenuID = "" + parentMenu.id;
                    if (parentMenuID == state.app.indexOfTopNavMenuActive) {
                        return parentMenu.children;
                    }
                }
            },
        }),
        activeIndex: {
            get() {
                return this.$store.state.app.indexOfLeftNavMenuActive;
            },
            set(val) {
                this.$store.commit("onSelectLeftNavMenu", val);
            },
        },
        mainTabs: {
            get() {
                return this.$store.state.tab.mainTabs;
            },
            set(val) {
                this.$store.commit("updateMainTabs", val);
            },
        },
        currTabName: {
            // 当前处于激活状态的tab页名称
            get() {
                return this.$store.state.tab.currTabName;
            },
            set(val) {
                this.$store.commit("updateCurrTabName", val);
            },
        },
    },
    mounted() {
        this.activeDefaultLeftNavMenu();

        // 如果导航默认收起，自动隐藏菜单右侧箭头
        this.$nextTick(function () {
            const els = this.$el.getElementsByClassName(
                "el-submenu__icon-arrow el-icon-arrow-right"
            );
            for (let i = 0; i < els.length; i++) {
                els[i].style.cssText =
                    "height: 0; width: 0;visibility: hidden; display: inline-block;";
            }
        });
    },

    methods: {
        // 设置导航折叠状态
        setNavFoldingState(navArray) {
            let children = [];
            for (let i = 0; i < navArray.length; i++) {
                if (
                    navArray[i].collapsed != undefined &&
                    !navArray[i].collapsed
                ) {
                    // 如果设置菜单折叠状态为展开，则展开菜单
                    let index = navArray[i].id + "";
                    this.openeds.push(index);
                }
                if (!navArray[i].children.length) {
                    children = children.concat(navArray[i].children);
                }
            }

            if (children.length) {
                this.setNavFoldingState(children);
            }
        },
        //激活左侧默认导航菜单
        activeDefaultLeftNavMenu() {
            let indexOfLeftNavMenuActive = sessionStorage.getItem(
                "indexOfLeftNavMenuActive"
            );
            let urlOfLeftNavMenuActive = sessionStorage.getItem(
                "urlOfLeftNavMenuActive"
            );
            if (indexOfLeftNavMenuActive) {
                // 有点击过左侧导航菜单
                this.activeIndex = indexOfLeftNavMenuActive;
                // 通过菜单URL跳转至指定路由
                this.handleSelect(indexOfLeftNavMenuActive, [
                    indexOfLeftNavMenuActive,
                ]);
                // 模拟点击 // 通过菜单URL跳转至指定路由
                this.$router.push(urlOfLeftNavMenuActive);
            } else {
                if (this.navMenuData.length > 0) {
                    this.setNavFoldingState(this.navMenuData);
                }
            }
        },
        handleOpen(index, indexPath) {
            // console.log(index, indexPath);
        },
        handleClose(index, indexPath) {
            // console.log(index, indexPath);
        },
        // 根据菜单id从菜单资源数组中获取该菜单自身相关信息
        getMenuInfo(menuID, menuData = []) {
            let children = []; // 存放二级菜单下的子菜单
            let result = {};
            for (var i = 0; i < menuData.length; i++) {
                if (menuData[i] && "" + menuData[i].id == menuID) {
                    result = {
                        name: menuData[i].name,
                        icon: menuData[i].icon,
                        title: menuData[i].name,
                        url: menuData[i].url,
                    };
                    return result;
                } else if (
                    menuData[i].children &&
                    menuData[i].children.length > 0
                ) {
                    children = children.concat(menuData[i].children);
                }
            }

            if (children.length > 0) {
                return this.getMenuInfo(menuID, children);
            }

            return result;
        },
        handleSelect(index, indexPath) {
            // 这里index被设计为“菜单资源id”
            var tab = this.mainTabs.filter((item) => item.id === index); // tab的id设计为菜单的id
            if (tab.length == 0) {
                // 不存在该tab页，则添加
                //根据菜单id从二级菜单开始，在二级、更高层级的菜单数据中查找本菜单相关信息，供新建tab页使用
                let navMenuData = this.$store.state.menu.navMenuData;
                let menuInfo = {};
                for (var i = 0; i < navMenuData.length; i++) {
                    if (navMenuData[i].children.length > 0) {
                        menuInfo = this.getMenuInfo(
                            index,
                            navMenuData[i].children
                        );
                        if (JSON.stringify(menuInfo) != "{}") {
                            var tab = {
                                name: index + menuInfo.name,
                                title: menuInfo.name, // 展示用
                                icon: menuInfo.icon,
                                url: menuInfo.url,
                                id: index,
                            };

                            this.mainTabs = this.mainTabs.concat([tab]);

                            this.currTabName = tab.name;
                            this.activeIndex = index;
                            sessionStorage.setItem(
                                "indexOfLeftNavMenuActive",
                                index
                            );
                            sessionStorage.setItem(
                                "urlOfLeftNavMenuActive",
                                tab.url
                            );

                            break;
                        }
                    }
                }
            } else {
                this.currTabName = tab[0].name;
                this.activeIndex = index;
                sessionStorage.setItem("indexOfLeftNavMenuActive", index);
                sessionStorage.setItem("urlOfLeftNavMenuActive", tab[0].url);
            }

            if (this.mainTabs.length >= 1) {
                this.$store.commit("onAllTabsClosed", false);
            }
        },
        // 折叠导航栏
        onCollapse: function () {
            this.$store.commit("onCollapse");

            // 收起导航时，隐藏右侧箭头按钮
            this.$nextTick(function () {
                const els = this.$el.getElementsByClassName(
                    "el-submenu__icon-arrow el-icon-arrow-right"
                );
                for (let i = 0; i < els.length; i++) {
                    els[i].style.cssText =
                        "height: 0; width: 0;visibility: hidden; display: inline-block;";
                }
            });

            sessionStorage.setItem(
                "navBarCollapsed",
                this.$store.state.app.isCollapsed
            );
        },
    },
};
</script>

<style scoped lang="scss">
.left-nav-wrapper {
    position: absolute;
    top: 0px;
    left: 0px;
    right: 0px;
    bottom: 0px;
    overflow-x: hidden;
    .el-menu {
        height: 100%;
    }
}

/*页面左侧导航折叠后的宽度*/
.left-nav-width-collapsed {
    width: 55px;
    border-right: solid 1px #e6e6e6;
}

.collapse-toggle {
    i {
        position: relative;
        float: right;
        color: #606266;
        z-index: 1;
    }
}
</style>
