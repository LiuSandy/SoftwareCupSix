
<style scoped>
  .layout{
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
  }
  .layout-breadcrumb{
    padding: 10px 15px 0;
  }
  .layout-content{
    min-height: 200px;
    margin: 15px;
    overflow: hidden;
    background: #fff;
    border-radius: 4px;
  }
  .layout-content-main{
    padding: 10px;
    min-height: 800px;
  }
  .layout-copy{
    text-align: center;
    padding: 10px 0 20px;
    color: #9ea7b4;
  }
  .layout-menu-left{
    background: #464c5b;
  }
  .layout-header{
    height: 60px;
    background: #fff;
    box-shadow: 0 1px 1px rgba(0,0,0,.1);
  }
  .layout-logo-left{
    width: 90%;
    height: 30px;
    background: #5b6270;
    border-radius: 3px;
    margin: 15px auto;
  }
  .layout-ceiling-main a{
    color: #9ba7b5;
  }
  .layout-hide-text .layout-text{
    display: none;
  }
  .ivu-col{
    transition: width .2s ease-in-out;
  }
</style>
<template>
  <div class="layout" :class="{'layout-hide-text': spanLeft < 5}">
    <Row type="flex">
      <i-col :span="spanLeft" class="layout-menu-left">
        <Menu active-name="1" theme="dark" width="auto">
          <div class="layout-logo-left"></div>
          <router-link to="/">
            <Menu-item name="1">
              <Icon type="navicon-round" :size="iconSize"></Icon>
              <span class="layout-text">整体状况</span>
            </Menu-item>
          </router-link>
          <Submenu name="2">
              <template slot="title">
              <Icon type="ios-keypad" :size="iconSize"></Icon>
              <span class="layout-text">详情分析</span>
              </template>
              <router-link :to="{path: '/sale'}"><Menu-item name="2-1">销售信息</Menu-item></router-link>
              <router-link :to="{path: '/degree'}"><Menu-item name="2-2">销售关系</Menu-item></router-link>
              <!-- <router-link :to="{path: '/PageRank'}"><Menu-item name="2-3">PageRank</Menu-item></router-link> -->
          </Submenu>
          <Submenu name="3">
              <template slot="title">
              <Icon type="ios-keypad" :size="iconSize"></Icon>
              <span class="layout-text">预测分析</span>
              </template>
              <router-link :to="{path: '/history'}"><Menu-item name="3-1">历史交易信息</Menu-item></router-link>
              <router-link :to="{path: '/predict'}"><Menu-item name="3-2">预测数据</Menu-item></router-link>
          </Submenu>
          <router-link to="/upload">
            <Menu-item name="4">
              <Icon type="upload" :size="iconSize"></Icon>
              <span >地位计算</span>
            </Menu-item>
          </router-link>
          <router-link to="/login">
            <Menu-item name="5">
              <Icon type="log-out" :size="iconSize"></Icon>
              <span >退出</span>
            </Menu-item>
          </router-link>

          <!-- <MenuItem name="4" @click="LoginOut">
            <Icon type="log-out"></Icon>
            <router-link :to="{path: '/login'}" style="color:#FFF">退出</router-link>
          </MenuItem> -->
        </Menu>
      </i-col>
      <i-col :span="spanRight">
        <div class="layout-header">
          <i-button type="text" @click="toggleClick">
            <Icon type="navicon" size="32"> </Icon>
          </i-button>
            <span style="font-size:20px">民航机票代理市场的预测及可视化</span>

        </div>

        <div class="layout-content">
          <div class="layout-content-main">
            <router-view></router-view>
          </div>
        </div>
        <div class="layout-copy">
          2011-2016 &copy; TalkingData
        </div>
      </i-col>
    </Row>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        spanLeft: 5,
        spanRight: 19
      }
    },
    computed: {
      iconSize () {
        return this.spanLeft === 5 ? 14 : 24
      }
    },
    methods: {
      LoginOut () {
        localStorage.clear()
        this.$router.push('/login')
      },
      toggleClick () {
        if (this.spanLeft === 5) {
          this.spanLeft = 2
          this.spanRight = 22
        } else {
          this.spanLeft = 5
          this.spanRight = 19
        }
      }
    }
  }
</script>
