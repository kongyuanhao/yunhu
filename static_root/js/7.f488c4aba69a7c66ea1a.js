webpackJsonp([7],{"1Rlq":function(n,t,o){t=n.exports=o("BkJT")(!0),t.push([n.i,"\n.demonUI[data-v-2b3344b0] {\n  position: relative;\n  width: 100%;\n  height: 100%;\n  background-image: url("+o("OhjC")+");\n  background-repeat: no-repeat;\n  background-size: cover;\n}\n.demonUI .Login[data-v-2b3344b0] {\n  position: absolute;\n  top: 50%;\n  left: 50%;\n  -webkit-transform: translate(-50%, -50%);\n          transform: translate(-50%, -50%);\n  -webkit-box-sizing: border-box;\n          box-sizing: border-box;\n  padding: 20px;\n  width: 100%;\n}\n.demonUI .Login .dm-input .loginInput[data-v-2b3344b0] {\n  color: #fff;\n}\n.demonUI .Login .dm-input .sendCode[data-v-2b3344b0] {\n  padding: 10px;\n  color: #969696;\n  background-color: #ffffff;\n  border-radius: 0 5px 5px 0;\n}\n","",{version:3,sources:["/Users/demongao/Documents/GitHub/yunhu/src/pages/Login.vue"],names:[],mappings:";AACA;EACE,mBAAmB;EACnB,YAAY;EACZ,aAAa;EACb,gDAA+C;EAC/C,6BAA6B;EAC7B,uBAAuB;CACxB;AACD;EACE,mBAAmB;EACnB,SAAS;EACT,UAAU;EACV,yCAAyC;UACjC,iCAAiC;EACzC,+BAA+B;UACvB,uBAAuB;EAC/B,cAAc;EACd,YAAY;CACb;AACD;EACE,YAAY;CACb;AACD;EACE,cAAc;EACd,eAAe;EACf,0BAA0B;EAC1B,2BAA2B;CAC5B",file:"Login.vue",sourcesContent:['\n.demonUI[data-v-2b3344b0] {\n  position: relative;\n  width: 100%;\n  height: 100%;\n  background-image: url("../assets/loginbg.jpg");\n  background-repeat: no-repeat;\n  background-size: cover;\n}\n.demonUI .Login[data-v-2b3344b0] {\n  position: absolute;\n  top: 50%;\n  left: 50%;\n  -webkit-transform: translate(-50%, -50%);\n          transform: translate(-50%, -50%);\n  -webkit-box-sizing: border-box;\n          box-sizing: border-box;\n  padding: 20px;\n  width: 100%;\n}\n.demonUI .Login .dm-input .loginInput[data-v-2b3344b0] {\n  color: #fff;\n}\n.demonUI .Login .dm-input .sendCode[data-v-2b3344b0] {\n  padding: 10px;\n  color: #969696;\n  background-color: #ffffff;\n  border-radius: 0 5px 5px 0;\n}\n'],sourceRoot:""}])},OhjC:function(n,t,o){n.exports=o.p+"static/img/loginbg.5e40249.jpg"},P7ry:function(n,t,o){"use strict";function e(n){o("Y7iZ")}Object.defineProperty(t,"__esModule",{value:!0});var i=o("vpGR"),a=o("MLG2"),s=o("hTFN"),r=o("8kIB"),d=o("xwk4"),c=o("TpY+"),u={mixins:[d.a,c.a],props:["identification"],data:function(){return{tel:"",code:""}},components:{XInput:i.a,Group:a.a,XButton:s.a,Box:r.a},computed:{},methods:{sendCode:function(){if(""===this.trim(this.tel))return void this.$vux.toast.text("手机号码不能为空");this.$axios.post({url:"/telcheck/",data:{tel:this.tel}}).then(function(n){console.log(n)})},nextFocus:function(n){this.$refs[n].focus()},submit:function(){var n=this;this.formMixin_submit("/h5register/").then(function(t){localStorage.setItem("yunhu!customer_id",t.customer_id);var o=n;n.$vux.toast.show({text:"登陆成功",time:500,onHide:function(){o.routerLink("Index",{identification:o.identification},{checkway:o.$route.query.checkway})}})}).catch(function(n){console.log("code:"+n.code+" \n msg:"+n.msg)})}},mounted:function(){}},l=function(){var n=this,t=n.$createElement,o=n._self._c||t;return o("div",{staticClass:"demonUI"},[o("div",{staticClass:"Login"},[o("group",{staticClass:"dm-input dm-input-placeholder-white"},[o("x-input",{ref:"tel",staticClass:"loginInput",attrs:{name:"tel",placeholder:"请输入手机号",required:!0},on:{"on-enter":function(t){n.nextFocus("code")}},model:{value:n.tel,callback:function(t){n.tel=t},expression:"tel"}})],1),n._v(" "),o("group",{staticClass:"dm-input dm-input-placeholder-white"},[o("x-input",{ref:"code",staticClass:"loginInput",attrs:{name:"code",placeholder:"请填写验证码",required:!0},model:{value:n.code,callback:function(t){n.code=t},expression:"code"}}),n._v(" "),o("span",{staticClass:"sendCode",on:{click:n.sendCode}},[n._v("发送验证码")])],1),n._v(" "),o("box",{attrs:{gap:"50px 0 0"}},[o("x-button",{attrs:{type:"confirm",disabled:n.submitLoadding,"show-loading":n.submitLoadding,gradients:["#1D62F0","#19D5FD"]},nativeOn:{click:function(t){n.submit(t)}}},[n._v(" 登录\n            ")])],1)],1)])},A=[],p={render:l,staticRenderFns:A},b=p,f=o("/Xao"),g=e,m=f(u,b,!1,g,"data-v-2b3344b0",null);t.default=m.exports},Y7iZ:function(n,t,o){var e=o("1Rlq");"string"==typeof e&&(e=[[n.i,e,""]]),e.locals&&(n.exports=e.locals);o("8bSs")("3f9a7feb",e,!0)}});
//# sourceMappingURL=7.f488c4aba69a7c66ea1a.js.map