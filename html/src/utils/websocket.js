import User from '@/domain/user'
import { notification } from './notification.js'

class Websocket {
  constructor() {
    this.ws = {}
  }

  connect() {
    const user = new User()
    let websocketURL = import.meta.env.ENV_WEBSOCKET_URL
    this.ws = new WebSocket(websocketURL)
    this.ws.onopen = () => {
      this.send({ token: user.getToken() })
    }
    this.ws.onmessage = (event) => {
      const jsonData = JSON.parse(event.data)
      if (jsonData.type === 'notification') {
        notification("TODO 消息提醒", jsonData["task_name"])
      }
    }
    this.ws.onclose = () => {
      console.log('disconnected')
    }
  }

  send(message) {
    this.ws.send(JSON.stringify(message))
  }
}

let websocket = new Websocket()

export default websocket