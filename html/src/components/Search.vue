<script setup>
import Task from "@/components/myday/Task.vue"
import Details from "@/components/myday/Details.vue";
import SvgIcon from "@/components/SvgIcon.vue";
import taskApi from "@/api/task";
import {
  ref,
  computed,
  watch,
  onMounted
} from 'vue'
import {
  useRouter
} from "vue-router";

const props = defineProps({
  showMenu: Boolean,
});
const emit = defineEmits(["update:showMenu", "updateCount"]);
const toggleMenu = () => {
  emit("update:showMenu", true);
};

const router = useRouter();
const taskPack = ref([])
const taskID = ref(0)
const rightComponent = ref(0)

const searchKeyword = computed(() => {
  return decodeURIComponent(router.currentRoute.value.params.keyword)
})

const getTasks = async () => {
  let data = await taskApi.filterTasks({
    keyword: decodeURIComponent(router.currentRoute.value.params.keyword)
  })
  taskPack.value = data['data']
}

onMounted(() => {
  getTasks()
})

const showDetail = (id) => {
  taskID.value = id
  rightComponent.value = 1
}

watch(router.currentRoute, (newValue, oldValue) => {
  getTasks();
});
</script>

<template>
  <div class="search">
    <div class="search--title">
      <svg-icon name="menu" v-if="!showMenu" @click="toggleMenu" />
      <div class="title--text">正在搜索 "{{ searchKeyword }}"</div>
    </div>

    <div class="tasks">
      <div v-for="item in taskPack">
        <div class="tasks--tasklist">
          <h3>{{ item.name }}</h3>
        </div>
        <div class="tasks--list">
          <div v-for="task in item.data">
            <Task :task="task" @getTasks="getTasks" @showDetail="showDetail" />
          </div>
        </div>
      </div>
    </div>
  </div>
  <Details v-if="rightComponent != 0" :taskID="taskID" @getTasks="getTasks" v-model:rightComponent="rightComponent" />
</template>


<style lang="scss" scoped>
.search {
  // width: 100%;
  flex: 1;
  overflow-y: auto;

  .search--title {
    display: flex;

    padding: 12px 16px 0 16px;

    .icon {
      cursor: pointer;
      padding-right: 5px;
      width: 24px;
      height: 24px;
    }

    .title--text {
      color: var(--bg-brand);
      font-size: 20px;
      font-weight: 600;
      // padding: 6px 8px;
    }
  }
}

.tasks {
  .tasks--tasklist {
    color: var(--font-color-primary);
    margin: 20px 20px 10px 15px;
  }

  .tasks--list {
    margin: 0 8px;
  }
}
</style>