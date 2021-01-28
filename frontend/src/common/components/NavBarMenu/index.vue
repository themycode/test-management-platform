<template>
  <!-- 这里使用div包含以下元素，主要是解决 鼠标移动到菜单目录时，报错：
  element-ui.common.js?ccbf:3687 Uncaught RangeError: Maximum call stack size exceeded.
  at VueComponent.handleMouseenter -->
  <div>
    <el-submenu
      v-if="menu.children && menu.children.length > 0"
      :index="'' + menu.id"
    >
      <template slot="title">
        <i :class="menu.icon"></i>
        <!-- 使用v-if-else解决收起导航时，菜单目录依然显示的问题 -->
        <span
          slot="title"
          v-if="isCollapsed"
          style="height: 0; width: 0;visibility: hidden;
    display: inline-block;"
          >{{ menu.name }}</span
        >
        <span slot="title" v-else>{{ menu.name }}</span>
      </template>
      <NavBarMenu
        v-for="item in menu.children"
        :key="item.id"
        :menu="item"
      ></NavBarMenu>
    </el-submenu>
    <el-menu-item v-else :index="'' + menu.id" @click="handleRoute(menu)">
      <i :class="menu.icon"></i>
      <span slot="title">{{ menu.name }}</span>
    </el-menu-item>
  </div>
</template>

<script>
import { getIFrameUrl, getIFramePath } from "@/common/utils/iframe";

export default {
  name: "NavBarMenu",
  props: ["menu", "isCollapsed"],
  methods: {
    handleRoute(menu) {
      // 如果是嵌套页面，转换成iframe的path
      let path = getIFramePath(menu.url);
      if (!path) {
        path = menu.url;
      }
      // 通过菜单URL跳转至指定路由
      this.$router.push(path);
    }
  }
};
</script>

<style scoped>
</style>
