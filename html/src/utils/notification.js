export function notification(message, body) {
  if (Notification.permission === "granted") {
    new Notification(message, {
      "body": body,
      "icon": "https://s2.loli.net/2022/07/05/7aXR1N5eCT9p3Do.png"
    });
  }
}     

export function requestPermission() {
  if (!("Notification" in window)) {

    console.log("浏览器不支持Notification");
    return
  }
  if (Notification.permission !== "granted") {
    Notification.requestPermission();
  }
}

Notification.onclick = function (event) {
  console.log("Notification.click");
}