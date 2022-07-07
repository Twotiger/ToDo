<script setup>
import {
  ref,
  computed,
  watch
} from "vue";
import moment from "moment";
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
    default: true
  }
});

const emit = defineEmits(["updateDeadline"]);

const updateMyday = () => {
  emit("updateDeadline")
};

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
  let today = new Date();
  today = new Date(
    today.getFullYear(),
    today.getMonth(),
    today.getDate(),
    23,
    59
  );

  props.datetime.value = today
  props.datetime.str = "今天"
  emit("updateDeadline")
  hide();
};

const clickTomorrow = () => {
  let today = new Date();
  today.setDate(today.getDate() + 1);
  const tomorrow = new Date(
    today.getFullYear(),
    today.getMonth(),
    today.getDate(),
    23,
    59
  );
  props.datetime.value = tomorrow
  props.datetime.str = "明天"
  emit("updateDeadline")

  hide();
};

const clickNextWeek = () => {
  let today = new Date();
  let week = today.getDay();
  if (week === 0) week = 7;
  const count = 8 - week;
  today.setDate(today.getDate() + count);
  const nextWeek = new Date(
    today.getFullYear(),
    today.getMonth(),
    today.getDate(),
    23,
    59
  );
  props.datetime.value = nextWeek
  props.datetime.str = "下周"
  emit("updateDeadline")

  hide();
};

const deleteDeadline = () => {
  props.datetime.value = ''
  props.datetime.str = ""
  emit("updateDeadline")

  hide();
};


const getWeek = (date) => {
  // 返回date是周几
  const week = date.getDay();
  const arr = ["日", "一", "二", "三", "四", "五", "六"];
  return "周" + arr[week];
};

const calloutStatus = computed(() => {
  if (props.showDetail && props.datetime.str) {
    return "callout__group--choice";
  }
});

const todayWeek = computed(() => {
  const date = new Date();
  return getWeek(date);
});

const tomorrowWeek = computed(() => {
  const date = new Date();
  date.setTime(date.getTime() + 24 * 60 * 60 * 1000);
  return getWeek(date);
});

const nextWeek = computed(() => {
  const date = new Date();
  let week = date.getDay();
  if (week === 0) week = 7;
  const count = 8 - week;
  date.setTime(date.getTime() + 24 * 60 * 60 * 1000 * count);
  return getWeek(date);
});
</script>

<template>
  <div class="callout" @click="onClick" v-click-outside="hide">
    <div class="callout__group" :class="calloutStatus">
      <slot>
        <svg-icon name="date" class="callout__icon" />
      </slot>
      <span class="callout__caption" v-if="showDetail">{{ datetime.str }}</span>
    </div>

    <div v-if="isShow" class="callout__main" :style="{ left: eleLeft + 'px', top: eleTop + 'px' }">
      <div class="callout__content">
        <div class="callout__title">截止</div>
      </div>
      <div class="callout__content">
        <div class="callout__menu" @click.stop="clickToday">
          <div class="callout__text">今天</div>
          <div class="callout__value">{{ todayWeek }}</div>
        </div>
        <div class="callout__menu" @click.stop="clickTomorrow">
          <div class="callout__text">明天</div>
          <div class="callout__value">{{ tomorrowWeek }}</div>
        </div>
        <div class="callout__menu" @click.stop="clickNextWeek">
          <div class="callout__text">下周</div>
          <div class="callout__value">{{ nextWeek }}</div>
        </div>
      </div>

      <div class="callout__content">
        <div class="callout__menu">
          <DatePick :datetime="datetime" @updateParent="updateMyday"/>
        </div>
      </div>
      <div class="callout__content" v-if="datetime.str">
        <div class="callout__menu" @click.stop="deleteDeadline">
          <div class="callout__value callout__value--del">删除截止日期</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.callout {
  width: 100%;
  display: inline-block;

  .callout__group--choice {
    background: #fff;
    padding: 0 5px;
    margin: 0 5px;
    border-radius: 2px;
  }

  .callout__group {
    display: flex;
    align-items: center;

    .callout__icon {
      width: 24px;
      height: 24px;
    }

    .callout__caption {
      font-size: 13px;
      color: var(--font-color-primary);
    }
  }

  .callout__main {
    z-index: 110;
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

    .callout__title {
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
      color: var(--font-color-primary);
      font-size: 14px;
      margin: 4px 0;
      padding: 0 4px;

      .callout__text {
        flex: 1;
      }

      .callout__value {
        color: var(--font-color-tertiary);
      }

      .callout__value--del {
        color: var(--font-color-warning);
      }

      &:hover {
        background: var(--bg-secondary);
      }
    }
  }
}
</style>