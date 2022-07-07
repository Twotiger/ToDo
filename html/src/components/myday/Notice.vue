<script setup>
  import {
    ref,
    computed,
    watch
  } from "vue";
  import SvgIcon from "@/components/SvgIcon.vue";
  import DatePick from "@/components/myday/DatePicker.vue";

  const props = defineProps({
    datetime: {
      type: Object,
      default: {
        str: "",
        value: ""
      },
    },
    showDetail: {
      type: Boolean,
      default: true,
    },
  });
  
  const emit = defineEmits(['updateNotice'])

  const isShow = ref(false);
  const eleLeft = ref(0);
  const eleTop = ref(0);

  const onClick = (e) => {
    let target = e.currentTarget
    if (isShow.value) {
      return;
    }
    const {
      left,
      width,
      height,
      top
    } = target.getBoundingClientRect();
    //元素宽200
    eleLeft.value = Math.max(left + width / 2 - 100, 0);
    eleTop.value = top + height;
    isShow.value = true;
  };

  const hide = () => {
    isShow.value = false;
  };

  const clickToday = () => {
    // 4小时后
    const date = new Date();
    if (date.getHours() > 20) {
      return;
    }
    date.setTime(date.getTime() + 4 * 60 * 60 * 1000);
    props.datetime.value = date
    props.datetime.str = "今天，" + date.getHours() + ":00"
    emit("updateNotice")
    hide();
  };

  const clickTomorrow = () => {
    const today = new Date();
    today.setDate(today.getDate() + 1);
    const tomorrow = new Date(
      today.getFullYear(),
      today.getMonth(),
      today.getDate(),
      9
    );
    props.datetime.value = tomorrow
    props.datetime.str = "明天，" + "9:00"
    emit("updateNotice")
    hide();
  };

  const clickNextWeek = () => {
    const days = nextWeekDays();
    const today = new Date();
    today.setDate(today.getDate() + days);
    const tomorrow = new Date(
      today.getFullYear(),
      today.getMonth(),
      today.getDate(),
      9
    );
    props.datetime.value = tomorrow
    props.datetime.str = "周一，" + "9:00"
    emit("updateNotice")
    hide();
  };

  const deleteDeadline = () => {
    props.datetime.value = ""
    props.datetime.str = ""
    emit("updateNotice")
    hide();
  };

  const getWeek = (date) => {
    const week = date.getDay();
    const arr = ["日", "一", "二", "三", "四", "五", "六"];
    return "周" + arr[week];
  };

  const nextWeekDays = () => {
    // 距离下周还有几天
    const date = new Date();
    let week = date.getDay();
    if (week === 0) week = 7;
    const count = 8 - week;
    return count;
  };

  const calloutGroup = computed(() => {
    if (props.showDetail && props.datetime.str) {
      return "callout-group";
    }
  });

  const todayTime = computed(() => {
    const date = new Date();
    if (date.getHours() >= 20) {
      return "";
    }
    date.setTime(date.getTime() + 4 * 60 * 60 * 1000);
    return date.getHours() + ":00";
  });

  const tomorroTime = computed(() => {
    const now = new Date();
    const newDate = new Date(
      now.getFullYear(),
      now.getMonth(),
      now.getDate() + 1,
      9
    );
    return getWeek(newDate) + "，9:00";
  });

  const greaterTwenty = computed(() => {
    const date = new Date();
    if (date.getHours() >= 20) {
      return true;
    }
    return false;
  });

  const nextWeek = ref("周一，9:00");

  const showTime = (minute) => {
    const date = new Date();
    date.setMinutes(date.getMinutes() + minute)
    return `${date.getHours()}:${date.getMinutes()}`
  }

  const clickCustomer = (minute) => {
    const date = new Date();
    date.setMinutes(date.getMinutes() + minute)
    props.datetime.value = date
    props.datetime.str = `今天，${date.getHours()}:${date.getMinutes()}`
    emit("updateNotice")
    hide();
  }

 const updateNotice = () => {
  emit("updateNotice")
};

  
</script>

<template>
  <div class="callout" @click="onClick" v-click-outside="hide">
    <div class="callout__group" :class="calloutGroup">
      <slot>
        <svg-icon name="small_bell" class="deadline-icon"></svg-icon>
      </slot>
      <span class="date" v-if="showDetail">{{ datetime.str }}</span>
    </div>
    <div v-if="isShow" class="deadline callout-main" :style="{ left: eleLeft + 'px', top: eleTop + 'px' }">
      <div class="callout__content">
        <div class="title">提醒</div>
      </div>

      <div class="callout__content">

        <div class="callout__menu" @click.stop="clickCustomer(25)">
          <div class="text">25分钟后</div>
          <div class="week">{{ showTime(25) }}</div>
        </div>

        <div v-if="!greaterTwenty" class="callout__menu" :class="todayTime" @click.stop="clickToday">
          <div class="text">今天晚些时候</div>
          <div class="week">{{ todayTime }}</div>
        </div>

        <div v-else class="callout__menu disabled">
          <div class="text">今天晚些时候</div>
          <div class="week">{{ todayTime }}</div>
        </div>

        <div class="callout__menu" @click.stop="clickTomorrow">
          <div class="text">明天</div>
          <div class="week">{{ tomorroTime }}</div>
        </div>
        <div class="callout__menu" @click.stop="clickNextWeek">
          <div class="text">下周</div>
          <div class="week">{{ nextWeek }}</div>
        </div>
      </div>

      <div class="callout__content">
        <div class="callout__menu">
          <DatePick :datetime="datetime" @updateParent="updateNotice"/>
        </div>
      </div>

      <div class="callout__content" v-if="datetime.str">
        <div class="callout__menu" @click.stop="deleteDeadline">
          <div class="week del">删除提醒</div>
        </div>
      </div>
    </div>
  </div>
</template>


<style lang="scss" scoped>
  .callout {
    width: 100%;
    display: inline-block;

    .callout-group {
      background: #fff;
      padding: 0 5px;
      margin-right: 5px;
      border-radius: 2px;
    }

    .callout__group {
      display: flex;
      align-items: center;

      .deadline-icon {
        width: 24px;
        height: 24px;
      }

      .date {
        font-size: 13px;
        color: #323130;
      }
    }

    .callout-button:hover {
      background: #ccc;
    }

    display: inline-block;

    .deadline {
      z-index: 99;
      border-radius: 2px;
      position: fixed;
      width: 200px;
      background: #fff;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);

      .callout__content {
        border-bottom: solid 1px #ddd;
      }

      .callout__content:nth-last-child(1) {
        border: none;
      }

      .title {
        padding: 8px 8px 12px;
        font-size: 14px;
        font-weight: 700;
        text-align: center;
        font-weight: 700px;
      }

      .callout__menu {
        display: flex;
        align-items: center;
        height: 36px;
        cursor: pointer;
        color: #323130;
        font-size: 14px;
        padding: 0 4px;
        margin: 4px 0;

        .text {
          flex: 1;
        }

        .week {
          color: var(--font-color-tertiary);
        }

        .week.del {
          color: var(--font-color-warning);
        }

        &:hover {
          background: #ddd;
        }
      }

      .disabled {
        color: #ddd;
        cursor: not-allowed;
      }
    }
  }
</style>