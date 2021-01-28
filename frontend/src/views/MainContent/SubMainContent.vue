<template>
    <div
        class="sub-main-wrapper"
        :class="isCollapsed ? 'sub-main-left-collapsed' : 'sub-main-left'"
    >
        <div class="sub-main-tabs">
            <el-dropdown class="tabs-tools" :show-timeout="0" trigger="hover">
                <div style="font-size: 20px; text-align: center">
                    <i class="el-icon-arrow-down"></i>
                </div>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item @click.native="closeCurrentTab"
                        >关闭当前标签</el-dropdown-item
                    >
                    <el-dropdown-item @click.native="closeOtherTab"
                        >关闭其它标签</el-dropdown-item
                    >
                    <el-dropdown-item @click.native="closeAllTabs"
                        >关闭全部标签</el-dropdown-item
                    >
                    <el-dropdown-item @click.native="refreshCurrentTab"
                        >刷新当前标签</el-dropdown-item
                    >
                </el-dropdown-menu>
            </el-dropdown>

            <!-- 标签页 -->
            <el-tabs
                class="tabs"
                v-model="currTabName"
                :closable="true"
                @tab-click="selectedTab"
                @tab-remove="removeTab"
            >
                <!-- tab 面板  -->
                <el-tab-pane
                    v-for="item in mainTabs"
                    :key="item.id"
                    :label="item.title"
                    :name="item.name"
                >
                    <span slot="label">
                        <i :class="item.icon"></i>
                        {{ item.title }}
                    </span>
                </el-tab-pane>
            </el-tabs>
        </div>
        <!-- 主内容区域 -->
        <div class="sub-main-content">
            <!-- <transition name="fade" mode="out-in"> -->
            <router-view v-if="allTabsClosed == false"></router-view>
            <!-- </transition> -->
        </div>
    </div>
</template>

<script>
import { mapState } from "vuex";

export default {
    data() {
        return {};
    },
    computed: {
        mainTabs: {
            get() {
                return this.$store.state.tab.mainTabs;
            },
            set(val) {
                this.$store.commit("updateMainTabs", val);
            },
        },

        currTabName: {
            get() {
                return this.$store.state.tab.currTabName;
            },
            set(val) {
                this.$store.commit("updateCurrTabName", val);
            },
        },
        ...mapState({
            isCollapsed: (state) => state.app.isCollapsed,
            allTabsClosed: (state) => state.tab.allTabsClosed,
        }),
    },
    methods: {
        // 选中tab
        selectedTab(tab) {
            tab = this.mainTabs.filter((item) => item.name === tab.name);
            if (tab.length >= 1) {
                tab = tab[0];
                this.$router.push({ path: tab.url });
                sessionStorage.setItem("indexOfLeftNavMenuActive", tab.id);
                sessionStorage.setItem("urlOfLeftNavMenuActive", tab.url);
                this.$store.commit("onSelectLeftNavMenu", tab.id);
            }
        },
        // 删除tab
        removeTab(tabName) {
            this.mainTabs = this.mainTabs.filter(
                (item) => item.name !== tabName
            ); // this.mainTabs只保留不要删除的tab names
            if (this.mainTabs.length >= 1) {
                // 删除当前选中的tab
                if (tabName == this.currTabName) {
                    let currTab = this.mainTabs[this.mainTabs.length - 1];
                    // 激活位于被删除tab之前的第一个tab
                    this.$router.push(currTab.url);
                    this.currTabName = currTab.name;

                    sessionStorage.setItem(
                        "indexOfLeftNavMenuActive",
                        currTab.id
                    );
                    sessionStorage.setItem(
                        "urlOfLeftNavMenuActive",
                        currTab.url
                    );
                    this.$store.commit("onSelectLeftNavMenu", currTab.id);
                }
            }

            if (this.mainTabs.length == 0) {
                this.$store.commit("onAllTabsClosed", true);
                sessionStorage.removeItem("indexOfLeftNavMenuActive"); // 移除默认展开、激活的菜单索引
                sessionStorage.removeItem("urlOfLeftNavMenuActive"); // // 移除默认展开、激活的菜单url
            }
        },
        // 关闭当前
        closeCurrentTab() {
            this.removeTab(this.currTabName);
        },
        // 关闭其它
        closeOtherTab() {
            this.mainTabs = this.mainTabs.filter(
                (item) => item.name === this.currTabName
            );
        },
        // 关闭全部
        closeAllTabs() {
            this.mainTabs = [];
            this.$store.commit("onAllTabsClosed", true);
            sessionStorage.removeItem("indexOfLeftNavMenuActive");
            sessionStorage.removeItem("urlOfLeftNavMenuActive");
        },
        // 刷新当前
        refreshCurrentTab() {
            var tempTabName = this.currTabName;
            let currTab = this.mainTabs.filter(
                (item) => item.name === tempTabName
            );

            var urlOfCurrTab = "";
            if (currTab.length >= 1) {
                urlOfCurrTab = currTab.url;
            } else {
                console.log("不存在当前tab页");
                return;
            }

            if (urlOfCurrTab) {
                this.$nextTick(() => {
                    this.$router.push(urlOfCurrTab);
                });
            }
        },
    },
};
</script>

<style scoped  lang="scss">
.sub-main-left {
    left: 200px; // 左侧导航宽度+2px
}

.sub-main-left-collapsed {
    left: 57px; // 左侧导航宽度+2px
}

.sub-main-wrapper {
    position: absolute;
    top: 0px;
    bottom: 0px;
    right: 0px;
    padding: 0px;

    .sub-main-tabs {
        position: relative;
        height: 30px;
        width: 100%;

        .tabs {
            position: absolute;
            width: 100%;
            height: 30px;
            line-height: 30px;
        }
        .tabs-tools {
            position: absolute;
            top: 0px;
            right: 0px;
            height: 30px;
            line-height: 30px;
            width: 30px;
            cursor: pointer;
            border-left-color: rgba(200, 206, 206, 0.5);
            border-left-width: 1px;
            border-left-style: solid;
            z-index: 3;
        }

        .tabs-tools:hover {
            background: rgba(200, 206, 206, 1);
        }
    }
    .sub-main-content {
        position: absolute;
        top: 35px;
        left: 5px;
        right: 5px;
        bottom: 2px;
        padding: 0px;
        // background:#CCE8CF;
    }
}
</style>