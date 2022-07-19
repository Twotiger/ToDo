<script setup>
import SvgIcon from "@/components/SvgIcon.vue";

import { reactive, ref, onMounted, provide, computed } from "vue";
import { useRouter } from "vue-router";
import Account from "./Account.vue";

import TaskList from "@/components/nav/TaskList.vue";
import TaskGroup from "@/components/nav/TaskGroup.vue";
import taskListApi from "@/api/task_list";

const taskGroups = reactive([]);
const showMenu = ref(true);
const taskCount = reactive({
  my_day: 0,
  important: 0,
  task: 0,
});

const willAddTaskGroup = ref(false);
const willAddTaskGroupName = ref("");
const willAddTaskName = ref("");
const router = useRouter();

const blur = () => {
  // 失去焦点时,删除输入框
  setTimeout(() => {
    willAddTaskGroup.value = false;
    willAddTaskGroupName.value = "";
  }, 200);
};

const addGroupInput = () => {
  if (willAddTaskGroup.value) {
    addTaskGroup(willAddTaskGroupName.value);
  }
  willAddTaskGroup.value = !willAddTaskGroup.value;
};

const addTaskGroup = async (name) => {
  if (name) {
    await taskListApi.addTaskGroup(name);
    await getTaskGroup();
  }
};

const addTaskList = async () => {
  if (willAddTaskName.value) {
    await taskListApi.addTaskList(willAddTaskName.value);
    willAddTaskName.value = "";
    await getTaskGroup();
  }
};

const getTaskGroup = async () => {
  const data = await taskListApi.getTaskList();
  taskGroups.length = 0;
  data["data"].forEach((item) => {
    taskGroups.push(item);
  });
  taskCount.my_day = data["task_count"]["my_day"];
  taskCount.important = data["task_count"]["important"];
  taskCount.task = data["task_count"]["task"];
};

provide("getTaskGroup", getTaskGroup);

const toggleMenu = () => {
  showMenu.value = !showMenu.value;
};

// 拖动开始
const dropID = ref(0);

const dragstart = (e, id) => {
  // console.log("dragstart-id=", id);
  dropID.value = id;
};

const enterGroup = reactive({
  id: 0,
  op: "",
});

const dragenter = (e, id) => {
  enterGroup.id = id;

  if (isUp(e)) {
    enterGroup.op = "up";
  } else {
    enterGroup.op = "down";
  }
};

const dragend = (e) => {
  // console.log("dragend,", e.target);
  // enterGroup.id = 0;
};

const isUp = (e) => {
  let domRect = e.currentTarget.getBoundingClientRect();
  const clientY = e.clientY;
  const { top, height } = domRect;
  if (clientY - top > height / 2) {
    return false;
  } else {
    return true;
  }
};

const dragleave = (e, id) => {
  // console.log("dragleave", id, e.target);
};

const findIndex = (id) => {
  for (let i = 0; i < taskGroups.length; i++) {
    let data = taskGroups[i];
    if (data.task_type === "group") {
      if (data.id === id) {
        return [i, -1];
      }
      for (let j = 0; j < data.children.length; j++) {
        if (data.children[j].id === id) {
          return [i, j];
        }
      }
    } else {
      if (data.id === id) {
        return [i, -1];
      }
    }
  }
};

// 如果是空组,就插入
const dropToEmpty = async (e, id) => {
  // console.log("dropToEmpty在", id, "上放下");

  let [fromI, fromJ] = findIndex(dropID.value);
  // console.log(fromI, fromJ);
  if (fromJ === -1 && taskGroups[fromI].task_type === "group") {
    return; //不可以把组放在组里面
  }

  await taskListApi.changeIndex(dropID.value, id, "in");
  await getTaskGroup();
};

const drop = async (e, id) => {
  let domRect = e.target.getBoundingClientRect();
  const clientY = e.clientY;
  const { top, height } = domRect;
  let position = "up";
  if (clientY - top > height / 2) {
    position = "down";
  } else {
    position = "up";
  }

  e.currentTarget.style.border = "none";
  await taskListApi.changeIndex(dropID.value, id, position);
  await getTaskGroup();
};

const dropClass = (id) => {
  let className = "";
  if (
    router.currentRoute.value.name === "Task" &&
    router.currentRoute.value.params["listID"] === id.toString()
  ) {
    className += " active";
  }

  if (enterGroup.id === 0) {
    return className;
  }
  if (id !== enterGroup.id) {
    return className;
  }
  if (enterGroup.op === "up") {
    return "border_top";
  }
  return "border_bottom";
};

