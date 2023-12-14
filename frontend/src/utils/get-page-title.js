import i18n from '@/lang'

const title = i18n.t("system_title") || '后台管理系统'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} | ${title}`
  }
  return `${title}`
}
