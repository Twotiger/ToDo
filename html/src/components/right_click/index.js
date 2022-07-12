import { createVNode, render, inject } from "vue";
import RightClickList from "@/components/right_click/rightClickList.vue";
import RightClickGroup from "@/components/right_click/rightClickGroup.vue";
const div = document.createElement("div");

const clickOutsideEvent = (event) => {
  if (!div.contains(event.target)) {
    document.removeEventListener("click", clickOutsideEvent);
    render(null, div);
  }
};

const components = {
  "RightClickList": RightClickList,
  "RightClickGroup": RightClickGroup
}

export default (component, e, id, getTaskGroup) => {
  const { pageX, pageY } = e;
  const vnode = createVNode(components[component], {
    x: pageX,
    y: pageY,
    id,
    close: () => {
      render(null, div);
    },
    getTaskGroup
  });
  document.addEventListener("click", clickOutsideEvent);
  render(vnode, div);
  document.body.appendChild(div);
};