let timer = 0;
const searchTasks = async (e) => {
  clearTimeout(timer);
  timer = setTimeout(() => {
    if (e.target.value === "") {
      return;
    }
    router.push({
      name: "Search",
      params: {
        keyword: encodeURIComponent(e.target.value),
      },
    });
  }, 500);
};

// 拖动结束

onMounted(getTaskGroup);

const openGroup = reactive([]);

const showAccount = ref(false);
</script>

<template>
  <div class="todo" id="todo">
    <div class="head">
      <div class="head-text">
        <span>To Do</span>
      </div>

      <div class="search">
        <span class="search-icon">
          <svg-icon name="search" />
        </span>
        <input class="search-input" type="text" @input="searchTasks" />
      </div>
      <!-- <svg-icon name="setting" /> -->
      <div class="icon-button" @click.stop="showAccount = !showAccount"><svg-icon name="account" color="#fff"/></div>
      <Account v-model:showAccount="showAccount"/>
    </div>

    <div class="content">
      <transition enter-active-class="animate__fadeInRight">
        <div class="sidebar" v-if="showMenu">
          <div class="sidebar-header">
            <span class="menu-icon">
              <svg-icon name="menu" @click="toggleMenu" />
            </span>
          </div>

          <div class="sidebar-content">
            <router-link
              :to="{ path: '/' }"
              class="todayToolbar tollbar"
              :class="router.currentRoute.value.name == 'Myday' ? 'active' : ''"
            >
              <svg-icon name="daytime" />
              <span class="text">我的一天</span>
              <span>{{ taskCount.my_day }}</span>
            </router-link>
            <router-link
              :to="{ path: '/important' }"
              class="todayToolbar tollbar"
              :class="
                router.currentRoute.value.name == 'Important' ? 'active' : ''
              "
            >
              <svg-icon name="star" /><span class="text">重要</span>
              <span>{{ taskCount.important }}</span>
            </router-link>

            <router-link
              :to="{ path: '/tasks' }"
              class="todayToolbar tollbar"
              :class="router.currentRoute.value.name == 'Tasks' ? 'active' : ''"
            >
              <svg-icon name="home" /><span class="text">任务</span>
              <span>{{ taskCount.task }}</span>
            </router-link>
          </div>

          <div class="task-groups">
            <template v-for="(item, index) in taskGroups" :key="item.id">
              <div
                class="task-group drag"
                :class="dropClass(item.id)"
                draggable="true"
                @dragover.prevent
                @dragend="dragend"
                @dragenter="dragenter($event, item.id)"
                @dragleave="dragleave($event, item.id)"
                @dragstart="dragstart($event, item.id)"
                @drop="drop($event, item.id)"
                v-if="item.task_type === 'list'"
              >
                <TaskList :data="item" />
              </div>

              <div
                v-else
                draggable="true"
                @dragover.prevent
                @dragend="dragend"
                @dragenter="dragenter($event, item.id)"
                @dragleave="dragleave($event, item.id)"
                @dragstart="dragstart($event, item.id)"
                @drop="drop($event, item.id)"
              >
                <TaskGroup
                  @dragstart="dragstart"
                  @drop="drop"
                  @dragenter="dragenter"
                  @dropToEmpty="dropToEmpty"
                  v-model:openGroup="openGroup"
                  @dragleave="dragleave"
                  :data="item"
                />
              </div>
            </template>
          </div>

          <!-- 新的group -->
          <div class="add-task-group" v-if="willAddTaskGroup">
            <div class="input-group">
              <svg-icon name="task_group" />
              <input
                v-model="willAddTaskGroupName"
                v-focus
                class="text"
                @blur="blur"
                @keyup.enter="addGroupInput"
              />
            </div>
          </div>

          <div class="add-task-group">
            <div class="input-group">
              <svg-icon name="plus" />
              <input
                class="text"
                v-model="willAddTaskName"
                @keyup.enter="addTaskList"
              />
            </div>
            <svg-icon
              name="add"
              class="icon pd12 add-group"
              @click="addGroupInput"
            />
          </div>
        </div>
      </transition>

      <div class="main">
        <router-view
          v-model:showMenu="showMenu"
          @updateCount="getTaskGroup"
        ></router-view>
      </div>
    </div>
  </div>
</template>



<style lang="scss">
html {
  height: 100%;
}

body {
  padding: 0;
  margin: 0;
  height: 100%;
}

#app {
  height: 100%;
  /* background: #f3f2f1; */
}

