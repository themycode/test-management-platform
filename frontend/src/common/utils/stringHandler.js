/**
 * 字符串处理函数
 */

// 下划线转换驼峰
function underlineToHump(string) {
  return string.replace(/\_(\w)/g, function(all, letter) {
    return letter.toUpperCase();
  });
}

// 驼峰转换下划线
function humpToUnderline(string) {
  return string.replace(/([A-Z])/g, "_$1").toLowerCase();
}

// 获取给定字符串像素宽度
function getTextPixelWith(text, fontStyle) {
  var canvas = document.createElement("canvas");
  var context = canvas.getContext("2d");
  context.font = fontStyle;
  var dimension = context.measureText(text);
  return dimension.width;
}

export { underlineToHump, humpToUnderline, getTextPixelWith };
