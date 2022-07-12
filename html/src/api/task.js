import request from "@/utils/request";

export default {
  filterTasks(data) {
    return request.get("/api/task/tasks", data);
  },

  addTask(data) {
    return request.post("/api/task/task", data);
  },

  deleteTask(data) {
    return request.delete("/api/task/task", data);
  },

  updateTask(data) {
    return request.put("/api/task/task", data);
  },

  completeTask(data) {
    data["op"] = "complete";
    return request.patch("/api/task/task", data);
  },

  uncompleteTask(data) {
    data["op"] = "uncomplete";
    return request.patch("/api/task/task", data);
  },

  getTask(taskID) {
    return request.get("/api/task/task", { task_id: taskID });
  },

  addMyDay(taskID) {
    const data = {
      task_id: taskID,
      op: "add_my_day",
    };
    return request.patch("/api/task/task", data);
  },

  deleteMyDay(taskID) {
    const data = {
      task_id: taskID,
      op: "delete_my_day",
    };
    return request.patch("/api/task/task", data);
  },

  addImportant(taskID) {
    const data = {
      task_id: taskID,
      op: "add_important",
    };
    return request.patch("/api/task/task", data);
  },

  deleteImportant(taskID) {
    const data = {
      task_id: taskID,
      op: "delete_important",
    };
    return request.patch("/api/task/task", data);
  },

  updateRemark(taskID, remark) {
    const data = {
      task_id: taskID,
      op: "update_remark",
      remark: remark,
    };
    return request.patch("/api/task/task", data);
  },
};
