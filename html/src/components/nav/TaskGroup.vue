<script setup>
import { reactive, computed, inject } from "vue";
import TaskList from "./TaskList.vue";
import SvgIcon from "@/components/SvgIcon.vue";
import showMenu from "@/components/right_click/index.js";

import { useRouter } from "vue-router";

const props = defineProps({
  data: Object,
  enterGroup: Object,
  openGroup: Array,
});

const emit = defineEmits([
  "dragstart",
  "drop",
  "dragenter",
  "dropToEmpty",
  "dragleave",
  "update:enterGroup",
]);

const router = useRouter();

const dragstart = (e, lid) => {
  emit("dragstart", e, lid);
};

const dragenter = (e, lid) => {
  emit("dragenter", e, lid);
};

const dropToEmpty = (e, id) => {
  emit("dropToEmpty", e, id);
};

const dragleave = (e, id) => {
  emit("dragleave", e, id);
};

const showGroup = () => {
  let index = props.openGroup.indexOf(props.data.id);
  if (index === -1) {
    props.openGroup.push(props.data.id);
  } else {
    props.openGroup.splice(index, 1);
  }
};

const drop = (e, id) => {
  emit("drop", e, id);
};

const getClass = (id) => {
  return router.currentRoute.value.params["listID"] === id.toString()
    ? "active"
    : "";
};

const getTaskGroup = inject("getTaskGroup");

const contextmenu = (e) => {
  showMenu("RightClickGroup", e, props.data.id, getTaskGroup);
  e.preventDefault();
};
</script>

<template>
  <div class="task-group" @click="showGroup" @contextmenu="contextmenu">
    <svg-icon name="task_group" />
    <span class="text">{{ data.name }}</span>
    <svg-icon
      name="arrow_left"
      class="m0"
      :class="openGroup.includes(data.id) ? 'icon-down' : 'icon-left'"
    />
  </div>

  <div
    v-if="openGroup.includes(data.id)"
    class="children"
    v-for="child in data.children"
    :key="child.id"
  >
    <!-- 列表渲染children -->
    <div
      class="drag"
      :class="getClass(child.id)"
      draggable="true"
      @dragover.prevent
      @dragenter="dragenter($event, child.id)"
      @dragstart.stop="dragstart($event, child.id)"
      @dragleave="dragleave($event, child.id)"
      @drop.stop="drop($event, child.id)"
    >
      <TaskList :data="child" />
    </div>
  </div>

  <div
    v-if="openGroup.includes(data.id) && data.children.length === 0"
    class="children"
  >
    <!-- 如果是空组 -->
    <div
      class="dragEmpty"
      @dragstart.stop
      @dragover.prevent
      @dragleave="dragleave($event, data.id)"
      @dragenter="dragenter($event, data.id)"
      @drop.stop="dropToEmpty($event, data.id)"
    >
      拖拽到此处添加列表
    </div>
  </div>
</template>

<style lang="scss" scoped>
.active {
  font-weight: 700;
  background: #fff;
}

.task-group {
  cursor: pointer;
  padding: 0 12px;
  height: 36px;
  display: flex;
  align-items: center;
  color: #323100;
  font-size: 14px;

  .icon-down {
    transform: rotate(-90deg);
    transition-duration: 0.25s;
  }

  .icon-left {
    transform: rotate(0deg);
    transition-duration: 0.25s;
  }

  .text {
    flex: 1;
    margin-left: 10px;
  }

  .icon {
    width: 20px;
    height: 20px;
  }
}

.task-group:hover {
  background: #fff;
}

.children {
  border-left: solid 2px #a19f9d;
  margin-left: 19px;

  .border {
    border: solid 2px #a19f9d;
  }

  .dragEmpty {
    padding: 0 12px;
    height: 36px;
    display: flex;
    align-items: center;
    color: #323100;
    font-size: 14px;
  }
}
</style>