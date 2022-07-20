import moment from "moment"
const myday = () => {
  const enToZh = {
    "Monday": "星期一",
    "Tuesday": "星期二",
    "Wednesday": "星期三",
    "Thursday": "星期四",
    "Friday": "星期五",
    "Saturday": "星期六",
    "Sunday": "星期日",
  }
  // 合理的显示repeat
  const humanizeRepeat = (repeat) => {
    if (!repeat) {
      return ""
    }
    switch (repeat.intervalType) {
      case "Daily":
        return repeat.interval === 1 ? `每天` : `每 ${repeat.interval} 天`

      case "WeekDays":
        return "工作日"

      case "Weekly":
        let weeks = []
        if (repeat.type === "custom") {
          repeat.weekdays.map((item) => {
            weeks.push(enToZh[item])
          })
        }

        let value = repeat.interval === 1 ? `每周` : `每 ${repeat.interval} 周`

        if (weeks.length > 0) {
          return value + "," + weeks.join("&")
        } else {
          return value
        }


      case "Monthly":
        return repeat.interval === 1 ? `每月` : `每 ${repeat.interval} 月`

      case "Yearly":
        return repeat.interval === 1 ? `每年` : `每 ${repeat.interval} 年`

    }
  }
  // 合理的显示日期
  const humanizeDate = (date) => {
    if (date === '') {
      return ''
    }
    const now = moment()
    const tomorrow = moment().add(1, 'days')
    const afterTomorrow = moment().add(2, 'days')

    const newDate = moment(date)
    if (now.year() === newDate.year() &&
      now.month() === newDate.month() &&
      now.date() === newDate.date()) {
      return "今天"
    } else if (tomorrow.year() === newDate.year() &&
      tomorrow.month() === newDate.month() &&
      tomorrow.date() === newDate.date()
    ) {
      return "明天"
    } else if (afterTomorrow.year() === newDate.year() &&
      afterTomorrow.month() === newDate.month() &&
      afterTomorrow.date() === newDate.date()
    ) {
      return "后天"
    } else {
      return newDate.format("YYYY-MM-DD")
    }

  }

  const humanizeDatetime = (datetime) => {
    return moment(datetime).fromNow()
  }

  return {
    humanizeRepeat,
    humanizeDate,
    humanizeDatetime
  }



}

export {
  myday
}