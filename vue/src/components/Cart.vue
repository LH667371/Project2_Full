<template>
    <div class="cart">
        <Header></Header>
        <div class="cart_info">
            <div class="cart_title">
                <span class="text">我的购物车</span>
                <span class="total">共{{ $store.state.cart_length }}门课程</span>
            </div>
            <div class="cart_table">
                <div class="cart_head_row">
                    <span class="doing_row"></span>
                    <span class="course_row">课程</span>
                    <span class="expire_row">有效期</span>
                    <span class="price_row">单价</span>
                    <span class="do_more">操作</span>
                </div>
                <div class="cart_course_list" v-for="(course, index) in this.$store.state.cart_list" :key="index">
                    <CartItem :course="course" @c_price="change_price"></CartItem>
                    <hr>
                </div>
                <div class="cart_footer_row">
                    <span class="cart_select">
                        <label>
                            <el-checkbox v-model="checked" @change="change_all_select"></el-checkbox>
                            <span>全选</span>
                        </label>
                    </span>
                    <span class="cart_delete">
                        <el-popconfirm icon="el-icon-info"
                                       icon-color="red"
                                       :title="'确定删除勾选的吗？'"
                                       @confirm="del_course">
                            <span slot="reference"><i class="el-icon-delete"> 删除</i></span>
                        </el-popconfirm>
                    </span>
                    <span class="goto_pay" @click="go_order">去结算</span>
                    <span class="cart_total">总计：¥{{ parseFloat(price).toFixed(2) }}</span>
                </div>
            </div>
        </div>
        <Footer></Footer>
    </div>
</template>

<script>
import CartItem from "./CartItem";
import Footer from "./common/Footer";
import Header from "./common/Header";

export default {
    name: "Cart",
    components: {
        CartItem,
        Footer,
        Header,
    },
    data() {
        return {
            token: "",
            checked: false,
            price: 0.00,
        }
    },
    created() {
        this.check_user_login();
        this.get_cart_list();
    },
    watch: {
        "$store.state.select_id"() {
            this.checked = this.$store.state.select_id.length !== 0 ? this.$store.state.select_id.length === this.$store.state.cart_list.length : false;
            this.change_price();
        },
    },
    methods: {
        // 获取购物车的数据
        get_cart_list() {
            this.$store.commit('give_cart_list', []);
            this.$store.commit('all_del_select', true);
            this.$axios.get(this.$settings.HOST + "cart/option/", {
                headers: {
                    "Authorization": "auth " + sessionStorage.token
                }
            }).then(res => {
                // console.log(res);
                this.$store.commit("change_count", res.data.length === 0 ? '' : res.data.length);
                this.$store.commit('give_cart_list', res.data);
                for (let i = 0; i < res.data.length; i++)
                    if (res.data[i].selected)
                        this.$store.commit('add_select', res.data[i].course_id)
                this.checked = this.$store.state.select_id.length !== 0 ? this.$store.state.select_id.length === res.data.length : false;
            }).catch(error => {
                console.log(error);
                if (error.response.data.detail === "Signature has expired.")
                    this.$confirm("登录已过期，请重新登录，点击确认可前往登录！").then(() => {
                        this.$store.commit('change_username', '');
                        this.$store.commit('change_count', '');
                        sessionStorage.clear();
                        this.$router.push('/login');
                    })
            })
        },
        // 用户在操作购物车时必须已经登录
        check_user_login() {
            if (!sessionStorage.token) {
                this.$confirm("请登录后再查看购物车，点击确认可前往登录！").then(() => {
                    this.$router.push('/login');
                }).catch( () => {
                    this.$router.push('/');
                })
                return false;
            }
        },
        // 发起请求修改redis中的选中状态
        change_all_select() {
            let course_id = [];
            if (this.$store.state.cart_list) {
                for (let i = 0; i < this.$store.state.cart_list.length; i++)
                    course_id.push(this.$store.state.cart_list[i].course_id);
            }
            this.$axios.put(this.$settings.HOST + "cart/option/", {
                course_id: course_id,
                selected: this.checked,
            }, {
                headers: {
                    "Authorization": "auth " + sessionStorage.token
                }
            }).then(res => {
                // console.log(res);
                if (this.checked) {
                    this.$message('全部勾选 ');
                    this.$store.commit('all_del_select', true);
                    for (let i = 0; i < this.$store.state.cart_list.length; i++)
                        if (this.$store.state.cart_list[i].selected)
                            this.$store.commit('add_select', this.$store.state.cart_list[i].course_id);
                } else {
                    this.$message('取消全部 ');
                    this.$store.commit('all_del_select', true);
                }
            }).catch(error => {
                console.log(error);
                if (error.response.data.detail === "Signature has expired.")
                    this.$confirm("登录已过期，请重新登录，点击确认可前往登录！").then(() => {
                        this.$store.commit('change_username', '');
                        this.$store.commit('change_count', '');
                        sessionStorage.clear();
                        this.$router.push('/login');
                    })
            })
        },
        del_course() {
            let course_id = this.$store.state.select_id;
            this.$store.commit('all_del_select', true);
            if (course_id.length > 0)
                this.$axios({
                    url: this.$settings.HOST + "cart/option/",
                    method: 'delete',
                    data: {
                        course_id: course_id,
                    },
                    headers: {
                        "Authorization": "auth " + sessionStorage.token
                    }
                }).then(res => {
                    // console.log(res);
                    this.$store.commit('change_count', this.$store.state.cart_length - course_id.length > 0 ? this.$store.state.cart_length - course_id.length : '');
                    for (let i = 0; i < this.$store.state.cart_list.length; i++)
                        for (let j = 0; j < course_id.length; j++) {
                            if (this.$store.state.cart_list[i].course_id === course_id[j]) {
                                this.$store.state.cart_list.splice(i, 1);
                            }
                        }
                    this.$message({
                        message: '已删除!',
                        type: "success"
                    });
                }).catch(error => {
                    console.log(error);
                    if (error.response.data.detail === "Signature has expired.")
                        this.$confirm("登录已过期，请重新登录，点击确认可前往登录！").then(() => {
                            this.$store.commit('change_username', '');
                            this.$store.commit('change_count', '');
                            sessionStorage.clear();
                            this.$router.push('/login');
                        })
                    else
                        this.$message({
                            message: '删除失败!',
                            type: "error"
                        });
                })
            else
                this.$message({
                    message: '需要您进行勾选需要删除的商品!',
                    type: "error"
                });
        },
        change_price() {
            this.price = 0;
            for (let i = 0; i < this.$store.state.cart_list.length; i++)
                for (let j = 0; j < this.$store.state.select_id.length; j++) {
                    if (this.$store.state.cart_list[i].course_id === this.$store.state.select_id[j]) {
                        if (this.$store.state.cart_list[i].expire_price !== null)
                            this.price += parseFloat(this.$store.state.cart_list[i].expire_price);
                        else
                            this.price += parseFloat(this.$store.state.cart_list[i].price);
                    }
                }
        },
        go_order() {
            if (this.$store.state.cart_list.length !== 0)
                this.$router.push("/order");
            else
                this.$message.error('没有加购商品，无法进行结算！');
        }
    },
}
</script>

