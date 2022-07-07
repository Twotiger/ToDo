class Calendar {
  constructor() {
    this.now = new Date()
    this.year = this.now.getFullYear()
    this.month = this.now.getMonth()
    this.data = {}
  }

  getDaysCountForMonth(month) {
    // 这个月有多少天
    let days = 0
    month = month + 1
    // let month = this.now.getMonth() + 1
    let year = this.now.getFullYear()
    if (month != 2) {
      if ((month == 4) || (month == 6) || (month == 9) || (month == 11)) {
        days = 30;
      } else {
        days = 31;
      }
    } else {
      if ((year % 4) == 0 && (year % 100) != 0 || year % 400 == 0) {
        days = 29;
      } else {
        days = 28;
      }

    }
    return days
  }

  getWeek(date) {
    // 周1返回1,周2返回2,星期天返回7
    let value = date.getDay()
    if (value === 0) {
      value = 7
    }
    return value
  }

  getWeekCount(year, month) {
    let date = new Date(year, month)
    let week = this.getWeek(date)
    return Math.ceil((this.getDaysCountForMonth(month) + week - 1) / 7)
  }

  nextMonth() {
    if (this.month === 11) {
      this.year += 1
      this.month = 0
    } else {
      this.month += 1
    }
  }

  lastMonth() {
    if (this.month === 0) {
      this.year -= 1
      this.month = 11
    } else {
      this.month -= 1
    }
  }

  getDays() {
    /* 返回[Date,Date,...]
    25 26 27 28 29 30 1
    2  3  4 
    ...
    30 31 1  2  3  4  5
    */
    const key = this.year.toString() + this.month.toString()
    if (key in this.data) {
      return this.data[key]
    }

    let one = new Date(this.year, this.month, 1)
    let week = this.getWeek(one)
    let res = []
    one.setDate(1 - week)

    for (let i = 0; i < this.getWeekCount(this.year, this.month); i++) {
      let tmp = []
      for (let j = 0; j < 7; j++) {
        one.setDate(one.getDate() + 1)
        tmp.push(new Date(one.valueOf()))
      }
      res.push(tmp)
    }
    this.data[key] = res
    return res
  }
}

export default Calendar