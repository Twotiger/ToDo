<script setup>
  import {
    ref,
    reactive,
    computed,
    onMounted,
  } from "vue";
  import SvgIcon from "@/components/SvgIcon.vue";
  import TaskInfo from "./TaskInfo.vue"
  import taskApi from "@/api/task";
  import clickOutside from "@/utils/clickoutside"

  const emit = defineEmits(["getTasks", "update:rightComponent"]);

  const tasks = ref([])
  const getSuggestTasks = async () => {
    let data = await taskApi.filterTasks({
      'suggest': true
    })
    tasks.value = data['data']
  }

  const addMyday = async (taskID) => {
    await taskApi.addMyDay(taskID);
    await getSuggestTasks()
    emit("getTasks")
  }

  const completeTask = async (taskID) => {
    await taskApi.completeTask({
      task_id: taskID
    })
    await getSuggestTasks()
    emit("getTasks")
  }

  const hide = () => {
    if (window.innerWidth <= 1000) {
      emit("update:rightComponent", 0)
    }
  }

  onMounted(() => {
    getSuggestTasks()
  })
</script>

<template>
  <div class="suggest" v-click-outside="hide">
    <div class="suggest--panel">
      <h2>建议</h2>
    </div>

    <div class="suggest--panel">
      <div class="task" v-for="task in tasks">
        <div class="task__finish" @click="completeTask(task.id)">
          <svg-icon name="radio"></svg-icon>
        </div>
        <div class="task--text">
          <div class="task--name">{{task.name}}</div>
          <TaskInfo :task="task" />
          <!-- <div class="task--info">{{task.task_list.name}}</div> -->
        </div>

        <div class="task__plus" @click="addMyday(task.id)">
          <svg-icon name="plus" color="#63b0eb"></svg-icon>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .suggest {
    overflow-y: auto;
    right: 0;
    width: 360px;
    height: 100%;
    background: #f3f2f1;
    box-shadow: rgb(0 0 0 / 22%) 0px 5px 5px 0px;
    max-width: 360px;
    z-index: 20;

    @media (max-width: 1000px) {
      position: fixed;
      right: 0;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
    }

    .suggest--panel {
      padding: 20px 16px 12px;

      .task {
        display: flex;
        align-items: center;
        padding: 10px;
        cursor: pointer;
        border-radius: 2px;
        border-bottom: 1px solid #ddd;

        &:hover {
          background: #fafafa;
        }

        &:last-child {
          border-bottom: none;
        }

        .task__finish {
          display: flex;
          align-items: center;

          .icon {
            width: 25px;
            height: 25px;
          }
        }

        .task--text {
          flex: 1;
          display: flex;
          flex-direction: column;
          font-size: 14px;

          .task--name {}
        }

        .task__plus {
          display: flex;
          align-items: center;

          .icon {
            width: 25px;
            height: 25px;
          }
        }
      }
    }
  }
</style>