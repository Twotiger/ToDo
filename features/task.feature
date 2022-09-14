Feature: Task

  @task @add_task
  Scenario: 用户可以添加Task
    Given 'Jim'登录网站
    When 添加任务
      """
      {
          "name": "今天晚上有约会",
          "deadline": "今天",
          "is_my_day": true
      }
      """
    Then 得到成功提示
    When 添加任务
      """
      {
          "name": "今天下班交报告",
          "notice": "今天",
          "is_my_day": true
      }
      """
    Then 得到成功提示
    When 添加任务
      """
      {
          "name": "下班交报告",
          "repeat": {
            "interval": 1,
            "intervalType": "Daily",
            "type": "",
            "weekdays": []
          },
          "is_important": true
      }
      """
    Then 得到成功提示
    When 添加任务
      """
      {
          "name": "晚上有约会",
          "deadline": "今天",
          "notice": "今天", 
          "repeat": {
            "interval": 1,
            "intervalType": "Daily",
            "type": "",
            "weekdays": []
          },
          "is_important": true
      }
      """
    Then 得到成功提示

  @task @search_task1
  Scenario: 用户可以查询Task
    Given 'Jim'登录网站
    When 添加任务
      """
      {
          "name": "今天晚上有约会",
          "deadline": "今天",
          "is_my_day": true
      }
      """
    Then 得到成功提示
    Then 查询每日任务
      """
      {
          "uncompleted": [
          {
              "name": "今天晚上有约会",
              "deadline": "今天"
          }
          ],
          "completed": []
      }
      
      """
    When 添加任务
      """
      {
          "name": "明天晚上有约会",
          "deadline": "明天",
          "is_important": true
      }
      """
    Then 得到成功提示
    Then 查询每日任务
      """
      {
          "uncompleted":[
          {
              "name": "今天晚上有约会",
              "deadline": "今天"
          }
          ],
          "completed": []
      }
      """

  @task @task_complete1
  Scenario: 用户可以完成Task
    Given 'Jim'登录网站
    When 添加任务
      """
      {
          "name": "今天晚上有约会",
          "deadline": "今天",
          "is_my_day": true
      }
      """
    Then 得到成功提示
    When 完成任务"今天晚上有约会"
    Then 得到成功提示
    When 添加任务
      """
      {
          "name": "下班交报告",
          "repeat": {
            "interval": 1,
            "intervalType": "Daily",
            "type": "",
            "weekdays": []
          },
          "is_important": true,
          "is_my_day": true
      }
      """
    Then 得到成功提示
    Then 查询每日任务
      """
      {
          "uncompleted": [{
              "name": "下班交报告",
              "repeat": {
                    "interval": 1,
                    "intervalType": "Daily",
                    "type": "",
                    "weekdays": []
                },
              "is_important": true,
              "is_my_day": true
          }],
          "completed": [{
              "name": "今天晚上有约会",
              "deadline": "今天",
              "is_my_day": true
          }]
      }
      """

  @task @task_complete2
  Scenario: 用户可以完成重复Task
    Given 'Jim'登录网站
    When 添加任务
      """
      {
          "name": "下班交报告",
          "deadline": "今天",
          "repeat": {
            "interval": 1,
            "intervalType": "Daily",
            "type": "",
            "weekdays": []
          },
          "is_important": true,
          "is_my_day": true
      }
      """
    Then 得到成功提示
    When 完成任务"下班交报告"
    Then 得到成功提示
    Then 查询默认任务列表
      """
      {
          "uncompleted": [{
              "name": "下班交报告",
              "repeat": {
                    "interval": 1,
                    "intervalType": "Daily",
                    "type": "",
                    "weekdays": []
                },
              "is_important": true,
              "is_my_day": false
          }],
          "completed": [{
              "name": "下班交报告",
              "deadline": "今天",
              "is_my_day": true,
              "is_important": true,
              "repeat": {
                    "interval": 1,
                    "intervalType": "Daily",
                    "type": "",
                    "weekdays": []
                }
              
          }]
      }
      """

  @task @task_add_my_day
  Scenario: 用户可以完成Task
    Given 'Jim'登录网站
    When 添加任务
      """
      {
          "name": "今天晚上有约会",
          "is_important": true,
          "deadline": "今天"
      }
      """
    Then 得到成功提示
    Then 查询每日任务
      """
      {
          "uncompleted":[],
          "completed": []
      }
      """
    When 将任务"今天晚上有约会"添加到我的一天
    Then 得到成功提示
    Then 查询每日任务
      """
      {
          "uncompleted":[
      {
          "name": "今天晚上有约会",
          "is_important": true,
          "deadline": "今天"
      }
          ],
          "completed": []
      }
      """
    When 将任务"今天晚上有约会"从我的一天删除
    Then 得到成功提示
    Then 查询每日任务
      """
      {
          "uncompleted":[],
          "completed": []
      }
      """

  @task @task_add_important
  Scenario: 用户可以修改任务为重要,也可以取消重要
    Given 'Jim'登录网站
    When 添加任务
      """
      {
          "name": "今天晚上有约会",
          "is_important": true,
          "is_my_day": true,
          "deadline": "今天"
      }
      """
    Then 得到成功提示
    When 添加任务
      """
      {
          "name": "下班交报告",
          "repeat": {
                "interval": 1,
                "intervalType": "Daily",
                "type": "",
                "weekdays": []
            },
          "is_important": false,
          "is_my_day": true
      }
      """
    Then 得到成功提示
    Then 查询每日任务
      """
      {
          "uncompleted": [{
              "name": "下班交报告",
              "repeat": {
                "interval": 1,
                "intervalType": "Daily",
                "type": "",
                "weekdays": []
                },
              "is_important": false,
              "is_my_day": true
          },{
              "name": "今天晚上有约会",
              "deadline": "今天",
              "is_important": true,
              "is_my_day": true
          }],
          "completed": []
      }
      """
    When 将任务"下班交报告"添加到重要
    Then 查询每日任务
      """
      {
          "uncompleted": [{
              "name": "下班交报告",
              "repeat": {
                    "interval": 1,
                    "intervalType": "Daily",
                    "type": "",
                    "weekdays": []
                },
              "is_important": true,
              "is_my_day": true
          },{
              "name": "今天晚上有约会",
              "deadline": "今天",
              "is_important": true,
              "is_my_day": true
          }],
          "completed": []
      }
      """
    When 将任务"今天晚上有约会"从重要删除
    Then 查询每日任务
      """
      {
          "uncompleted": [{
              "name": "下班交报告",
              "repeat": {
                    "interval": 1,
                    "intervalType": "Daily",
                    "type": "",
                    "weekdays": []
                },
              "is_important": true,
              "is_my_day": true
          },{
              "name": "今天晚上有约会",
              "deadline": "今天",
              "is_important": false,
              "is_my_day": true
          }],
          "completed": []
      }
      """

  @task @task_update_remark
  Scenario: 用户可以更新remark
    Given 'Jim'登录网站
    When 添加任务
      """
      {
          "name": "今天晚上有约会",
          "is_important": true,
          "is_my_day": true,
          "deadline": "今天"
      }
      """
    Then 得到成功提示
    When 修改"今天晚上有约会"的备注
      """
      {"remark": "记得带礼物"}
      """
    Then 查询任务"今天晚上有约会"
      """
      {
      
      "name": "今天晚上有约会",
      "is_important": true,
      "is_my_day": true,
      "remark": "记得带礼物"
      
      }
      """

  @task @task_suggest
  Scenario: 用户可以查询建议
    Given 'Jim'登录网站
    When 添加任务
      """
      {
          "name": "今天晚上有约会",
          "is_important": true,
          "is_my_day": true,
          "deadline": "今天"
      }
      """
    Then 得到成功提示
    When 添加任务
      """
      {
          "name": "明天晚上有约会",
          "is_important": true,
          "deadline": "今天"
      }
      """
    Then 得到成功提示
    When 添加任务列表
      """
      {
          "name": "打游戏"
      }
      """
    When 添加任务列表
      """
      {
          "name": "看电影"
      }
      """
    When 添加任务
      """
      {
          "name": "明天晚上看电影",
          "task_list_name": "看电影"
      }
      """
    Then 查询每日建议
      """
      [
        {
          "name": "明天晚上看电影"
      
        },
        {
          "name": "明天晚上有约会"
        }
      ]
      """

  @task @delete_task1
  Scenario: 用户可以删除Task
    Given 'Jim'登录网站
    When 添加任务
      """
      {
          "name": "今天晚上有约会",
          "deadline": "今天",
          "is_my_day": true
      }
      """
    Then 得到成功提示
    Then 查询每日任务
      """
      {
          "uncompleted": [
          {
              "name": "今天晚上有约会",
              "deadline": "今天"
          }
          ],
          "completed": []
      }
      
      """
    When 添加任务
      """
      {
          "name": "明天晚上有约会",
          "deadline": "明天",
          "is_important": true
      }
      """
    Then 得到成功提示
    Then 查询每日任务
      """
      {
          "uncompleted":[
          {
              "name": "今天晚上有约会",
              "deadline": "今天"
          }
          ],
          "completed": []
      }
      """
    Then 查询任务列表详情
      """
      {
        "data": [],
        "task_count": {
          "important": 1,
          "my_day": 1,
          "task": 2
        }
      }
      """
    When 删除任务"今天晚上有约会"
    Then 查询任务列表详情
      """
      {
        "data": [],
        "task_count": {
          "important": 1,
          "my_day": 0,
          "task": 1
        }
      }
      """
    When 删除任务"明天晚上有约会"
    Then 查询任务列表详情
      """
      {
        "data": [],
        "task_count": {
          "important": 0,
          "my_day": 0,
          "task": 0
        }
      }
      """
