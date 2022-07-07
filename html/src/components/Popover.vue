<template>
  <div class="callout" @click="onClick" v-click-outside="hide">
    <div :class="calloutGroup">
      <slot class="callout-icon" :deadline="deadline"></slot>
    </div>
    <div v-if="isShow" class="deadline callout-main" :style="{ left: eleLeft + 'px' }">
      <div class="callout-content">
        <div class="title">{{ title }}</div>
      </div>
    </div>

  </div>
</template>

<script>
import clickOutside from "@/utils/clickoutside"
export default {

  directives: { 'click-outside': clickOutside },
  props() {
    title: String
  },
  data() {
    return {
      isShow: false,
      eleLeft: 0,
      deadline: "",
    }
  },
  methods: {
    onClick(e) {
      if (this.isShow) {
        this.isShow = false
        return
      }
      const { left } = e.target.getBoundingClientRect()
      this.eleLeft = Math.max(left - 100 + 16, 0)
      this.isShow = true
    },
    hide() {
      this.isShow = false
    },
    clickToday() {
      this.deadline = "今天"
    },
    clickTomorrow() {
      this.deadline = "明天"
    },
    deleteDeadline() {
      this.deadline = ""
      this.hide()
    },
    getWeek(date) {
      const week = date.getDay()
      const arr = ['日', '一', '二', '三', '四', '五', '六']
      return "周" + arr[week]
    }
  },
  mounted() { },
  computed: {
    calloutGroup() {
      if (this.deadline) {
        return "callout-group"
      }
    },

    todayWeek() {
      const date = new Date()
      return this.getWeek(date)
    },
    tomorrowWeek() {
      const date = new Date()
      date.setTime(date.getTime() + 24 * 60 * 60 * 1000);
      return this.getWeek(date)
    },
    nextWeek() {
      return "x"
    }

  },
};
</script>

<style lang="scss" scoped>
.callout {

  .callout-group {
    background: #fff;
    padding: 0 5px;
    margin: 0 5px;
    border-radius: 2px;
  }

  .callout-button:hover {
    background: #ccc;
  }


  display: inline-block;

  .deadline {
    border-radius: 2px;
    position: absolute;
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