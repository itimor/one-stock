// set function parseTime,formatTime to filter
export { parseTime, formatTime } from '@/utils'

function pluralize(time, label) {
  if (time === 1) {
    return time + label
  }
  return time + label + 's'
}

export function timeAgo(time) {
  const between = Date.now() / 1000 - Number(time)
  if (between < 3600) {
    return pluralize(~~(between / 60), ' minute')
  } else if (between < 86400) {
    return pluralize(~~(between / 3600), ' hour')
  } else {
    return pluralize(~~(between / 86400), ' day')
  }
}

/* 数字 格式化*/
export function numberFormatter(num, digits) {
  const si = [
    { value: 1E18, symbol: 'E' },
    { value: 1E15, symbol: 'P' },
    { value: 1E12, symbol: 'T' },
    { value: 1E9, symbol: 'G' },
    { value: 1E6, symbol: 'M' },
    { value: 1E3, symbol: 'k' }
  ]
  for (let i = 0; i < si.length; i++) {
    if (num >= si[i].value) {
      return (num / si[i].value + 0.1).toFixed(digits).replace(/\.0+$|(\.[0-9]*[1-9])0+$/, '$1') + si[i].symbol
    }
  }
  return num.toString()
}

export function toThousandFilter(num) {
  return (+num || 0).toString().replace(/^-?\d+/g, m => m.replace(/(?=(?!\b)(\d{3})+$)/g, ','))
}

// 格式化日期
export function parseDate(datestr) {
  if (datestr !== undefined) {
    const date = datestr.slice(0, 10)
    const time = datestr.slice(11, 19)
    return date + ' ' + time
  }
}

// 格式化时间 09:30:00.0000
export function parseTimeZ(datestr) {
  if (datestr !== undefined) {
    const time = datestr.slice(0, 8)
    return time
  }
}

export function diffDate(date) {
  const d1 = new Date()
  const d2 = new Date(date)
  return Math.round(parseInt(d2 - d1) / 1000 / 60 / 60 / 24)
}

// 菜单
export function menuTypeFilter(val) {
  const Map = {
    1: '模块',
    2: '菜单',
    3: '操作'
  }
  return Map[val]
}

// 按钮
export function operateTypeFilter(val) {
  const Map = {
    'none': '无',
    'add': '新增',
    'del': '删除',
    'update': '编辑',
    'view': '查看',
  }
  return Map[val]
}

// 取第一个字母并大写
export function AvatarFilter(val) {
  return val.substr(0, 1).toUpperCase()
}

export function VolumeFilter (val) {
    const f = 2 // 保留2位小数
    let pre = '' // 前缀
    let v = val
    if (v < 0) {
      pre = '-'
      v = val.toString().split('-')[1]
    }
    if (v >= 100000000) {
      v = (v / 100000000).toFixed(f) + '亿'
      } else if (v >= 10000000) {
      v = (v / 10000000).toFixed(f) + '千万'
      } else if (v >= 10000000) {
      v = (v / 10000000).toFixed(f) + '百万'
      } else if (v >= 10000) {
      v = (v / 10000).toFixed(f) + '万'
      } else {
      v = v +''
      }
      return pre + v
  }
