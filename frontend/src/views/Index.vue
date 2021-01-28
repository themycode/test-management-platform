<template>
    <div class="root-page">
        <el-container>
            <!-- 顶部导航栏 -->
            <el-header class="page-header">
                <keep-alive>
                    <header-bar></header-bar>
                </keep-alive>
            </el-header>

            <!-- 主内容区 -->
            <el-main class="page-body">
                <main-content></main-content>
            </el-main>

            <!-- 底部区 -->
            <el-footer class="page-footer">
                <keep-alive>
                    <Footer></Footer>
                </keep-alive>
            </el-footer>
        </el-container>
    </div>
</template>

<script>
import HeaderBar from "./HeaderBar/HeaderBar";
import MainContent from "./MainContent/MainContent";
import Footer from "./Footer/Footer";

export default {
    data() {
        return {};
    },
    components: {
        HeaderBar,
        MainContent,
        Footer,
    },
};
</script>

<style lang="scss" scoped>
.root-page {
    position: absolute;
    left: 0px;
    right: 0px;
    top: 0px;
    bottom: 0px;
    overflow: hidden;

    .page-header {
        position: absolute;
        height: 60px !important; // 导航菜单组件会占用到61
        left: 0px ;
        right: 0px ;
        padding: 0px ;
    }

    .page-body {
        position: absolute;
        top: 62px;
        bottom: 40px;
        left: 0px;
        right: 0px;
        padding: 0px;
        overflow: hidden;
    }

    .page-footer {
        position: absolute;
        bottom: 0px;
        height: 40px !important;
        line-height: 40px;
        left: 0px;
        right: 0px;
        padding: 0px;
        overflow: hidden;
    }
}
</style>
