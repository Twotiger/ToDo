<script setup>
  import SvgIcon from "@/components/SvgIcon.vue";
  import {
    ref,
    reactive,
    computed,
    watch
  } from "vue";
  // import IntervalPicker from "@/components/myday/IntervalPicker.vue";
  import {
    myday
  } from './myday.js'

  const isShow = ref(false);
  const eleLeft = ref(0);
  const eleTop = ref(0);

  const emit = defineEmits(["updateRepeat"])

  const props = defineProps({
    repeat: {
      type: Object,
      default: {
        interval: 1,
        intervalType: '',
        type: '',
        weekdays: [],
      }
    },
    showDetail: { // 区别在myday里面用,还是在Detail.vue里面用
      type: Boolean,
      default: true
    }
  });

  const calloutStatus = computed(() => {
    if (props.showDetail && props.repeat.intervalType) {
      return "callout__group--choice";
    }
  });

  const onClick = (e) => {
    let target = e.currentTarget;
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
    eleTop.value = top + height
    isShow.value = true;
  };

  const hide = () => {
    isShow.value = false;
  };

  const clear = () => {
    props.repeat.interval = 1
    props.repeat.intervalType = ""
    props.repeat.weekdays = []
    props.repeat.type = ''
  }

  const deleteRepeat = () => {
    // 删除重复
    clear()
    update()
    hide();
  };

  const getWeek = (date) => {
    const week = date.getDay();
    const arr = ["日", "一", "二", "三", "四", "五", "六"];
    return "周" + arr[week];
  };

  const clickDaily = () => {
    props.repeat.interval = 1
    props.repeat.intervalType = "Daily"
    props.repeat.weekdays = []
    props.repeat.type = ''
    update()
    hide();
  };

  const clickWeekDays = () => {
    props.repeat.interval = 1
    props.repeat.intervalType = "WeekDays"
    props.repeat.weekdays = []
    props.repeat.type = ''
    update()
    hide();
  };

  const clickWeekly = () => {
    props.repeat.interval = 1
    props.repeat.intervalType = "Weekly"
    props.repeat.weekdays = []
    props.repeat.type = ''
    update()
    hide();
  };

  const clickMonthly = () => {
    props.repeat.interval = 1
    props.repeat.intervalType = "Monthly"
    props.repeat.weekdays = []
    props.repeat.type = ''
    update()
    hide();
  };

  const clickYearly = () => {
    props.repeat.interval = 1
    props.repeat.intervalType = "Yearly"
    props.repeat.weekdays = []
    props.repeat.type = ''
    update()
    hide();
  };

  const todayWeek = computed(() => {
    const date = new Date();
    return this.getWeek(date);
  });

  const tomorrowWeek = computed(() => {
    const date = new Date();
    date.setTime(date.getTime() + 24 * 60 * 60 * 1000);
    return getWeek(date);
  });


  const {
    humanizeRepeat
  } = myday()

  const update = () => {
    emit("updateRepeat")
  }
</script>

<template>

  <div class="callout" @click="onClick" v-click-outside="hide">
    <div class="callout__group" :class="calloutStatus">
      <slot>
        <svg-icon name="repeat"></svg-icon>
      </slot>
      <span class="date" v-if="showDetail">{{ humanizeRepeat(props.repeat) }}</span>
    </div>
    <div v-if="isShow" class="deadline callout-main" :style="{ left: eleLeft + 'px', top: eleTop + 'px' }">
      <div class="callout-content">
        <div class="title">重复</div>

      </div>
      <div class="callout-content">
        <div class="menu" @click.stop="clickDaily">
          <div class="text">每天</div>
        </div>
        <div class="menu" @click.stop="clickWeekDays">
          <div class="text">工作日</div>
        </div>
        <div class="menu" @click.stop="clickWeekly">
          <div class="text">每周</div>
        </div>
        <div class="menu" @click.stop="clickMonthly">
          <div class="text">每月</div>
        </div>
        <div class="menu" @click.stop="clickYearly">
          <div class="text">每年</div>
        </div>
      </div>

      <!-- <div class="callout-content">
        <div class="menu">
          <IntervalPicker :custom="repeat" @update="update" />
        </div>
      </div> -->
      <div class="callout-content" v-if="repeat.intervalType">
        <div class="menu" @click.stop="deleteRepeat">
          <div class="week del">从不重复</div>
        </div>
      </div>
    </div>
  </div>
</template>


<style lang="scss" scoped>
  .callout {
    width: 100%;

    .callout__group--choice {
      background: #fff;
      padding: 0 5px;
      margin: 0 5px;
      border-radius: 2px;
    }

    .callout-group {
      background: #fff;
      padding: 0 5px;
      margin: 0 5px;
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

      .callout-content {
        border-bottom: solid 1px #ddd;
      }

      .callout-content:nth-last-child(1) {
        border: none;
      }

      .title {
        padding: 8px 8px 12px;
        font-size: 14px;
        font-weight: 700;
        text-align: center;
        font-weight: 700px;
      }

      .menu {
        display: flex;
        align-items: center;
        height: 36px;
        cursor: pointer;
        color: #323130;
        font-size: 14px;
        margin: 4px 0;
        padding: 0 4px;

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
          background: #f3f2f1;
        }
      }
    }
  }
</style>