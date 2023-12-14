import Request from '@/api/common'

// auth
import * as auths from '@/api/auths'
export const auth = auths

// systems
export const user = new Request('/sys/user/')
export const group = new Request('/sys/group/')
export const role = new Request('/sys/role/')
export const menu = new Request('/sys/menu/')
export const perm = new Request('/sys/perm/')

// tools
export const audit = new Request('/tool/audit/')
export const simple = new Request('/tool/simple/')

// notices
export const email = new Request('/notice/email/')
export const telegram = new Request('/notice/telegram/')
export const to = new Request('/notice/to/')

// stocks
export const stocks = new Request('/stock/stocks/')
export const stockdaily = new Request('/stock/stockdaily/')
export const stockchange = new Request('/stock/stockchange/')
export const stockchangefilter = new Request('/stock/stockchangefilter/')

// stock
import * as stock from '@/api/stock'
export const c_stock = stock

// tool
import * as tool from '@/api/tool'
export const c_tool = tool