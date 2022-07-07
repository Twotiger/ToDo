<script setup>
import SvgIcon from "@/components/SvgIcon.vue";
import {
  myday
} from "./myday.js"

const {
  humanizeDate,
  humanizeDatetime
} = myday()
const props = defineProps({
  task: {
    type: Object,
    default: {
      id: '',
      notice: "",
      deadline: '',
      repeat: Object,
      task_list: {}
    }
  }
})
</script>

<template>
  <div class="info">
    <span>{{ props.task.task_list.name }}</span>
    <span class="deadline" v-if="props.task.deadline">
      <svg-icon name="dot" />
      <svg-icon name="date"></svg-icon>
      {{ humanizeDate(props.task.deadline) }}
      <svg-icon v-if="props.task.repeat.intervalType" name="repeat"></svg-icon>
    </span>

    <span class="notice" v-if="props.task.notice">
      <svg-icon name="dot" />
      <svg-icon name="small_bell"></svg-icon>
      {{ humanizeDatetime(props.task.notice) }}
    </span>
    <!-- {{props.id}} -->
  </div>
</template>

<style lang="scss" scoped>
.info {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #797775;


  .deadline,
  .notice {
    display: flex;
    align-items: center;

    .icon {
      width: 12px;
      height: 12px;
    }
  }

  .icon {
    width: 12px;
    height: 12px;
  }
}
</style>