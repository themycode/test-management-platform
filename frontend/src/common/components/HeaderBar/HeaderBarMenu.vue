<template>
  <el-menu-item :index="''+menu.id" @click="handleRoute(menu)">
    <i :class="menu.icon"></i>{{menu.name}}
  </el-menu-item>
</template>

<script>

export default {
  name: "HeaderBarMenu",
  props: {
    menu: {
      type: Object,
      required: true
    },
    activeIndex:{
        type:String,
        required:true
    }
  },
  methods: {
    handleRoute(menu) {
        if (menu.id == this.activeIndex){ // 如果被点击菜单已经是当前菜单，则无动作
            return;
        }
      this.$router.push(menu.url);
    }
  }
  
};
</script>

<style scoped lang="scss">
</style>