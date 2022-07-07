<script setup>
import SvgIcon from "@/components/SvgIcon.vue";
import {
  ref,
  computed,
  watch,
  reactive,
  onMounted
} from "vue";

const isShow = ref(false)
const eleLeft = ref(0)
const eleTop = ref(0)

const mouseenter = (e) => {
  if (isShow.value) {
    return;
  }
  const {
    width,
    height,
    right
  } = e.target.getBoundingClientRect();

  let pickerWidth = 200;
  if (repeat.value.intervalType == "Weekly") {
    pickerWidth = 266;
  }
  if (right + pickerWidth > document.body.clientWidth) {
    eleLeft.value = -pickerWidth;
  } else {
    eleLeft.value = width;
  }

  eleTop.value = height;
  isShow.value = true;
};

const props = defineProps({
  custom: {
    type: Object,
    default: {
      interval: 1,
      intervalType: 'Daily',
      type: 'custom',
      weekdays: [],
    }
  }
})
const repeat = ref({
  interval: 1,
  intervalType: 'Daily',
  type: 'custom',
  weekdays: [],
})

const emit = defineEmits(["update"]);

const save = () => {
  isShow.value = false
  props.custom.interval = repeat.value.interval
  props.custom.intervalType = repeat.value.intervalType
  props.custom.type = "custom"
  props.custom.weekdays = repeat.value.weekdays
  emit("update")
}

const week = [{
  str: "一",
  value: "Monday"
}, {
  str: "二",
  value: "Tuesday"
}, {
  str: "三",
  value: "Wednesday"
}, {
  str: "四",
  value: "Thursday"
}, {
  str: "五",
  value: "Friday"
}, {
  str: "六",
  value: "Saturday"
}, {
  str: "日",
  value: "Sunday"
}]

const selectWeek = (week) => {
  const index = repeat.value.weekdays.indexOf(week)
  if (index === -1) {
    repeat.value.weekdays.push(week)
  } else {
    repeat.value.weekdays.splice(index, 1)
  }
}

onMounted(() => {
  repeat.value.interval = props.custom.interval
  if (props.custom.intervalType) {
    repeat.value.intervalType = props.custom.intervalType
  } else {
    repeat.value.intervalType = "Daily"
  }

  repeat.value.weekdays = props.custom.weekdays
})

</script>


<template>
  <div class="picker" @mouseenter="mouseenter">
    <div class="picker--text">
      自定义
    </div>
    <svg-icon name="arrow_right"></svg-icon>

    <div class="popover" v-if="isShow" :style="{ left: eleLeft + 'px', top: 0 + 'px' }">
      <div class="popover--title">重复周期</div>

      <div class="popover--content">
        <div class="content--row">
          <input type="number" v-model="repeat.interval" class="content__interval">
          <select name="interval" v-model="repeat.intervalType" class="content__interval-type">
            <option value="Daily">天</option>
            <option value="Weekly">周</option>
            <option value="Monthly">月</option>
            <option value="Yearly">年</option>
          </select>
        </div>

        <div class="content--row" v-if="repeat.intervalType === 'Weekly'">
          <div class="week">
            <template v-for="item in week">

              <div class="week__choice" :class="repeat.weekdays.indexOf(item.value) !== -1 ? 'selected' : ''"
                @click="selectWeek(item.value)">
                {{ item.str }}
              </div>
            </template>
          </div>
        </div>

        <div class="content--footer">
          <button class="button primary" @click="save">保存</button>
        </div>
      </div>


    </div>
  </div>
</template>

<style lang="scss" scoped>
.picker {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;

  .picker--text {
    flex: 1;

  }

  .icon {
    width: 20px;
    height: 20px;
  }
}

.popover {
  position: absolute;
  z-index: 99;
  min-width: 200px;
  // height: 200px;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);

  .popover--title {
    padding: 8px 8px 12px;
    font-size: 14px;
    font-weight: 700;
    text-align: center;
    font-weight: 700px;
    border-bottom: 1px solid #ddd;


  }

  .popover--content {
    display: flex;
    align-items: center;
    flex-direction: column;
    padding: 6px;


    .content--row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      width: 100%;

      .content__interval {
        box-sizing: border-box;
        width: 50px;
        outline: none;
        border: 1px solid #ddd;
        height: 27px;
        margin-right: 6px;
      }

      .content__interval-type {
        box-sizing: border-box;
        width: 50px;
        outline: none;
        border: 1px solid #ddd;
        height: 27px;
        flex: 1;
      }

      .week {
        display: flex;
        align-items: center;
        border: 1px solid #ddd;

        .week__choice {
          display: flex;
          align-items: center;
          justify-content: space-around;
          width: 36px;
          height: 36px;
        }

        .week__choice.selected {
          color: #fff;
          background-color: #2564cf;
        }
      }
    }

    .content--footer {
      width: 100%;
      display: flex;
      justify-content: flex-end;
    }
  }
}
</style>