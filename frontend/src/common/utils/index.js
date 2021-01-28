// 导入所有接口
import customUtils from "./customUtils"

const install = Vue => {
  if (install.installed) return

  install.installed = true

  Object.defineProperties(Vue.prototype, {
    // 注意，此处挂载在 Vue 原型的 $customUtils 对象上
    $customUtils: {
      get() {
        return customUtils
      }
    }
  })
}

export default install
