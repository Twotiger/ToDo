<script setup>
  import SvgIcon from "@/components/SvgIcon.vue";
  import {
    ref,
    onMounted,
    watch
  } from "vue";

  const hour = ref("");
  const minute = ref("");
  const isShowSelect = ref(false);

  const props = defineProps({
    modelValue: {
      type: String,
      default: "23:59"
    }
  })

  onMounted(() => {
    let [h, m] = props.modelValue.split(":")
    hour.value = h
    minute.value = m
  })

  const emit = defineEmits(["update:modelValue"]);

  const options = ref([{
      str: "早上",
      value: "09:00"
    },
    {
      str: "中午",
      value: "12:00"
    },
    {
      str: "下午",
      value: "17:00"
    },
    {
      str: "晚上",
      value: "20:00"
    },
    {
      str: "结束",
      value: "23:59"
    },
  ]);

  const inputHour = (target) => {
    let value = target.value;

    const re = /^(2[0-3]|[0-1]?\d)$/;
    if (re.test(value)) {
      hour.value = value;
    } else {
      target.value = hour.value
    }
    return hour.value
  };

  const inputMinute = (target) => {
    let value = target.value;
    const re =/^([0-5]?\d)$/;
    if (re.test(value)) {
      minute.value = value;
    } else {
      target.value = minute.value
    }
  };

  const showSelect = () => {
    isShowSelect.value = !isShowSelect.value;
  };

  const selectChoice = (item) => {
    let [h, m] = item.value.split(":");
    hour.value = h;
    minute.value = m;
    isShowSelect.value = false;
  };

  watch(hour, () => {
    emit("update:modelValue", `${hour.value}:${minute.value}`)
  })

  watch(minute, () => {
    emit("update:modelValue", `${hour.value}:${minute.value}`)
  })
</script>

<template>
  <div class="time-pick">
  
    <div class="time-pick__time">
      <input class="time-pick__hour" :value="hour" @input.native="inputHour($event.target)" type="text" />
      <span>:</span>
      <input class="time-pick__minute" @input="inputMinute($event.target)" :value="minute" type="text" />
    </div>
    <div class="time-pick__select" @click="showSelect">
      <svg-icon name="arrow_down"></svg-icon>
    </div>

    <div class="time-pick__options" v-show="isShowSelect">
      <div class="time-pick__option" v-for="item in options" @click="selectChoice(item)">
        <div class="time-pick__str">{{ item.str }}</div>
        <div class="time-pick__value">{{ item.value }}</div>
      </div>
    </div>
  </div>
</template>


<style lang="scss" scoped>
  .time-pick {
    position: relative;
    display: flex;
    text-align: right;
    align-items: center;
    width: 100%;
    height: 30px;
    border: 1px solid #ddd;

    .time-pick__time {
      display: flex;
      align-items: center;
      height: 100%;

      .time-pick__hour,
      .time-pick__minute {
        border: none;
        outline: none;
        width: 20px;
        // height: 100%;
      }
    }

    .time-pick__select {
      flex: 1;
      align-items: center;

      .icon {
        width: 15px;
        height: 15px;
      }
    }

    .time-pick__options {
      background: #fff;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
      padding: 10px 0;
      text-align: left;
      position: absolute;

      top: 30px;
      left: 0;
      width: 100%;

      .time-pick__option {
        padding: 0 10px;
        display: flex;
        justify-content: space-between;
        height: 36px;
        line-height: 36px;

        &:hover {
          background: #f4f4f4;
        }

        .time-pick__str {}
      }
    }
  }
</style>