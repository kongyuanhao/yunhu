webpackJsonp([1],{"/FAz":function(t,e){},"5MvM":function(t,e){},NHnr:function(t,e,l){"use strict";function i(t){l("odBa")}function n(t){l("5MvM")}function s(t){l("/FAz")}function a(t){l("hUX/")}function r(t){l("bW6m")}Object.defineProperty(e,"__esModule",{value:!0});var c=l("TWX9"),o=l("iDdd"),u=l.n(o),d=l("zO6J"),v={name:"app"},_=function(){var t=this,e=t.$createElement,l=t._self._c||e;return l("div",{attrs:{id:"app"}},[l("router-view")],1)},f=[],p={render:_,staticRenderFns:f},h=p,g=l("/Xao"),m=i,b=g(v,h,!1,m,null,null),x=b.exports,y=l("/mxv"),w=l.n(y),C={name:"group",methods:{cleanStyle:w.a},props:{title:String,titleColor:String,labelWidth:String,labelAlign:String,labelMarginRight:String,gutter:[String,Number]}},S=function(){var t=this,e=t.$createElement,l=t._self._c||e;return l("div",[t.title?l("div",{staticClass:"weui-cells__title",style:t.cleanStyle({color:t.titleColor}),domProps:{innerHTML:t._s(t.title)}}):t._e(),t._v(" "),t._t("title"),t._v(" "),l("div",{staticClass:"weui-cells",class:{"vux-no-group-title":!t.title},style:t.cleanStyle({marginTop:"number"==typeof t.gutter?t.gutter+"px":t.gutter})},[t._t("after-title"),t._v(" "),t._t("default")],2)],2)},j=[],M={render:S,staticRenderFns:j},k=M,$=l("/Xao"),R=n,X=$(C,k,!1,R,null,null),A=X.exports,O={name:"inline-desc"},F=function(){var t=this,e=t.$createElement;return(t._self._c||e)("span",{staticClass:"vux-label-desc"},[t._t("default")],2)},T=[],W={render:F,staticRenderFns:T},D=W,E=l("/Xao"),I=s,H=E(O,D,!1,I,null,null),L=H.exports,z=l("jdWM"),N=l("9RqI"),U=l("s1ao"),B={name:"cell",components:{InlineDesc:L},props:Object(N.a)(),created:function(){},beforeMount:function(){this.hasTitleSlot=!!this.$slots.title,this.$slots.value},computed:{labelStyles:function(){return w()({width:Object(U.a)(this,"labelWidth"),textAlign:Object(U.a)(this,"labelAlign"),marginRight:Object(U.a)(this,"labelMarginRight")})},valueClass:function(){return{"vux-cell-primary":"content"===this.primary||"left"===this.valueAlign,"vux-cell-align-left":"left"===this.valueAlign,"vux-cell-arrow-transition":!!this.arrowDirection,"vux-cell-arrow-up":"up"===this.arrowDirection,"vux-cell-arrow-down":"down"===this.arrowDirection}},labelClass:function(){return{"vux-cell-justify":"justify"===Object(U.a)(this,"justify")}},style:function(){if(this.alignItems)return{alignItems:this.alignItems}}},methods:{onClick:function(){!this.disabled&&Object(z.a)(this.link,this.$router)}},data:function(){return{hasTitleSlot:!0,hasMounted:!1}}},J=function(){var t=this,e=t.$createElement,l=t._self._c||e;return l("div",{staticClass:"weui-cell",class:{"vux-tap-active":t.isLink||!!t.link,"weui-cell_access":t.isLink||!!t.link,"vux-cell-no-border-intent":!t.borderIntent,"vux-cell-disabled":t.disabled},style:t.style,on:{click:t.onClick}},[l("div",{staticClass:"weui-cell__hd"},[t._t("icon")],2),t._v(" "),l("div",{staticClass:"vux-cell-bd",class:{"vux-cell-primary":"title"===t.primary&&"left"!==t.valueAlign}},[l("p",[t.title||t.hasTitleSlot?l("label",{staticClass:"vux-label",class:t.labelClass,style:t.labelStyles},[t._t("title",[t._v(t._s(t.title))])],2):t._e(),t._v(" "),t._t("after-title")],2),t._v(" "),l("inline-desc",[t._t("inline-desc",[t._v(t._s(t.inlineDesc))])],2)],1),t._v(" "),l("div",{staticClass:"weui-cell__ft",class:t.valueClass},[t._t("value"),t._v(" "),t._t("default",[t._v(t._s(t.value))]),t._v(" "),t.isLoading?l("i",{staticClass:"weui-loading"}):t._e()],2),t._v(" "),t._t("child")],2)},P=[],Q={render:J,staticRenderFns:P},q=Q,G=l("/Xao"),V=a,K=G(B,q,!1,V,null,null),Y=K.exports,Z={components:{Group:A,Cell:Y},data:function(){return{msg:"Hello World!"}}},tt=function(){var t=this,e=t.$createElement,l=t._self._c||e;return l("div",[t._m(0,!1,!1),t._v(" "),l("group",{attrs:{title:"cell demo"}},[l("cell",{attrs:{title:"VUX",value:"cool","is-link":""}})],1)],1)},et=[function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"vux-demo"},[i("img",{staticClass:"logo",attrs:{src:l("ge4Q")}}),t._v(" "),i("h1")])}],lt={render:tt,staticRenderFns:et},it=lt,nt=l("/Xao"),st=r,at=nt(Z,it,!1,st,null,null),rt=at.exports;c.a.use(d.a);var ct=[{path:"/",component:rt}],ot=new d.a({routes:ct});u.a.attach(document.body),c.a.config.productionTip=!1,new c.a({router:ot,render:function(t){return t(x)}}).$mount("#app-box")},bW6m:function(t,e){},ge4Q:function(t,e,l){t.exports=l.p+"static/img/vux_logo.79cbb96.png"},"hUX/":function(t,e){},odBa:function(t,e){}},["NHnr"]);
//# sourceMappingURL=app.f4a436b5fd0ec91df7b3.js.map