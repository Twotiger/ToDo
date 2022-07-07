//      引入创建虚拟节点和渲染方法
import { createVNode, render } from "vue";
import message from "./message.vue";

const div = document.createElement("div");
document.body.appendChild(div);
let timer = null;

const m = (str, type) => {
    const vnode = createVNode(message, { str, type});
    render(vnode, div);
    timer && clearTimeout(timer);
    timer = setTimeout(() => {
        render(null, div);
    }, 2000);
}

const error = (str) => {
    m(str, "error")
}

const success = (str) => {
    m(str, "success")
}

const warn = (str) => {
    m(str, "warn")
}

export default { error, success, warn }