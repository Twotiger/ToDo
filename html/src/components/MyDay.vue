<script setup>
  import moment from "moment";
  import SvgIcon from "@/components/SvgIcon.vue";

  import Deadline from "@/components/myday/Deadline.vue";
  import Notice from "@/components/myday/Notice.vue";
  import Repeat from "@/components/myday/Repeat.vue";
  import Suggest from "@/components/myday/Suggest.vue";
  import Details from "@/components/myday/Details.vue";
  import TaskInfo from "@/components/myday/TaskInfo.vue"

  import taskApi from "@/api/task";
  import ws from "@/utils/websocket"

  import {
    notification,
    requestPermission
  } from "@/utils/notification"
  import {
    getDeadlineStr,
    getNoticeStr
  } from "@/utils/date"
  import {
    ref,
    computed,
    watch,
    reactive,
    onMounted
  } from "vue";
  import {
    useRouter
  } from "vue-router";

  const rightComponent = ref(0); // 右边显示的元素
  const showComplete = ref(false);
  const taskName = ref("");

  const deadline = reactive({
    str: "",
    value: ""
  });

  const notice = reactive({
    str: "",
    value: {}
  });

  const repeat = reactive({
    interval: 1,
    intervalType: '',
    type: '',
    weekdays: [],
  });

  const router = useRouter();
  const todoList = ref([]); // 未完成任务
  const todoListCompleted = ref([]);
  const todoID = ref(0)

  const props = defineProps({
    showMenu: Boolean,
  });

  const _title = ref("");

  const showRightComponent = (v) => {
    if (v === 1 && rightComponent.value === 1) {
      rightComponent.value = 0;
    } else {
      rightComponent.value = v;
    }
  };

  const emit = defineEmits(["update:showMenu", "updateCount"]);

  const title = computed(() => {
    return router.currentRoute.value.meta["title"] || _title.value
  });

  const dateInfo = computed(() => {
    const today = new Date();
    const date = new Array("日", "一", "二", "三", "四", "五", "六");
    return `${today.getMonth() + 1}月 ${today.getDate()}日 星期${
    date[today.getDay()]
  }`;
  });

  const canAdd = computed(() => {
    if (/^\s*$/.test(taskName.value)) {
      return false;
    }
    return true;
  });

  const isSameDay = (dateA, dateB) => {
    retturntoday.getFullYear() == newDate.year() &&
      today.getMonth() == newDate.month() &&
      today.getDate() == newDate.date();
  };


  const toggleMenu = () => {
    emit("update:showMenu", true);
  };

  const toggleComplete = () => {
    showComplete.value = !showComplete.value;
  };

  const getRepeat = (str) => {
    const dict = {
      Daily: "每天",
      WeekDays: "工作日",
      Weekly: "每周",
      Monthly: "每月",
      Yearly: "每年",
    };
    return dict[str];
  };

  const getTasks = async () => {
    let postData = {};
    let routerInfo = router.currentRoute.value;
    if (routerInfo.name === "Myday") {
      postData["is_my_day"] = true;
    }
    if (routerInfo.name === "Important") {
      postData["is_important"] = true;
    }
    if (routerInfo.name === "Tasks") {
      postData["tasks"] = true;
    }
    if (routerInfo.name === "Task") {
      postData["task_list_id"] = routerInfo.params["listID"];
    }
    let data = await taskApi.filterTasks(postData);
    todoList.value = data["uncompleted"];
    todoListCompleted.value = data["completed"];
    _title.value = data["name"]
    emit("updateCount")
  };

  const addTask = async () => {

    let noticeValue = "";
    let deadlineValue = "";
    // let repeatValue = "";

    if (deadline.value) {
      deadlineValue = deadline.value
    }
    if (notice.value) {
      noticeValue = notice.value
    }

    let postData = {
      name: taskName.value,
      deadline: deadlineValue,
      notice: noticeValue,
      repeat: repeat,
    };
    let routerInfo = router.currentRoute.value;
    if (routerInfo.name === "Myday") {
      postData["is_my_day"] = true;
    }
    if (routerInfo.name === "Important") {
      postData["is_important"] = true;
    }
    if (routerInfo.name === "Task") {
      postData["task_list_id"] = routerInfo.params["listID"];
    }

    await taskApi.addTask(postData);
    taskName.value = "";
    deadline.str = ''
    deadline.value = ''

    notice.str = ''
    notice.value = ''

    reset()
    getTasks();
  };

  const reset = () => {
    repeat.interval = 0
    repeat.intervalType = ''
    repeat.type = ''
    repeat.weekdays = []
  }

  const completeTask = async (taskID) => {
    await taskApi.completeTask({
      task_id: taskID
    });
    await getTasks();
    emit("updateCount")
  };

  const showDetails = (taskID) => {
    todoID.value = taskID
    showRightComponent(2);
  };

  //添加到重要任务
  const addImportant = async (taskID) => {
    await taskApi.addImportant(taskID)
    await getTasks();
  }

  const deleteImportant = async (taskID) => {
    await taskApi.deleteImportant(taskID)
    await getTasks();
  }

  watch(router.currentRoute, (newValue, oldValue) => {
    if (router.currentRoute.value.name==='Search') {
      return
    }
    rightComponent.value = 0;
    getTasks();
  });

  const atMyDay = computed(() => { // 页面是否为我的一天
    return router.currentRoute.value.name === 'Myday'
  })

  // 如果更新repeat的时候deadline没有数据，需要添加数据
  const updateRepeat = () => {
    if (repeat.intervalType && deadline.value.value === "") {
      let today = new Date();
      today = new Date(
        today.getFullYear(),
        today.getMonth(),
        today.getDate(),
        18
      );
      deadline.value = {
        str: "今天",
        value: today
      };
    }
  }

  onMounted(() => {
    getTasks()
    requestPermission()
    ws.connect()
  })
