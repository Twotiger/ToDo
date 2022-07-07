<script setup>
import SvgIcon from "@/components/SvgIcon.vue";
import TaskInfo from "@/components/myday/TaskInfo.vue"
import taskApi from "@/api/task";
const props = defineProps({
  task: {
    type: Object,
    default: {
      name: '',
      id: '',
      deadline: '',
      repeat: {},
      notice: '',
      task_list: {}
    }
  }
})

const emit = defineEmits(["getTasks", "showDetail"])

const showDetail = () => {
  emit("showDetail", props.task.id)
}
const completeTask = async () => {
  await taskApi.completeTask({
    task_id: props.task.id
  });
  emit("getTasks");
}

const deleteImportant = async () => {
  await taskApi.deleteImportant(props.task.id)
  emit("getTasks");
}
const addImportant = async () => {
  await taskApi.addImportant(props.task.id)
  emit("getTasks");
}
</script>

<template>
  <div class="todo" @click="showDetail(task.id)">
    <svg-icon name="radio" @click.stop="completeTask(task.id)" />

    <div class="contant">
      <div class="title">{{ task.name }}</div>
      <task-info :task="task" />
    </div>

    <div class="important_icon">
      <svg-icon name="star_select" @click.stop="deleteImportant" v-if="task.is_important"></svg-icon>
      <svg-icon name="star" @click.stop="addImportant" v-else></svg-icon>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.todo {
  border-bottom: solid 1px #ddd;
  cursor: pointer;
  min-height: 52px;
  max-height: 52px;

  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 0 8px;

  &:hover {
    background: var(--bg-hover);
  }

  .icon {
    height: 30px;
    width: 30px;
    display: inline-block;
  }

  .contant {
    display: flex;
    flex-direction: column;
    flex: 1;
    font-size: 14px;
    padding: 8px 12px;

    .title {
      display: flex;
      align-items: center;
      font-size: 14px;
      color: #323130;


      .icon-down {
        transform: rotate(90deg);
        transition-duration: 0.25s;
      }

      .icon-right {
        transform: rotate(0deg);
        transition-duration: 0.25s;
      }

      .icon {
        width: 15px;
        height: 15px;
        margin-right: 10px;
      }
    }

    .info {
      .icon {
        width: 12px;
        height: 12px;
      }
    }
  }

  .important_icon {
    .icon {
      width: 15px;
      height: 15px;

      &:hover {
        transform: scale(1.2)
      }
    }
  }

  border-radius: 2px;
}
</style>