<script setup>
import {
  ref,
  reactive,
  onMounted,
  watch,
  computed
} from "vue";
import moment from "moment";
import SvgIcon from "@/components/SvgIcon.vue";
import Deadline from "@/components/myday/Deadline.vue";
import Notice from "@/components/myday/Notice.vue";
import Repeat from "@/components/myday/Repeat.vue";
import {
  getDeadlineStr,
  getNoticeStr
} from "@/utils/date"
import taskApi from "@/api/task";
import {
  myday
} from "./myday.js"

const deadline = reactive({ str: '', value: '' });
const notice = reactive({ str: '', value: '' })
const repeat = reactive({
  interval: 1,
  intervalType: '',
  type: '',
  weekdays: [],
})

const props = defineProps({
  taskID: {
    type: Number,
    default: 0,
  },
  rightComponent: {
    type: Number,
    default: 2,
  },
});

const emit = defineEmits(["getTasks", "update:rightComponent"]);

const task = reactive({
  id: 0,
  name: "",
  is_my_day: false,
  is_important: false,
  deadline: "",
  repeat: "",
  notice: "",
  remark: "",
  status: '',
  created_at: "",
});

const listAssign = (a, b) =>
  Object.keys(a).forEach((key) => {
    a[key] = b[key] || a[key];
  });

const getTask = async () => {
  // TODO 更新tasks
  let data = await taskApi.getTask(props.taskID);
  task.id = data["data"].id;
  task.name = data['data'].name
  task.is_my_day = data['data'].is_my_day
  task.is_important = data['data'].is_important
  task.deadline = data['data'].deadline
  task.repeat = data['data'].repeat
  task.notice = data['data'].notice
  task.remark = data['data'].remark
  task.status = data["data"].status
  task.created_at = data['data'].created_at
  deadline.value = data['data'].deadline
  deadline.str = getDeadlineStr(data['data'].deadline)

  notice.value = data['data'].notice
  notice.str = getNoticeStr(data['data'].notice)

  let repeatData = data['data'].repeat
  repeat.interval = repeatData.interval
  repeat.intervalType = repeatData.intervalType
  repeat.type = repeatData.type
  repeat.weekdays = repeatData.weekdays

  // repeat.str = getRepeat(data['data'].repeat)

};

const addToMyDay = async () => {
  if (task.is_my_day) {
    return;
  }
  await taskApi.addMyDay(props.taskID);
  await getTask();
  emit("getTasks");
};

const delteMyDay = async () => {
  await taskApi.deleteMyDay(props.taskID);
  await getTask();
  emit("getTasks");
};

//添加到重要任务
const addImportant = async (taskID) => {
  await taskApi.addImportant(taskID);
  await getTask();
  emit("getTasks");
};

const deleteImportant = async (taskID) => {
  await taskApi.deleteImportant(taskID);
  await getTask();
  emit("getTasks");
};

watch(props, (newValue, oldValue) => {
  getTask();
});

onMounted(getTask);

// 更新remark
let timer = 0;
const updateRemark = async () => {
  clearTimeout(timer);
  timer = setTimeout(() => {
    taskApi.updateRemark(props.taskID, task.remark);
  }, 500);
};

const updateDeadline = async () => {
  await taskApi.updateTask({
    task_id: props.taskID,
    deadline: deadline,
  });
}

const updateRepeat = async () => {
  let data = repeat
  if (repeat.intervalType === '') {
    data = {}
  }
  await taskApi.updateTask({
    task_id: props.taskID,
    repeat: data,
  });
}

const updateNotice = async () => {
  await taskApi.updateTask({
    task_id: props.taskID,
    notice: notice,
  });
}

const rows = computed(() => {
  let arr = task.remark.split("\n");
  return arr.length + 3;
});


// 隐藏
const hide = () => {
  emit("update:rightComponent", 0);
};

// 删除任务
const deleteTask = async () => {
  await taskApi.deleteTask({
    'task_id': props.taskID
  });
  emit("getTasks");
  hide()
};

// 完成任务
const completeTask = async () => {

  await taskApi.completeTask({
    task_id: props.taskID
  });
  await getTask();
  emit("getTasks");
};

const uncompleteTask = async () => {
  await taskApi.uncompleteTask({
    task_id: props.taskID
  });
  await getTask();
  emit("getTasks");
};

const createdAt = computed(() => {
  return moment(task.created_at).locale("zh-cn").format("YYYY年MM月DD日");
});


const {
  humanizeRepeat
} = myday()
const getRepeat = (value) => {
  return humanizeRepeat(value)
};


</script>


