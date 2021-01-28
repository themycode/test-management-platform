/**
 * Cookie相关操作
 */

// 根据指定cookie名称获取value值
export const getCookieValue = key => {
  let cookies = document.cookie.split(";") // 获取每个cookie项(不含会话id)
  let value = null
  for (let i in cookies) {
    let kv = cookies[i].split("=") // 每个cookie项的名称和cookie的值
    let temp_key = kv[0].replace(" ", "") // 获取的cookie项有多个值，第二个开始，键 的值 的左侧会加个空格
    if (key == temp_key) {
      value = kv[1]
      break
    }
  }
  return value
}
