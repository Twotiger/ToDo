<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
</script>

<template>
  <div class="app-todo">
    <router-view></router-view>
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

.app-todo {
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

    .head-text {
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
      line-height: 32px;
      border: 1px solid #ddd;
      border-radius: 2px;
      background: #c3ddf7;
      margin-top: 8px;
      margin-bottom: 8px;
      width: 400px;
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
  }

  .content {
    display: flex;
    height: 100%;
    flex: 1;

    .sidebar {
      /* display: flex; */
      background: #f3f2f1;

      flex-direction: column;
      width: 290px;
      top: 48px;
      bottom: 0px;
      left: 0px;

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

        /* position: absolute; */
        /* flex: 1; */
        .tollbar {
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
    }

    .main {
      background: #fff;
      // padding: 10px;
      flex: 1;
      display: flex;
    }
  }
}

.background-line {
  background: linear-gradient(180deg,
      var(--bg-primary),
      var(--bg-primary) 52px,
      var(--bg-separator) 52px,
      var(--bg-separator) 52px);
}

/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */

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
