<template>
    <el-form
        :model="loginForm"
        :rules="fieldRules"
        ref="loginForm"
        label-position="left"
        label-width="0px"
        class="demo-ruleForm login-container"
    >
        <h2 class="title">授客测试管理系统</h2>
        <el-form-item prop="account">
            <el-input
                type="text"
                v-model="loginForm.account"
                auto-complete="off"
                placeholder="请输入您的账号\邮箱\手机号"
                @keyup.enter.native="login"
            ></el-input>
        </el-form-item>
        <el-form-item prop="password">
            <el-input
                type="password"
                v-model="loginForm.password"
                auto-complete="off"
                placeholder="请输入密码"
                @keyup.enter.native="login"
            ></el-input>
        </el-form-item>
        <!-- <el-form-item> -->
        <!-- <el-col :span="12">
                <el-form-item prop="captcha">
                    <el-input
                        type="test"
                        v-model="loginForm.captcha"
                        auto-complete="off"
                        placeholder="验证码, 单击图片刷新"
                        style="width: 100%;"
                    ></el-input>
                </el-form-item>
        </el-col>-->
        <!-- <el-col class="line" :span="1">&nbsp;</el-col> -->
        <!-- <el-col :span="11">
                <el-form-item>
                    <img
                        style="width: 100%;"
                        class="pointer"
                        :src="loginForm.src"
                        @click="refreshCaptcha"
                    />
                </el-form-item>
        </el-col>-->
        <!-- </el-form-item> -->
        <!-- <el-checkbox v-model="checked" checked class="remember">记住密码</el-checkbox> -->
        <el-form-item style="width:100%;">
            <el-button type="primary" style="width:48%;" @click.native.prevent="reset">重 置</el-button>
            <el-button
                type="primary"
                style="width:48%;"
                @click.native.prevent="login"
                :loading="loading"
            >登 录</el-button>
        </el-form-item>
    </el-form>
</template>

<script>
import { mapState } from "vuex";
import Cookies from "js-cookie";

export default {
    name: "Login",
    data() {
        return {
            loading: false,
            loginForm: {
                account: "admin",
                password: "admin",
                captcha: "",
                src: ""
            },
            fieldRules: {
                account: [
                    { required: true, message: "请输入账号", trigger: "blur" }
                ],
                password: [
                    { required: true, message: "请输入密码", trigger: "blur" }
                ]
                // ,
                // captcha: [
                //   { required: true, message: '请输入验证码', trigger: 'blur' }
                // ]
            }
            // checked: true
        };
    },
    methods: {
        login() {
            this.loading = true; // 设置为加载状态
            let userInfo = {
                account: this.loginForm.account,
                password: this.loginForm.password,
                captcha: this.loginForm.captcha
            };
            this.$api.login
                .login(userInfo)
                .then(res => {
                    if (res.success) {
                        Cookies.set("token", res.data.token); // 保存token到Cookie
                        sessionStorage.setItem(
                            "refreshToken",
                            res.data.refreshToken
                        ); // 保存刷新token到本地会话

                        sessionStorage.setItem("name", res.data.name); // 保存用户姓名到本地会话
                        this.$store.commit(
                            "setUserGroups",
                            res.data.userGroups
                        ); // 用户用户关联的组别
                        this.$store.commit("setUserId", res.data.userId); // 保存用户id
                        this.$store.commit("setUserName", res.data.name); // 保存用户真是姓名
                        this.$store.commit("setNavMenu", undefined); // 重置菜单资源
                        this.$store.commit("setMenuRouteLoadStatus", false); // 重置导航菜单加载状态为false
                        this.$store.commit("setUserPerms", res.data.perms); // 保存用户权限标识
                        this.$store.commit(
                            "setIsSuperUser",
                            res.data.isSuperuser
                        ); // 保存是否超级管理员用户标识
        
                        if (JSON.stringify(this.$route.query) != "{}") {
                            this.$router.push(this.$route.query.redirect); // 登录成功，跳转之前页面
                        } else {// 不需要跳转到登录前的页面
                            this.$router.push("/");
                        }
                        this.$message({
                            message: res.msg,
                            type: "success"
                        });
                    } else {
                        this.loading = false;
                        this.$message.error(res.msg);
                    }
                    this.loading = false;
                })
                .catch(res => {
                    this.$message.error(res.msg);
                    this.loading = false;
                });
        },
        refreshCaptcha: function() {
            this.loginForm.src =
                this.$globalConstant.baseUrl +
                "/captcha.jpg?t=" +
                new Date().getTime();
        },
        reset() {
            this.$refs.loginForm.resetFields();
        }
    },
    mounted() {
        this.refreshCaptcha();
    },
    computed: {
        ...mapState({
            themeColor: state => state.app.themeColor
        })
    }
};
</script>

<style lang="scss" scoped>
.login-container {
    -webkit-border-radius: 5px;
    border-radius: 5px;
    -moz-border-radius: 5px;
    background-clip: padding-box;
    margin: 100px auto;
    width: 400px;
    padding: 35px 35px 15px 35px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;

    // 登录系统 标题居中及背景色设置
    .title {
        margin: 0px auto 30px auto;
        text-align: center;
        color: #505458;
    }
    // .remember {
    //   margin: 0px 0px 35px 0px;
    // }
}
</style>