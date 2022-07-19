<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import SvgIcon from "@/components/SvgIcon.vue";
import taskApi from "@/api/account";

const account = ref({ username: "", email: "" });

const getAccount = async () => {
  let data = await taskApi.getAccount();
  account.value.username = data.username;
  account.value.email = data.email;
};

onMounted(() => {
  getAccount();
});

const router = useRouter();
const emit = defineEmits(["update:showAccount"]);
const props = defineProps({
  showAccount: Boolean,
});
const hide = () => {
  emit("update:showAccount", false);
};

const logout = () => {
  router.push({
    name: "Login",
  });
};
</script>

<template>
  <div class="menu" v-click-outside="hide" v-if="showAccount">
    <div class="account">
      <div class="account--logout" @click="logout">注销</div>
      <div class="account--avatar">
        <svg-icon color="#ddd" name="account" />
      </div>
      <div class="account--info">
        <div class="username">{{ account.username }}</div>
        <div class="email">{{ account.email }}</div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.menu {
  position: absolute;

  right: 0;
  top: 48px;
  z-index: 200;
}
.account {
  display: grid;

  width: 320px;
  height: 180px;
  background: #fff;
  border: 1px solid #ddd;

  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
  grid-template-columns: 134px 1fr 46px;
  grid-template-rows: 48px auto;
  justify-items: center;
  align-items: center;

  .account--logout {
    cursor: pointer;
    box-sizing: border-box;
    font-size: 13px;
    color: #333333;
    grid-row: 1/2;
    grid-column: 3/4;
  }

  .account--avatar {
    .icon {
      width: 88px;
      height: 88px;
    }
    grid-row: 2/3;
    grid-column: 1/2;
  }

  .account--info {
    grid-row: 2/3;
    grid-column: 2/3;
    justify-self: flex-start;
    .username {
      line-height: 25px;
      font-size: 18px;
      font-weight: 700;
    }

    .email {
      line-height: 18px;
      font-size: 13px;
    }
  }
}
</style>