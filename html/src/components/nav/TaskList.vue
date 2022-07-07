<script setup>
  import {
    useRouter
  } from 'vue-router'
  import SvgIcon from "@/components/SvgIcon.vue"


  const props = defineProps({
    data: Object,
  });

  let router = useRouter()

  const jump = (listID) => {
    router.push({
      path: `/task/${listID}`
    })
  }
</script>

<template>
  <div class="task-list" @click="jump(data.id)">
    <svg-icon name="task_list" />
    <span class="text">{{ data.name }}</span>
    <span class="count">{{ data.count }}</span>
  </div>
</template>

<style lang="scss" scoped>
  .task-list {
    cursor: pointer;
    padding: 0 12px;
    height: 36px;
    display: flex;
    align-items: center;
    color: #323100;
    font-size: 14px;

    .text {
      flex: 1;
      margin-left: 10px;
    }

    .icon {
      width: 20px;
      height: 20px;
    }
  }

  .task-list:hover {
    background: #fff;
  }
</style>