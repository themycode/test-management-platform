<template>
    <div>
        <!-- 导航栏 -->
        <nav-bar></nav-bar>

        <!-- 主内容区 -->
        <sub-main-content></sub-main-content>
    </div>
</template>

<script>
import NavBar from "./NavBar/NavBar";
import SubMainContent from "./MainContent/SubMainContent";


export default {
    components: {
        NavBar,
        SubMainContent
    },
    mounted() {
        this.$customUtils.headerMenu.initMenuComponent();
        
    }
};
</script>

<style>
</style>


