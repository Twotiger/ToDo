import request from "@/utils/request"


export default {
    addTaskList(name){
        return request.post("/api/task_list/task_list", {"name":name, "task_type": "list"})
    },

    addTaskGroup(name){
        return request.post("/api/task_list/task_list", {"name":name, "task_type": "group"})
    },

    getTaskList(){
        return request.get("/api/task_list/task_lists")

    },

    changeIndex(fromID, toID, position) {
        return request.patch("/api/task_list/task_lists" , {"from_id":fromID, "to_id":toID, "position":position})
    }
}