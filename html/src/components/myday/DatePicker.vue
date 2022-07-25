<script setup>
import SvgIcon from "@/components/SvgIcon.vue";
import Calendar from "@/utils/calendar";
import TimePicker from "@/components/myday/TimePicker.vue";
import moment from "moment";
import { ref } from "vue";

const isShow = ref(false);
const eleLeft = ref(0);
const eleTop = ref(0);
// const popover = ref(null);

const props = defineProps({
  datetime: {
    type: Object,
    default: {
      str: "",
      value: "",
    },
  },
});

const emit = defineEmits(["updateParent"]);

const calendar = ref(new Calendar());

const mouseenter = (e) => {
  if (isShow.value) {
    return;
  }
  const { width, height, right, bottom } = e.target.getBoundingClientRect();
  // DatePicker宽222
  const datePickerWidth = 222;
  const datePickerHeight = 350;
  if (right + datePickerWidth > document.body.clientWidth) {
    eleLeft.value = -datePickerWidth;
  } else {
    eleLeft.value = width;
  }
  eleLeft.value = Math.max(eleLeft.value, 0); // 修正,适应小屏幕

  eleTop.value = 0;
  if (window.innerHeight < bottom + datePickerHeight){
    eleTop.value = -datePickerHeight
  }
  // 修正,适应小屏幕
  isShow.value = true;
};

const weeks = ["一", "二", "三", "四", "五", "六", "日"];

const getDays = () => {
  return calendar.value.getDays();
};

let now = new Date();
now.setHours(0);
now.setMinutes(0);
const choiceDay = ref(now);

const choice = (date) => {
  choiceDay.value = date;
};

const time = ref("23:59"); // 传递给子组件

const save = () => {
  let [h, m] = time.value.split(":");
  choiceDay.value.setHours(h);
  choiceDay.value.setMinutes(m);

  props.datetime.str = moment(choiceDay.value).fromNow();
  props.datetime.value = choiceDay.value;

  isShow.value = false;
  emit("updateParent");
};

// 是否是同一天
const sameDay = (a, b) => {
  if (
    a.getFullYear() == b.getFullYear() &&
    a.getMonth() == b.getMonth() &&
    a.getDate() == b.getDate()
  ) {
    return true;
  }
  return false;
};

const buttonClass = (day) => {
  if (!day) {
    return "";
  }
  let c = "";
  if (sameDay(choiceDay.value, day)) {
    c += "popover_button--choice ";
  }

  if (sameDay(now, day)) {
    return "popover_button--today";
  }

  c +=
    day.getMonth() === calendar.value.month ? "" : "popover__button--secondary";
  return c;
};

const clickNextMonth = () => {
  calendar.value.nextMonth();
  getDays();
};

const clicklastMonth = () => {
  calendar.value.lastMonth();
  getDays();
};
</script>


<template>
  <div class="datepick" @mouseenter="mouseenter">
    <div class="datepick__choice">选择日期</div>
    <div class="datepick__icon">
      <svg-icon name="arrow_right"></svg-icon>
    </div>
    <div
      class="popover"
      ref="popover"
      v-if="isShow"
      :style="{ left: eleLeft + 'px', top: eleTop + 'px' }"
    >
      <div class="popover__title">选择日期</div>
      <div class="popover__content">
        <div class="popover__header">
          <span class="popover__caption"
            >{{ calendar.year }}年 {{ calendar.month + 1 }}月
          </span>
          <svg-icon name="up" @click="clicklastMonth" />
          <svg-icon name="down" @click="clickNextMonth" />
        </div>
        <div class="popover__main">
          <table>
            <thead>
              <tr>
                <th v-for="weekName in weeks">
                  <button class="popover__button">{{ weekName }}</button>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="week in getDays()">
                <th v-for="day in week">
                  <button
                    class="popover__button"
                    @click="choice(day)"
                    :class="buttonClass(day)"
                  >
                    {{ day.getDate() }}
                  </button>
                </th>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="popover__time-picker">
          <TimePicker v-model="time" />
        </div>

        <div class="popover__footer">
          <button class="button primary" z-index="-1" @click="save">
            保存
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.datepick {
  user-select: none;
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  z-index: 99;

  .datepick__choice {
    flex: 1;
  }

  .datepick__icon {
    user-select: none;

    .icon {
      width: 14px;
      height: 14px;
    }
  }

  .popover {
    border-radius: 2px;

    position: absolute;
    background-color: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);

    .popover__title {
      padding: 8px 8px 12px;
      font-size: 14px;
      font-weight: 700;
      text-align: center;
      font-weight: 700px;
      border-bottom: 1px solid #ddd;
    }

    .popover__content {
      padding: 12px;

      .popover__header {
        display: flex;
        align-items: center;
        height: 28px;
        line-height: 28px;
        font-weight: 600;

        .popover__caption {
          flex: 1;
        }

        .icon {
          width: 15px;
          height: 15px;

          &:hover {
            background: #f4f4f4;
          }
        }
      }

      .popover__main {
        .popover__button {
          background-color: inherit;
          border: none;
          cursor: pointer;
          width: 24px;
          height: 24px;
          color: var(--font-color-primary);
          font-family: "Microsoft Yahei", 微软雅黑, STXihei, "Meiryo UI", Meiryo,
            メイリオ, "ＭＳ Ｐゴシック", "MS PGothic",
            "Hiragino Kaku Gothic Pro", "Arial Unicode MS", "Helvetica Neue",
            Helvetica, Arial, sans-serif;
          font-size: 12px;

          &:hover {
            background: #f4f4f4;
          }
        }

        .popover__button--secondary {
          color: var(--font-color-secondary);
        }

        .popover_button--choice {
          background-color: var(--bg-brand-secondary);
        }

        .popover_button--today {
          background-color: var(--bg-brand);
          color: var(--bg-primary);
          border-radius: 2px;

          &:hover {
            background-color: var(--bg-brand);
          }
        }
      }

      .popover__time-picker {
        margin: 10px 0;
      }

      .popover__footer {
        display: flex;
        justify-content: flex-end;
      }
    }
  }
}
</style>