<style scoped>
.cart {
    /*margin-top: 80px;*/
    display: flex;
    min-height: 100vh;
    flex-direction: column;
}

.cart_info {
    flex: 1;
    width: 1200px;
    margin: 0 auto 10px;
}

.cart_title {
    margin: 25px 0;
}

.cart_title .text {
    font-size: 18px;
    color: #666;
}

.cart_title .total {
    font-size: 12px;
    color: #d0d0d0;
}

.cart_table {
    width: 1170px;
}

.cart_course_list {
    margin-top: 10px;
    margin-bottom: -8px;
    width: 1200px;
}

.cart_course_list hr {
    border: solid 1px #F7F7F7;
    height: 0;
}

.cart_table .cart_head_row {
    background: #F7F7F7;
    width: 100%;
    height: 80px;
    line-height: 80px;
    padding-right: 30px;
}

.cart_table .cart_head_row::after {
    content: "";
    display: block;
    clear: both;
}

.cart_table .cart_head_row .doing_row,
.cart_table .cart_head_row .course_row,
.cart_table .cart_head_row .expire_row,
.cart_table .cart_head_row .price_row,
.cart_table .cart_head_row .do_more {
    padding-left: 10px;
    height: 80px;
    float: left;
}

.cart_table .cart_head_row .doing_row {
    width: 148px;
}

.cart_table .cart_head_row .course_row {
    width: 470px;
}

.cart_table .cart_head_row .expire_row {
    width: 178px;
}

.cart_table .cart_head_row .price_row {
    width: 156px;
}

.cart_table .cart_head_row .do_more {
    width: 162px;
}

.cart_footer_row {
    padding-left: 30px;
    background: #F7F7F7;
    width: 100%;
    height: 80px;
    line-height: 80px;
}

.cart_footer_row .cart_select span {
    font-size: 15px;
    color: #666;
}

.cart_footer_row .cart_select label {
    padding-left: 3px;
}

.cart_footer_row .cart_delete {
    margin-left: 58px;
}

.cart_footer_row .cart_delete i {
    font-size: 15px;
    color: #666;
}

.cart_footer_row .cart_delete i:hover {
    cursor: default;
    color: #ffc210;
}

.cart_delete .el-icon-delete {
    font-size: 16px;
    color: #666;
}

.cart_delete span {
    margin-left: 15px;
    cursor: pointer;
    font-size: 18px;
    color: #666;
}

.cart_total {
    float: right;
    margin-right: 62px;
    font-size: 18px;
    color: #666;
}

.goto_pay {
    float: right;
    width: 159px;
    height: 80px;
    outline: none;
    border: none;
    background: #ffc210;
    font-size: 18px;
    color: #fff;
    text-align: center;
    cursor: pointer;
}
</style>