.todo {
  height: 100%;
  display: flex;
  flex-direction: column;

  .head {
    height: 48px;
    line-height: 48px;
    background: #346fef;
    display: flex;
    align-items: center;
    width: 100%;

    .icon {
      width: 25px;
      height: 25px;
    }

    .head-text {
      min-width: 3rem;
      font-size: 1rem;
      display: inline-block;
      color: #fff;
      margin: 0 10px 0 10px;
      font-family: SegoeUI-SemiBold-final, Segoe UI Semibold,
        SegoeUI-Regular-final, Segoe UI, "Segoe UI Web (West European)", Segoe,
        -apple-system, BlinkMacSystemFont, Roboto, Helvetica Neue, Tahoma,
        Helvetica, Arial, sans-serif;
    }

    .search {
      cursor: pointer;
      line-height: 2rem;
      border: 0.0625rem solid #ddd;
      border-radius: 0.125rem;
      background: #c3ddf7;
      margin-top: 0.5rem;
      margin-bottom: 0.5rem;
      width: 25rem;
      display: flex;
      margin-left: auto;
      margin-right: auto;

      .search-icon {
        height: 30px;
        width: 32px;
        display: flex;
        align-items: center;
        justify-content: center;

        .icon {
          width: 16px;
          height: 16px;
        }
      }

      .search-icon:hover {
        background: #b9d6f3;
        // opacity: 0.5;
      }

      .search-input {
        flex: 1;
        background: none;
        outline: none;
        border: none;
      }

      .search-input:focus {
        border: none;
      }
    }

    .setting {
      display: inline-block;
      line-height: 48px;
      padding: 0 16px;
      width: 24px;
      height: 24px;
      cursor: pointer;
    }

    .icon-button {
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      box-sizing: border-box;
      width: 48px;
      height: 48px;
    }
  }

  .content {
    display: flex;
    height: 100%;
    flex: 1;
    overflow: hidden;

    .sidebar {
      /* display: flex; */
      background: #f3f2f1;
      flex-direction: column;
      width: 290px;
      top: 48px;
      bottom: 0px;
      left: 0px;

      @media (max-width: 1000px) {
        position: fixed;
        left: 0;
        z-index: 20;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
      }

      .sidebar-header {
        height: 48px;
        line-height: 48px;

        .menu-icon {
          width: 48px;
          cursor: pointer;
          display: inline-block;
          height: 48px;
          padding: 0 12px;
          display: flex;
          align-items: center;

          .icon {
            width: 24px;
            height: 24px;
          }
        }
      }

      .sidebar-content {
        .tollbar {
          box-sizing: border-box;
          display: flex;
          align-items: center;
          height: 36px;
          padding: 0 12px;
          font-size: 14px;
          cursor: pointer;

          .icon {
            width: 20px;
            height: 20px;
          }

          .text {
            margin: 0 8px;
            flex: 1;
          }
        }

        .tollbar:hover {
          background: #fff;
        }

        .active {
          font-weight: 700;
          background: #fff;
        }
      }

      .task-groups {
        margin-top: 10px;

        .active {
          font-weight: 700;
          background: #fff;
        }

        .border_top {
          border-top: 2px solid #2564cf;
        }

        .border_bottom {
          border-bottom: 2px solid #2564cf;
        }
      }

      .add-task-group {
        display: flex;
        align-items: center;
        height: 36px;

        .input-group {
          display: flex;
          align-items: center;
          flex: 1;
          height: 100%;

          .text {
            box-sizing: border-box;
            height: 100%;
            border: none;
            outline: none;
            background: transparent;
          }

          .text:hover {
            background: #fff;
          }
        }

        .input-group:hover {
          background: #fff;
        }

        .icon {
          padding: 0 10px;
          width: 20px;
          height: 20px;
          cursor: pointer;
        }

        .pd12 {
          padding: 0 12px;
        }

        .add-group {
          height: 100%;
        }

        .add-group:hover {
          background: #fff;
        }
      }
    }

    .main {
      background: #fff;
      flex: 1;
      display: flex;
    }
  }
}

.background-line {
  background: linear-gradient(
    180deg,
    var(--bg-primary),
    var(--bg-primary) 52px,
    var(--bg-separator) 52px,
    var(--bg-separator) 52px
  );
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

a {
  text-decoration: none; //去掉下划线
  color: inherit;
  -webkit-user-select: none;
  -moz-user-select: none;
  user-select: none;
  -webkit-appearance: none;
  -webkit-text-size-adjust: none;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
  -webkit-touch-callout: none;
  border-bottom: none; //去掉下边框（用text-decoration: none;没有用是时候加上）；
  display: block;
  width: 100%;
  height: 40px;
}
</style>