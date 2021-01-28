<template>
    <div class="tester">
        <el-container>
            <!-- <el-aside style="width:200px">
                <nav-bar></nav-bar>
            </el-aside> -->

            <!-- 主内容区 -->
            <div>
                主内容区41
            </div>
            <!-- <el-main>
                <sub-main-content></sub-main-content>
            </el-main> -->
        </el-container>
    </div>
</template>

<script>
import NavBar from "../NavBar/NavBar";
import SubMainContent from "../MainContent/SubMainContent";

export default {
    components: {
        NavBar,
        SubMainContent
    }
};
</script>

<style scoped>
/* .tester {
    position:relative;
} */
</style>


