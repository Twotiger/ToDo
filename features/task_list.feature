Feature: 任务列表

  @task_list @task_list_1
  Scenario: 用户可以添加任务组
    Given 'Jim'登录网站
    When 添加任务组
      """
      {
          "name": "学习"
      }
      """
    Then 得到成功提示
    When 添加任务组
      """
      {
          "name": "娱乐"
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
    When 添加任务列表
      """
      {
          "name": "work"
      }
      """
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group"
          },
          {
              "name": "娱乐", "task_type": "group"
          },
          {
              "name": "打游戏", "task_type": "list"
          },
          {
              "name": "看电影", "task_type": "list"
          },
          {
              "name": "work", "task_type": "list"
          }
      ]
      """

  @task_list @task_list_2
  Scenario: 单纯的位置移动
    Given 'Jim'登录网站
    When 添加任务组
      """
      {
          "name": "学习"
      }
      """
    Then 得到成功提示
    When 添加任务组
      """
      {
          "name": "娱乐"
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
    When 添加任务列表
      """
      {
          "name": "work"
      }
      """
    When 移动任务列表"work"到"娱乐"的"上面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group"
          },
          {
              "name": "work", "task_type": "list"
          },
          {
              "name": "娱乐", "task_type": "group"
          },
          {
              "name": "打游戏", "task_type": "list"
          },
          {
              "name": "看电影", "task_type": "list"
          }
      ]
      """
    When 移动任务列表"work"到"学习"的"上面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "work", "task_type": "list"
          },
          {
              "name": "学习", "task_type": "group"
          },
          {
              "name": "娱乐", "task_type": "group"
          },
          {
              "name": "打游戏", "task_type": "list"
          },
          {
              "name": "看电影", "task_type": "list"
          }
      ]
      """
    When 移动任务列表"学习"到"看电影"的"下面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "work", "task_type": "list"
          },
          {
              "name": "娱乐", "task_type": "group"
          },
          {
              "name": "打游戏", "task_type": "list"
          },
          {
              "name": "看电影", "task_type": "list"
          },
          {
              "name": "学习", "task_type": "group"
          }
      ]
      """
    When 移动任务列表"看电影"到"打游戏"的"上面"
    Then 查询任务列表
      """
      [
          {
              "name": "work", "task_type": "list"
          },
          {
              "name": "娱乐", "task_type": "group"
          },
          {
              "name": "看电影", "task_type": "list"
          },
          {
              "name": "打游戏", "task_type": "list"
          },
      
          {
              "name": "学习", "task_type": "group"
          }
      ]
      """
    When 移动任务列表"娱乐"到"学习"的"下面"
    Then 查询任务列表
      """
      [
          {
              "name": "work", "task_type": "list"
          },
          {
              "name": "看电影", "task_type": "list"
          },
          {
              "name": "打游戏", "task_type": "list"
          },
          {
              "name": "学习", "task_type": "group"
          },
          {
              "name": "娱乐", "task_type": "group"
          }
      ]
      """

  @task_list @task_list_3
  Scenario: 移动list到group里面
    Given 'Jim'登录网站
    When 添加任务组
      """
      {
          "name": "学习"
      }
      """
    Then 得到成功提示
    When 添加任务组
      """
      {
          "name": "娱乐"
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
    When 添加任务列表
      """
      {
          "name": "work"
      }
      """
    When 移动任务列表"打游戏"到"学习"的"里面"
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group", "children": [
                  {
                      "name": "打游戏", "task_type": "list"
                  }
              ]
          },
          {
              "name": "娱乐", "task_type": "group"
          },
          {
              "name": "看电影", "task_type": "list"
          },
          {
              "name": "work", "task_type": "list"
          }
      ]
      """
    When 移动任务列表"看电影"到"娱乐"的"里面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group", "children": [
                  {
                      "name": "打游戏", "task_type": "list"
                  }
              ]
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
                  {
                      "name": "看电影", "task_type": "list"
                  }
              ]
          },
          {
              "name": "work", "task_type": "list"
          }
      ]
      """
    When 移动任务列表"work"到"看电影"的"下面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group", "children": [
                  {
                      "name": "打游戏", "task_type": "list"
                  }
              ]
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
                  {
                      "name": "看电影", "task_type": "list"
                  },
                  {
                      "name": "work", "task_type": "list"
                  }
              ]
          }
      
      ]
      """
    When 移动任务列表"work"到"打游戏"的"下面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group", "children": [
                  {
                      "name": "打游戏", "task_type": "list"
                  },
                  {
                      "name": "work", "task_type": "list"
                  }
              ]
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
                  {
                      "name": "看电影", "task_type": "list"
                  }
              ]
          }
      
      ]
      """
    When 移动任务列表"work"到"娱乐"的"上面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          { 
              "name": "学习", "task_type": "group", "children": [
                  {
                      "name": "打游戏", "task_type": "list"
                  }
              ]
          },
          {
              "name": "work", "task_type": "list"
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
                  {
                      "name": "看电影", "task_type": "list"
                  }
              ]
          }
      
      ]
      """
    When 移动任务列表"打游戏"到"娱乐"的"下面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          { 
              "name": "学习", "task_type": "group", "children": [
      
              ]
          },
          {
              "name": "work", "task_type": "list"
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
                  {
                      "name": "看电影", "task_type": "list"
                  }
              ]
          },{
              "name": "打游戏", "task_type": "list"
          }
      
      ]
      """
    When 移动任务列表"打游戏"到"看电影"的"上面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          { 
              "name": "学习", "task_type": "group", "children": [
      
              ]
          },
          {
              "name": "work", "task_type": "list"
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
                  {
                      "name": "打游戏", "task_type": "list"
                  },
                  {
                      "name": "看电影", "task_type": "list"
                  }
              ]
          }
      
      ]
      """
    When 移动任务列表"看电影"到"学习"的"上面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "看电影", "task_type": "list"
          },
          { 
              "name": "学习", "task_type": "group", "children": [
      
              ]
          },
          {
              "name": "work", "task_type": "list"
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
                  {
                      "name": "打游戏", "task_type": "list"
                  }
              ]
          }
      
      ]
      """
    When 移动任务列表"看电影"到"娱乐"的"下面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          { 
              "name": "学习", "task_type": "group", "children": [
      
              ]
          },
          {
              "name": "work", "task_type": "list"
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
                  {
                      "name": "打游戏", "task_type": "list"
                  }
              ]
          },
          {
              "name": "看电影", "task_type": "list"
          }
      
      ]
      """
    When 移动任务列表"打游戏"到"看电影"的"下面"
    Then 得到成功提示
    When 移动任务列表"work"到"看电影"的"上面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          { 
              "name": "学习", "task_type": "group", "children": [
      
              ]
          },
      
          {
              "name": "娱乐", "task_type": "group", "children": [
      
              ]
          },
          {
              "name": "work", "task_type": "list"
          },
          {
              "name": "看电影", "task_type": "list"
          },
          {
              "name": "打游戏", "task_type": "list"
          }
      
      ]
      """
    When 移动任务列表"打游戏"到"学习"的"里面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          { 
              "name": "学习", "task_type": "group", "children": [
              {
                  "name": "打游戏", "task_type": "list"
              }
      
              ]
          },
      
          {
              "name": "娱乐", "task_type": "group", "children": [
      
              ]
          },
          {
              "name": "work", "task_type": "list"
          },
          {
              "name": "看电影", "task_type": "list"
          }
      ]
      """
    When 移动任务列表"work"到"学习"的"下面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          { 
              "name": "学习", "task_type": "group", "children": [
              {
                  "name": "打游戏", "task_type": "list"
              }
              ]
          },
          {
              "name": "work", "task_type": "list"
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
      
              ]
          },
      
          {
              "name": "看电影", "task_type": "list"
          }
      ]
      """

  @task_list @task_list_4
  Scenario: 随机测试任务列表
    Given 'Jim'登录网站
    When 添加任务组
      """
      {
          "name": "学习"
      }
      """
    Then 得到成功提示
    When 添加任务组
      """
      {
          "name": "娱乐"
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
    When 添加任务列表
      """
      {
          "name": "work"
      }
      """
    When 移动任务列表"打游戏"到"娱乐"的"里面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          { 
              "name": "学习", "task_type": "group", "children": [
              ]
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
              {
                  "name": "打游戏", "task_type": "list"
              }
              ]
          },
          {
              "name": "看电影", "task_type": "list"
          },
          {
              "name": "work", "task_type": "list"
          }
      
      ]
      """

  @task_list @task_list_5
  Scenario: 外面的移动到里面
    Given 'Jim'登录网站
    When 添加任务组
      """
      {
          "name": "学习"
      }
      """
    Then 得到成功提示
    When 添加任务组
      """
      {
          "name": "娱乐"
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
    When 添加任务列表
      """
      {
          "name": "work"
      }
      """
    When 移动任务列表"打游戏"到"娱乐"的"里面"
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group"
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
              {
                  "name": "打游戏", "task_type": "list"
              }
              ]
          },
          {
              "name": "看电影", "task_type": "list"
          },
          {
              "name": "work", "task_type": "list"
          }
      ]
      """

  @task_list @task_list_6
  Scenario: 外面的移动到里面
    Given 'Jim'登录网站
    When 添加任务组
      """
      {
          "name": "学习"
      }
      """
    Then 得到成功提示
    When 添加任务组
      """
      {
          "name": "娱乐"
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
    When 添加任务列表
      """
      {
          "name": "work"
      }
      """
    When 移动任务列表"打游戏"到"娱乐"的"里面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group"
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
              {
                  "name": "打游戏", "task_type": "list"
              }
              ]
          },
          {
              "name": "看电影", "task_type": "list"
          },
          {
              "name": "work", "task_type": "list"
          }
      ]
      """
    When 移动任务列表"work"到"打游戏"的"下面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group"
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
              {
                  "name": "打游戏", "task_type": "list"
              },
              {
                  "name": "work", "task_type": "list"
              }
              ]
          },
          {
              "name": "看电影", "task_type": "list"
          }
      ]
      """

  @task_list @task_list_7
  Scenario: 外面的移动到里面
    Given 'Jim'登录网站
    When 添加任务组
      """
      {
          "name": "学习"
      }
      """
    Then 得到成功提示
    When 添加任务组
      """
      {
          "name": "娱乐"
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
    When 添加任务列表
      """
      {
          "name": "work"
      }
      """
    When 移动任务列表"打游戏"到"娱乐"的"里面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group"
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
              {
                  "name": "打游戏", "task_type": "list"
              }
              ]
          },
          {
              "name": "看电影", "task_type": "list"
          },
          {
              "name": "work", "task_type": "list"
          }
      ]
      """
    When 移动任务列表"打游戏"到"学习"的"里面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group", "children": [
              {
                  "name": "打游戏", "task_type": "list"
              }
              ]
          },
          {
              "name": "娱乐", "task_type": "group"
          },
          {
              "name": "看电影", "task_type": "list"
          },
          {
              "name": "work", "task_type": "list"
          }
      ]
      """

  @task_list @task_list_8
  Scenario: 外面的移动到里面
    Given 'Jim'登录网站
    When 添加任务组
      """
      {
          "name": "学习"
      }
      """
    Then 得到成功提示
    When 添加任务组
      """
      {
          "name": "娱乐"
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
    When 添加任务列表
      """
      {
          "name": "work"
      }
      """
    When 移动任务列表"打游戏"到"娱乐"的"里面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group"
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
              {
                  "name": "打游戏", "task_type": "list"
              }
              ]
          },
          {
              "name": "看电影", "task_type": "list"
          },
          {
              "name": "work", "task_type": "list"
          }
      ]
      """
    When 移动任务列表"看电影"到"娱乐"的"里面"
    Then 得到错误提示"操作错误"

  @task_list_random
  Scenario: 随机测试任务列表
    Given 'Jim'登录网站
    When 添加任务组
      """
      {
          "name": "学习"
      }
      """
    Then 得到成功提示
    When 添加任务组
      """
      {
          "name": "娱乐"
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
    When 添加任务列表
      """
      {
          "name": "work"
      }
      """
    When 随机测试任务列表

  @task_list @delete_task_list1
  Scenario: 删除任务列表
    Given 'Jim'登录网站
    When 添加任务组
      """
      {
          "name": "学习"
      }
      """
    Then 得到成功提示
    When 添加任务组
      """
      {
          "name": "娱乐"
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
    When 添加任务列表
      """
      {
          "name": "work"
      }
      """
    When 删除任务列表"打游戏"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group"
          },
          {
              "name": "娱乐", "task_type": "group"
          },
          {
              "name": "看电影", "task_type": "list"
          },
          {
              "name": "work", "task_type": "list"
          }
      ]
      """

  @task_list @delete_task_list2
  Scenario: 删除组里面的任务列表
    Given 'Jim'登录网站
    When 添加任务组
      """
      {
          "name": "学习"
      }
      """
    Then 得到成功提示
    When 添加任务组
      """
      {
          "name": "娱乐"
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
    When 添加任务列表
      """
      {
          "name": "work"
      }
      """
    When 移动任务列表"打游戏"到"娱乐"的"里面"
    Then 得到成功提示
    When 移动任务列表"看电影"到"打游戏"的"下面"
    Then 得到成功提示
    When 移动任务列表"work"到"看电影"的"下面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group"
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
              {
                  "name": "打游戏", "task_type": "list"
              },
            {
                "name": "看电影", "task_type": "list"
            },
            {
                "name": "work", "task_type": "list"
            }
              ]
          }
      
      ]
      """
    When 删除任务列表"看电影"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group"
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
              {
                  "name": "打游戏", "task_type": "list"
              },
            {
                "name": "work", "task_type": "list"
            }
              ]
          }
      
      ]
      """



  @task_list @delete_task_list3
  Scenario: 删除组
    Given 'Jim'登录网站
    When 添加任务组
      """
      {
          "name": "学习"
      }
      """
    Then 得到成功提示
    When 添加任务组
      """
      {
          "name": "娱乐"
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
    When 添加任务列表
      """
      {
          "name": "work"
      }
      """
    When 移动任务列表"打游戏"到"娱乐"的"里面"
    Then 得到成功提示
    When 移动任务列表"看电影"到"打游戏"的"下面"
    Then 得到成功提示
    When 移动任务列表"work"到"看电影"的"下面"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group"
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
              {
                  "name": "打游戏", "task_type": "list"
              },
            {
                "name": "看电影", "task_type": "list"
            },
            {
                "name": "work", "task_type": "list"
            }
              ]
          }
      
      ]
      """
    When 删除任务列表"看电影"
    Then 得到成功提示
    Then 查询任务列表
      """
      [
          {
              "name": "学习", "task_type": "group"
          },
          {
              "name": "娱乐", "task_type": "group", "children": [
              {
                  "name": "打游戏", "task_type": "list"
              },
              {
                "name": "work", "task_type": "list"
              }
              ]
          }
      
      ]
      """

    When 删除任务列表"娱乐"
    Then 查询任务列表
      """
      [
        {
            "name": "学习", "task_type": "group"
        },
        {
            "name": "打游戏", "task_type": "list"
        },
        {
        "name": "work", "task_type": "list"
        }
      ]
      """