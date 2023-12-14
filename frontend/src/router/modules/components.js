/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const componentsRouter = {
  path: '/omponents-demo',
  component: Layout,
  redirect: 'noRedirect',
  name: 'ComponentDemo',
  meta: {
    title: 'ComponentDemo',
    icon: 'component'
  },
  children: [
    {
      path: 'clipboard',
      component: () => import('@/views/components-demo/clipboard'),
      name: 'clipboard',
      meta: { title: 'clipboard' }
    },
    {
      path: 'sticky',
      component: () => import('@/views/components-demo/sticky'),
      name: 'StickyDemo',
      meta: { title: 'Sticky' }
    },
    {
      path: 'mixin',
      component: () => import('@/views/components-demo/mixin'),
      name: 'ComponentMixinDemo',
      meta: { title: 'Component Mixin' }
    }
  ]
}

export default componentsRouter
