import request from '@/utils/request'

export function stockinfo(data) {
  return request({
    url: '/stock/stockdaily/stockinfo/',
    method: 'post',
    data
  })
}

export function is_first_zt(data) {
  return request({
    url: '/stock/stockdaily/is_first_zt/',
    method: 'post',
    data
  })
}