<template>
  <div class="details">
    <div class="details__content">
      <div class="panel-header">
        <div class="panel">
          <div class="panel-innerClick">
            <span class="left">
              <svg-icon v-if="task.status" @click="uncompleteTask" name="radio_select" />
              <svg-icon v-else name="radio" @click="completeTask" />
            </span>
            <span class="right">{{ task.name }}</span>
            <svg-icon name="star_select" @click.stop="deleteImportant(task.id)" v-if="task.is_important"></svg-icon>
            <svg-icon name="star" @click.stop="addImportant(task.id)" v-else></svg-icon>
          </div>
        </div>
      </div>

      <div class="panel-content">
        <div class="panel" @click="addToMyDay">
          <div class="panel-innerClick">
            <span class="left is-my-day">
              <svg-icon name="sun" :color="task.is_my_day ? '#2564cf' : ''" />
            </span>
            <span class="right is-my-day" v-if="task.is_my_day">已添加到"我的一天"</span>
            <span class="right" v-else>添加到"我的一天"</span>
            <span v-if="task.is_my_day" @click="delteMyDay">
              <svg-icon name="del" color="#ddd" />
            </span>
          </div>
        </div>
      </div>
      <div class="section">
        <div class="section-item">
          <div class="panel">

            <Deadline :datetime="deadline" :showDetail="false" @updateDeadline="updateDeadline">
              <div class="section__slot">
                <svg-icon :color="deadline.value ? '#2564cf' : ''" name="date" class="left" />
                <span class="right" :class="deadline.value ? 'has-value' : ''">{{
                    getDeadlineStr(deadline.value) || "添加截止日期"
                }}</span>
              </div>
            </Deadline>

          </div>
          <div class="panel">

            <Notice :datetime="notice" :showDetail="false" @updateNotice="updateNotice">
              <div class="section__slot">
                <svg-icon :color="notice.value ? '#2564cf' : ''" name="small_bell" class="left" />
                <span class="right" :class="notice.value ? 'has-value' : ''">{{
                    getNoticeStr(notice.value) || "提醒我"
                }}</span>
              </div>
            </Notice>

          </div>

          <div class="panel">
            <Repeat :repeat="repeat" :showDetail="false" @updateRepeat="updateRepeat">
              <div class="section__slot">
                <svg-icon :color="repeat.intervalType ? '#2564cf' : ''" name="repeat" class="left" />
                <span class="right" :class="repeat.intervalType ? 'has-value' : ''">{{
                    getRepeat(repeat) || "重复"
                }}</span>
              </div>
            </Repeat>
          </div>
        </div>
      </div>

      <div class="section">
        <!-- <div class="section-item">1</div> -->
        <textarea class="textarea" placeholder="添加备注" :rows="rows" v-model="task.remark"
          @input="updateRemark"></textarea>
      </div>
    </div>
    <div class="footer">
      <div class="footer__icon" title="收起" @click="hide">
        <svg-icon name="pack_up" />
      </div>

      创建于:{{ createdAt }}
      <div class="footer__icon" title="删除任务" @click="deleteTask">
        <svg-icon name="delete" />
      </div>
    </div>
  </div>

</template>

<style lang="scss" scoped>
.details {
  width: 360px;
  height: 100%;
  background: #f3f2f1;
  max-width: 360px;
  display: flex;
  flex-direction: column;
  z-index: 100;

  @media (max-width: 1000px) {
    position: fixed;
    right: 0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
  }

  .details__content {
    // flex: 1;

    .panel-header {
      margin: 12px 12px;

      .panel {
        cursor: pointer;
        padding: 10px;
        border-radius: 2px;
        background-clip: "content-box";
        background: #fff;

        .panel-innerClick {
          display: flex;
          align-items: center;
          padding: 10px;

          .left {
            margin-right: 10px;

            .icon {
              width: 25px;
              height: 25px;
            }
          }

          .right {
            flex: 1;
            font-size: 16px;
            color: #323130;
            font-weight: 600;
          }

          .icon {
            width: 15px;
            height: 15px;
          }
        }
      }
    }

    .panel-content {
      margin: 12px 12px;

      .panel {
        padding: 10px;
        cursor: pointer;
        border-radius: 2px;
        background-clip: "content-box";
        background: #fff;

        .panel-innerClick {
          padding: 10px;
          display: flex;
          align-items: center;

          .left {
            margin-right: 10px;

            .icon {
              width: 20px;
              height: 20px;
            }
          }

          .right {
            font-size: 14px;
            color: var(--font-color-tertiary);
            flex: 1;
          }

          .icon {
            width: 15px;
            height: 15px;
          }

          .is-my-day {
            color: var(--font-color-brand);
          }
        }
      }

      .panel:hover {
        background: var(--bg-hover-tertiary);
      }
    }

    .section {
      margin: 12px 12px;

      .section-item {
        // padding: 10px;
        border-radius: 2px;
        background: #fff;

        .panel {
          cursor: pointer;


          .callout {
            padding: 20px;

            .callout__group {
              .section__slot {
                display: flex;
                align-items: center;
                width: 100%;
                height: 100%;

                .icon {
                  width: 20px;
                  height: 20px;
                }
              }

            }

            .left {
              margin-right: 10px;

              .callout {}

              .icon {
                width: 20px;
                height: 20px;
              }
            }

            .right {
              font-size: 14px;
              color: var(--font-color-tertiary);
            }

            .right.has-value {
              color: var(--font-color-brand);
            }
          }
        }

        .panel:hover {
          background: var(--bg-hover-tertiary);
        }
      }

      .textarea {
        box-sizing: border-box;
        padding: 10px;
        width: 100%;
        border: none;
        outline: none;
        resize: none;
      }
    }
  }

  .footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 38px;
    padding: 0 10px;
    color: #797979;
    font-size: 12px;

    .footer__icon {
      cursor: pointer;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;

      &:hover {
        background: #fff;
      }
    }

    .icon {
      width: 20px;
      height: 20px;
    }
  }
}
</style>