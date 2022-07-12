<script setup>
import taskApi from "@/api/task_list";

const props = defineProps({
  id: Number,
  x: Number,
  y: Number,
  close: Function,
  getTaskGroup: Function,
});

const deleteTaskList = async () => {
  await taskApi.deleteTaskList(props.id);
  props.getTaskGroup();
  props.close(); // 关闭
};
</script>

<template>
  <div class="menu" :style="{ top: y + 'px', left: x + 'px' }">
    <div class="menu--item delete" @click="deleteTaskList">删除列表</div>
  </div>
</template>


<style lang="scss" scoped>
.menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 100px;
  background: #fff;
  border: solid 1px #ddd;
  padding: 5px 0;
  border-radius: 2px;
  box-sizing: border-box;
  width: 200px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
}

.menu--item {
  box-sizing: border-box;
  padding: 4px 8px;
  height: 36px;
  cursor: pointer;
  display: flex;
  align-items: center;

  &:hover {
    background: var(--bg-hover);
  }
}

.menu--item.delete {
  color: var(--font-color-warning);
}
</style>