</script>

<template>
  <div class="myday">
    <div class="pd10">
      <div class="sticky">
        <div class="task-tool-bar">
          <div class="title">
            <svg-icon name="menu" v-if="!showMenu" @click="toggleMenu" />
            <span>{{ title }}</span>
            <svg-icon name="suggest" v-if="atMyDay" @click.stop="showRightComponent(1)" />
          </div>
          <div class="date">{{ dateInfo }}</div>
        </div>
        <div class="add-task">
          <div class="add-base add-main">
            <svg-icon name="radio" />
            <input v-model.trim="taskName" class="add-input" type="text" placeholder="添加任务" @keyup.enter="addTask" />
          </div>
          <div class="add-base add-extend">
            <div class="extend-group">
              <Deadline :datetime="deadline"></Deadline>
              <Notice :datetime="notice"></Notice>
              <Repeat :repeat="repeat" @updateRepeat="updateRepeat"></Repeat>
            </div>
            <span :class="canAdd ? 'add-text' : 'cant-add-text'" @click="addTask">添加</span>
          </div>
        </div>
      </div>

      <div class="todo-list">
        <template v-for="todo in todoList">
          <div class="todo" @click="showDetails(todo.id)">
            <svg-icon name="radio" @click.stop="completeTask(todo.id)" />

            <div class="contant">
              <div class="title">{{ todo.name }}</div>
              <task-info :task="todo" />
            </div>

            <div class="important_icon">
              <svg-icon name="star_select" @click.stop="deleteImportant(todo.id)" v-if="todo.is_important"></svg-icon>
              <svg-icon name="star" @click.stop="addImportant(todo.id)" v-else></svg-icon>
            </div>
          </div>
        </template>
      </div>

      <div class="todo-list">
        <div class="todo complete" @click="toggleComplete">
          <div class="contant">
            <div class="title">
              <svg-icon name="arrow_right" :class="showComplete ? 'icon-down' : 'icon-right'" />
              <span>已完成 {{ todoListCompleted.length }}</span>
            </div>
          </div>
        </div>
        <template v-if="showComplete" v-for="todo in todoListCompleted">
          <div class="todo through">
            <div class="select">
              <svg-icon name="radio_select" />
            </div>

            <div class="title">{{ todo.name }}</div>
          </div>
        </template>
      </div>
    </div>

  </div>
  <Suggest v-if="rightComponent === 1" @getTasks="getTasks" v-model:rightComponent="rightComponent"/>
  <Details v-if="rightComponent === 2" :taskID="todoID" @getTasks="getTasks" v-model:rightComponent="rightComponent" />
</template>


<style lang="scss">
  .myday {
    flex: 1;
    overflow-y: auto;
    // padding: 10px;

    .pd10 {
      padding: 0 10px 10px 10px;

      .sticky {
        position: sticky;
        top: 0;
        background-color: #fff;
        padding: 10px 0;
        z-index: 10;

        .task-tool-bar {
          padding-bottom: 10px;

          .title {
            display: flex;
            align-items: center;
            padding: 6px 8px;
            font-size: 20px;
            font-weight: 700;

            span {
              flex: 1;
            }

            .icon {
              // color: var(--font-color-tertiary);
              cursor: pointer;
              padding-right: 5px;
              width: 24px;
              height: 24px;
            }
          }

          .date {
            padding: 0 8px;
            color: var(--font-color-tertiary);
            font-size: 12px;
          }
        }


        .add-task {
          background: #f3f2f1;
          border-radius: 5px;
          padding: 5px 8px;
          display: flex;
          flex-direction: column;

          .add-main {
            display: flex;
            height: 40px;
            padding: 8px 0;
            align-items: center;

            .add-input {
              border-radius: 2px;
              display: inline-block;
              border: none;
              width: 100%;
              flex: 1;
              height: 100%;
              padding: 0 8px;
              border-bottom: 1px solid blue;
            }

            .add-input:focus {
              outline: none;
              border-bottom: 1px solid blue;
            }
          }

          .add-extend {
            display: flex;
            align-items: center;
            margin-left: 32px;

            .extend-group {
              flex-grow: 1;

              .callout {
                width: inherit;
              }
            }

            .icon {
              padding: 4px;
              width: 24px;
              height: 24px;
            }

            .cant-add-text {
              cursor: pointer;
              font-size: 12px;
              color: #c2c2c2;
              font-weight: 700;
            }

            .add-text {
              cursor: pointer;
              font-size: 12px;
              font-weight: 700;
            }
          }

          .icon {
            padding: 4px;
            width: 30px;
            height: 30px;
          }
        }
      }

      .todo-list {
        .todo {
          border-bottom: solid 1px #ddd;
          cursor: pointer;
          min-height: 52px;
          max-height: 52px;

          display: flex;
          flex-direction: row;
          align-items: center;
          padding: 0 8px;

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

        .todo:hover {
          background: var(--bg-hover);
        }

        .complete {
          user-select: none;
        }

        .todo.complete:hover {
          background: none;
        }

        .todo.through {
          text-decoration: line-through;
          color: var(--font-color-tertiary);
        }
      }

    }


  }
</style>