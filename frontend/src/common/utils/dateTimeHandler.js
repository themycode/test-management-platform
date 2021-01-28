// 转日期对象为字符串
export const dateToString = date => {
  let year = date.getFullYear()
  let month = (date.getMonth() + 1).toString()
  let day = date.getDate().toString()
  if (month.length == 1) {
    month = "0" + month
  }

  if (day.length == 1) {
    day = "0" + day
  }

  return year + "-" + month + "-" + day
}


// 转换日期时间为字符串
export const datetimeToString = (date) => {
  let year = date.getFullYear();
  let month = (date.getMonth() + 1).toString();
  let day = date.getDate().toString();
  if (month.length == 1) {
    month = "0" + month;
  }
  if (day.length == 1) {
    day = "0" + day;
  }
  var hours = date.getHours().toString();
  if (hours.length == 1) {
    hours = "0" + hours;
  }
  var mintus = date.getMinutes().toString();
  if (mintus.length == 1) {
    mintus = "0" + mintus;
  }
  var second = date.getSeconds().toString();
  if (second.length == 1) {
    second = "0" + second;
    }
    
  var dateTime =
    year + "-" + month + "-" + day + " " + hours + ":" + mintus + ":" + second;
  return dateTime;
}
