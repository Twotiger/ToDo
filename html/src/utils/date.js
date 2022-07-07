import moment from "moment"
const getDeadlineStr = (value) => {
  if (value === '') {
    return ''
  }
  let date = moment(value).format("YYYY-MM-DD")
  if (date === moment().format("YYYY-MM-DD")) {
    return "今天"
  } else if (date === moment().add(1, 'd').format("YYYY-MM-DD")) {
    return "明天"
  } else if (date === moment().add(2, 'd').format("YYYY-MM-DD")) {
    return "后天"
  } else {
    return date
  }

}

const getNoticeStr = (value) => {
  if (value === '') {
    return ''
  }
  let m = moment(value)
  let date = m.format("YYYY-MM-DD")
  let time = m.format("HH:mm")
  if (date === moment().format("YYYY-MM-DD")) {
    return `今天 ${time}`
  } else if (date === moment().add(1, 'd').format("YYYY-MM-DD")) {
    return `明天 ${time}`
  } else if (date === moment().add(2, 'd').format("YYYY-MM-DD")) {
    return `后天 ${time}`
  } else {
    return date
  }
}

export {
  getDeadlineStr,
  getNoticeStr
}