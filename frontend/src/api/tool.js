import request from '@/utils/request'

export function netseasemusic(data) {
  return request({
    url: '/tool/netseasemusic/',
    method: 'post',
    data
  })
}

export function dogecloud(data) {
  return request({
    url: '/tool/dogecloud/',
    method: 'post',
    data
  })
}