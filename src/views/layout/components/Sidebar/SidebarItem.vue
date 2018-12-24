<template>
  <div v-if="!item.hidden&&item.children" class="menu-wrapper">

    <template v-if="hasOneShowingChild(item.children,item) && (!onlyOneChild.children||onlyOneChild.noShowingChildren)&&!item.alwaysShow">
      <app-link :to="resolvePath(onlyOneChild.power_path)">
        <el-menu-item :index="resolvePath(onlyOneChild.power_path)" :class="{'submenu-title-noDropdown':!isNest}">
          <item v-if="onlyOneChild.power_meta" :icon="onlyOneChild.power_meta.powermeta_icon||item.power_meta.powermeta_icon" :title="onlyOneChild.power_meta.powermeta_title" />
        </el-menu-item>
      </app-link>
    </template>

    <el-submenu v-else :index="resolvePath(item.power_path)">
      <template slot="title">
        <item v-if="item.power_meta" :icon="item.power_meta.powermeta_icon" :title="item.power_meta.powermeta_title" />
      </template>

      <template v-for="child in item.children" v-if="!child.power_hidden">
        <sidebar-item
          v-if="child.children&&child.children.length>0"
          :is-nest="true"
          :item="child"
          :key="child.power_path"
          :base-path="resolvePath(child.power_path)"
          class="nest-menu" />
        <app-link v-else :to="resolvePath(child.power_path)" :key="child.power_meta.powermeta_title">
          <el-menu-item :index="resolvePath(child.power_path)">
            <item v-if="child.power_meta" :icon="child.power_meta.powermeta_icon" :title="child.power_meta.powermeta_title" />
          </el-menu-item>
        </app-link>
      </template>
    </el-submenu>

  </div>
</template>

<script>
import path from 'path'
import { isExternal } from '@/utils'
import Item from './Item'
import AppLink from './Link'

export default {
  name: 'SidebarItem',
  components: { Item, AppLink },
  props: {
    // route object
    item: {
      type: Object,
      required: true
    },
    isNest: {
      type: Boolean,
      default: false
    },
    basePath: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      onlyOneChild: null
    }
  },
  methods: {
    hasOneShowingChild(children, parent) {
      const showingChildren = children.filter(item => {
        if (item.hidden) {
          return false
        } else {
          // Temp set(will be used if only has one showing child)
          this.onlyOneChild = item
          return true
        }
      })

      // When there is only one child router, the child router is displayed by default
      if (showingChildren.length === 1) {
        return true
      }

      // Show parent if there are no child router to display
      if (showingChildren.length === 0) {
        this.onlyOneChild = { ... parent, path: '', noShowingChildren: true }
        return true
      }

      return false
    },
    resolvePath(routePath) {
      if (this.isExternalLink(routePath)) {
        return routePath
      }
      return path.resolve(this.basePath, routePath)
    },
    isExternalLink(routePath) {
      return isExternal(routePath)
    }
  }
}
</script>
