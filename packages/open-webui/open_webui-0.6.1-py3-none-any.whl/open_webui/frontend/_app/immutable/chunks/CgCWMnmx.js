import{s as ft,y as De,k as q,e as m,t as R,o as A,c as h,a as _,d,b as W,f as c,i as te,g as r,u as ge,z as dt,A as We,h as J,H as mt,j as rt,p as ht,n as Ye,B as ve,C as Fe}from"./vexCXLX9.js";import{S as _t,i as pt,f as Ge,b as X,d as Z,m as x,g as gt,a as L,c as vt,t as O,e as ee}from"./Cdll-xsj.js";import{C as wt}from"./DGZyJbQE.js";import{g as bt}from"./7pUP5QFf.js";import{C as yt}from"./CzvQehHf.js";import{C as kt}from"./Dzg7Oazf.js";import{T as Ue}from"./DzHlmjPS.js";import{A as Et,L as It}from"./B7bv6E6x.js";import{u as Tt}from"./BWfq-JMv.js";function Ct(s){let e,t,n,u,a;return t=new kt({props:{strokeWidth:"2.5"}}),{c(){e=m("button"),X(t.$$.fragment),this.h()},l(i){e=h(i,"BUTTON",{class:!0,type:!0});var p=_(e);Z(t.$$.fragment,p),p.forEach(d),this.h()},h(){c(e,"class","w-full text-left text-sm py-1.5 px-1 rounded-lg dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-gray-850"),c(e,"type","button")},m(i,p){te(i,e,p),x(t,e,null),n=!0,u||(a=ge(e,"click",s[20]),u=!0)},p:Ye,i(i){n||(O(t.$$.fragment,i),n=!0)},o(i){L(t.$$.fragment,i),n=!1},d(i){i&&d(e),ee(t),u=!1,a()}}}function Dt(s){let e,t,n,u;return{c(){e=m("input"),this.h()},l(a){e=h(a,"INPUT",{class:!0,type:!0,placeholder:!0}),this.h()},h(){c(e,"class","w-full text-2xl font-medium bg-transparent outline-hidden font-primary"),c(e,"type","text"),c(e,"placeholder",t=s[12].t("Tool Name")),e.required=!0},m(a,i){te(a,e,i),ve(e,s[0]),n||(u=ge(e,"input",s[21]),n=!0)},p(a,i){i[0]&4096&&t!==(t=a[12].t("Tool Name"))&&c(e,"placeholder",t),i[0]&1&&e.value!==a[0]&&ve(e,a[0])},d(a){a&&d(e),n=!1,u()}}}function Pt(s){let e,t;return e=new Ue({props:{className:"w-full",content:s[12].t("e.g. my_tools"),placement:"top-start",$$slots:{default:[qt]},$$scope:{ctx:s}}}),{c(){X(e.$$.fragment)},l(n){Z(e.$$.fragment,n)},m(n,u){x(e,n,u),t=!0},p(n,u){const a={};u[0]&4096&&(a.content=n[12].t("e.g. my_tools")),u[0]&4132|u[1]&16&&(a.$$scope={dirty:u,ctx:n}),e.$set(a)},i(n){t||(O(e.$$.fragment,n),t=!0)},o(n){L(e.$$.fragment,n),t=!1},d(n){ee(e,n)}}}function Vt(s){let e,t;return{c(){e=m("div"),t=R(s[2]),this.h()},l(n){e=h(n,"DIV",{class:!0});var u=_(e);t=W(u,s[2]),u.forEach(d),this.h()},h(){c(e,"class","text-sm text-gray-500 shrink-0")},m(n,u){te(n,e,u),r(e,t)},p(n,u){u[0]&4&&J(t,n[2])},i:Ye,o:Ye,d(n){n&&d(e)}}}function qt(s){let e,t,n,u;return{c(){e=m("input"),this.h()},l(a){e=h(a,"INPUT",{class:!0,type:!0,placeholder:!0}),this.h()},h(){c(e,"class","w-full text-sm disabled:text-gray-500 bg-transparent outline-hidden"),c(e,"type","text"),c(e,"placeholder",t=s[12].t("Tool ID")),e.required=!0,e.disabled=s[5]},m(a,i){te(a,e,i),ve(e,s[2]),n||(u=ge(e,"input",s[23]),n=!0)},p(a,i){i[0]&4096&&t!==(t=a[12].t("Tool ID"))&&c(e,"placeholder",t),i[0]&32&&(e.disabled=a[5]),i[0]&4&&e.value!==a[2]&&ve(e,a[2])},d(a){a&&d(e),n=!1,u()}}}function At(s){let e,t,n,u;return{c(){e=m("input"),this.h()},l(a){e=h(a,"INPUT",{class:!0,type:!0,placeholder:!0}),this.h()},h(){c(e,"class","w-full text-sm bg-transparent outline-hidden"),c(e,"type","text"),c(e,"placeholder",t=s[12].t("Tool Description")),e.required=!0},m(a,i){te(a,e,i),ve(e,s[3].description),n||(u=ge(e,"input",s[24]),n=!0)},p(a,i){i[0]&4096&&t!==(t=a[12].t("Tool Description"))&&c(e,"placeholder",t),i[0]&8&&e.value!==a[3].description&&ve(e,a[3].description)},d(a){a&&d(e),n=!1,u()}}}function Nt(s){let e,t,n,u=s[12].t("Please carefully review the following warnings:")+"",a,i,p,v,b=s[12].t("Tools have a function calling system that allows arbitrary code execution.")+"",y,N,w,E=s[12].t("Do not install tools from sources you do not fully trust.")+"",T,k,V,I=s[12].t("I acknowledge that I have read and I understand the implications of my action. I am aware of the risks associated with executing arbitrary code and I have verified the trustworthiness of the source.")+"",C;return{c(){e=m("div"),t=m("div"),n=m("div"),a=R(u),i=q(),p=m("ul"),v=m("li"),y=R(b),N=q(),w=m("li"),T=R(E),k=q(),V=m("div"),C=R(I),this.h()},l(g){e=h(g,"DIV",{class:!0});var D=_(e);t=h(D,"DIV",{class:!0});var M=_(t);n=h(M,"DIV",{});var $=_(n);a=W($,u),$.forEach(d),i=A(M),p=h(M,"UL",{class:!0});var j=_(p);v=h(j,"LI",{});var se=_(v);y=W(se,b),se.forEach(d),N=A(j),w=h(j,"LI",{});var S=_(w);T=W(S,E),S.forEach(d),j.forEach(d),M.forEach(d),k=A(D),V=h(D,"DIV",{class:!0});var P=_(V);C=W(P,I),P.forEach(d),D.forEach(d),this.h()},h(){c(p,"class","mt-1 list-disc pl-4 text-xs"),c(t,"class","bg-yellow-500/20 text-yellow-700 dark:text-yellow-200 rounded-lg px-4 py-3"),c(V,"class","my-3"),c(e,"class","text-sm text-gray-500")},m(g,D){te(g,e,D),r(e,t),r(t,n),r(n,a),r(t,i),r(t,p),r(p,v),r(v,y),r(p,N),r(p,w),r(w,T),r(e,k),r(e,V),r(V,C)},p(g,D){D[0]&4096&&u!==(u=g[12].t("Please carefully review the following warnings:")+"")&&J(a,u),D[0]&4096&&b!==(b=g[12].t("Tools have a function calling system that allows arbitrary code execution.")+"")&&J(y,b),D[0]&4096&&E!==(E=g[12].t("Do not install tools from sources you do not fully trust.")+"")&&J(T,E),D[0]&4096&&I!==(I=g[12].t("I acknowledge that I have read and I understand the implications of my action. I am aware of the risks associated with executing arbitrary code and I have verified the trustworthiness of the source.")+"")&&J(C,I)},d(g){g&&d(e)}}}function St(s){var Xe,Ze,xe,et;let e,t,n,u,a,i,p,v,b,y,N,w,E,T,k,V,I,C,g,D,M,$=s[12].t("Access")+"",j,se,S,P,U,me,F,we,oe,H,be,G,ae,B,l,ye=s[12].t("Warning:")+"",Pe,Be,ke=s[12].t("Tools are a function calling system with arbitrary code execution")+"",Ve,Me,$e,je,he,Ee=s[12].t("don't install random tools from sources you don't trust.")+"",qe,He,ie,Ie=s[12].t("Save")+"",Ae,Ne,Y,Le,Q,Oe,ze;function lt(o){s[18](o)}function it(o){s[19](o)}let Re={accessRoles:["read","write"],allowPublic:((xe=(Ze=(Xe=s[11])==null?void 0:Xe.permissions)==null?void 0:Ze.sharing)==null?void 0:xe.public_tools)||((et=s[11])==null?void 0:et.role)==="admin"};s[8]!==void 0&&(Re.show=s[8]),s[4]!==void 0&&(Re.accessControl=s[4]),e=new Et({props:Re}),De.push(()=>Ge(e,"show",lt)),De.push(()=>Ge(e,"accessControl",it)),w=new Ue({props:{content:s[12].t("Back"),$$slots:{default:[Ct]},$$scope:{ctx:s}}}),k=new Ue({props:{content:s[12].t("e.g. My Tools"),placement:"top-start",$$slots:{default:[Dt]},$$scope:{ctx:s}}}),g=new It({props:{strokeWidth:"2.5",className:"size-3.5"}});const Ke=[Vt,Pt],ne=[];function Je(o,f){return o[5]?0:1}P=Je(s),U=ne[P]=Ke[P](s),F=new Ue({props:{className:"w-full self-center items-center flex",content:s[12].t("e.g. Tools for performing various operations"),placement:"top-start",$$slots:{default:[At]},$$scope:{ctx:s}}});let ut={value:s[1],lang:"python",boilerplate:s[14],onChange:s[25],onSave:s[26]};H=new wt({props:ut}),s[27](H);function ct(o){s[30](o)}let Qe={$$slots:{default:[Nt]},$$scope:{ctx:s}};return s[7]!==void 0&&(Qe.show=s[7]),Y=new yt({props:Qe}),De.push(()=>Ge(Y,"show",ct)),Y.$on("confirm",s[31]),{c(){X(e.$$.fragment),u=q(),a=m("div"),i=m("div"),p=m("form"),v=m("div"),b=m("div"),y=m("div"),N=m("div"),X(w.$$.fragment),E=q(),T=m("div"),X(k.$$.fragment),V=q(),I=m("div"),C=m("button"),X(g.$$.fragment),D=q(),M=m("div"),j=R($),se=q(),S=m("div"),U.c(),me=q(),X(F.$$.fragment),we=q(),oe=m("div"),X(H.$$.fragment),be=q(),G=m("div"),ae=m("div"),B=m("div"),l=m("span"),Pe=R(ye),Be=q(),Ve=R(ke),Me=q(),$e=m("br"),je=R(`—
							`),he=m("span"),qe=R(Ee),He=q(),ie=m("button"),Ae=R(Ie),Ne=q(),X(Y.$$.fragment),this.h()},l(o){Z(e.$$.fragment,o),u=A(o),a=h(o,"DIV",{class:!0});var f=_(a);i=h(f,"DIV",{class:!0});var ue=_(i);p=h(ue,"FORM",{class:!0});var _e=_(p);v=h(_e,"DIV",{class:!0});var z=_(v);b=h(z,"DIV",{class:!0});var re=_(b);y=h(re,"DIV",{class:!0});var K=_(y);N=h(K,"DIV",{class:!0});var ce=_(N);Z(w.$$.fragment,ce),ce.forEach(d),E=A(K),T=h(K,"DIV",{class:!0});var pe=_(T);Z(k.$$.fragment,pe),pe.forEach(d),V=A(K),I=h(K,"DIV",{class:!0});var Te=_(I);C=h(Te,"BUTTON",{class:!0,type:!0});var fe=_(C);Z(g.$$.fragment,fe),D=A(fe),M=h(fe,"DIV",{class:!0});var Ce=_(M);j=W(Ce,$),Ce.forEach(d),fe.forEach(d),Te.forEach(d),K.forEach(d),se=A(re),S=h(re,"DIV",{class:!0});var de=_(S);U.l(de),me=A(de),Z(F.$$.fragment,de),de.forEach(d),re.forEach(d),we=A(z),oe=h(z,"DIV",{class:!0});var tt=_(oe);Z(H.$$.fragment,tt),tt.forEach(d),be=A(z),G=h(z,"DIV",{class:!0});var Se=_(G);ae=h(Se,"DIV",{class:!0});var st=_(ae);B=h(st,"DIV",{class:!0});var le=_(B);l=h(le,"SPAN",{class:!0});var ot=_(l);Pe=W(ot,ye),ot.forEach(d),Be=A(le),Ve=W(le,ke),Me=A(le),$e=h(le,"BR",{}),je=W(le,`—
							`),he=h(le,"SPAN",{class:!0});var at=_(he);qe=W(at,Ee),at.forEach(d),le.forEach(d),st.forEach(d),He=A(Se),ie=h(Se,"BUTTON",{class:!0,type:!0});var nt=_(ie);Ae=W(nt,Ie),nt.forEach(d),Se.forEach(d),z.forEach(d),_e.forEach(d),ue.forEach(d),f.forEach(d),Ne=A(o),Z(Y.$$.fragment,o),this.h()},h(){c(N,"class","shrink-0 mr-2"),c(T,"class","flex-1"),c(M,"class","text-sm font-medium shrink-0"),c(C,"class","bg-gray-50 hover:bg-gray-100 text-black dark:bg-gray-850 dark:hover:bg-gray-800 dark:text-white transition px-2 py-1 rounded-full flex gap-1 items-center"),c(C,"type","button"),c(I,"class","self-center shrink-0"),c(y,"class","flex w-full items-center"),c(S,"class","flex gap-2 px-1 items-center"),c(b,"class","w-full mb-2 flex flex-col gap-0.5"),c(oe,"class","mb-2 flex-1 overflow-auto h-0 rounded-lg"),c(l,"class","font-semibold dark:text-gray-200"),c(he,"class","font-medium dark:text-gray-400"),c(B,"class","text-xs text-gray-500 line-clamp-2"),c(ae,"class","flex-1 pr-3"),c(ie,"class","px-3.5 py-1.5 text-sm font-medium bg-black hover:bg-gray-900 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-full"),c(ie,"type","submit"),c(G,"class","pb-3 flex justify-between"),c(v,"class","flex flex-col flex-1 overflow-auto h-0 rounded-lg"),c(p,"class","flex flex-col max-h-[100dvh] h-full"),c(i,"class","mx-auto w-full md:px-0 h-full"),c(a,"class","flex flex-col justify-between w-full overflow-y-auto h-full")},m(o,f){x(e,o,f),te(o,u,f),te(o,a,f),r(a,i),r(i,p),r(p,v),r(v,b),r(b,y),r(y,N),x(w,N,null),r(y,E),r(y,T),x(k,T,null),r(y,V),r(y,I),r(I,C),x(g,C,null),r(C,D),r(C,M),r(M,j),r(b,se),r(b,S),ne[P].m(S,null),r(S,me),x(F,S,null),r(v,we),r(v,oe),x(H,oe,null),r(v,be),r(v,G),r(G,ae),r(ae,B),r(B,l),r(l,Pe),r(B,Be),r(B,Ve),r(B,Me),r(B,$e),r(B,je),r(B,he),r(he,qe),r(G,He),r(G,ie),r(ie,Ae),s[28](p),te(o,Ne,f),x(Y,o,f),Q=!0,Oe||(ze=[ge(C,"click",s[22]),ge(p,"submit",dt(s[29]))],Oe=!0)},p(o,f){var Te,fe,Ce,de;const ue={};f[0]&2048&&(ue.allowPublic=((Ce=(fe=(Te=o[11])==null?void 0:Te.permissions)==null?void 0:fe.sharing)==null?void 0:Ce.public_tools)||((de=o[11])==null?void 0:de.role)==="admin"),!t&&f[0]&256&&(t=!0,ue.show=o[8],We(()=>t=!1)),!n&&f[0]&16&&(n=!0,ue.accessControl=o[4],We(()=>n=!1)),e.$set(ue);const _e={};f[0]&4096&&(_e.content=o[12].t("Back")),f[1]&16&&(_e.$$scope={dirty:f,ctx:o}),w.$set(_e);const z={};f[0]&4096&&(z.content=o[12].t("e.g. My Tools")),f[0]&4097|f[1]&16&&(z.$$scope={dirty:f,ctx:o}),k.$set(z),(!Q||f[0]&4096)&&$!==($=o[12].t("Access")+"")&&J(j,$);let re=P;P=Je(o),P===re?ne[P].p(o,f):(gt(),L(ne[re],1,1,()=>{ne[re]=null}),vt(),U=ne[P],U?U.p(o,f):(U=ne[P]=Ke[P](o),U.c()),O(U,1),U.m(S,me));const K={};f[0]&4096&&(K.content=o[12].t("e.g. Tools for performing various operations")),f[0]&4104|f[1]&16&&(K.$$scope={dirty:f,ctx:o}),F.$set(K);const ce={};f[0]&2&&(ce.value=o[1]),f[0]&512&&(ce.onChange=o[25]),f[0]&64&&(ce.onSave=o[26]),H.$set(ce),(!Q||f[0]&4096)&&ye!==(ye=o[12].t("Warning:")+"")&&J(Pe,ye),(!Q||f[0]&4096)&&ke!==(ke=o[12].t("Tools are a function calling system with arbitrary code execution")+"")&&J(Ve,ke),(!Q||f[0]&4096)&&Ee!==(Ee=o[12].t("don't install random tools from sources you don't trust.")+"")&&J(qe,Ee),(!Q||f[0]&4096)&&Ie!==(Ie=o[12].t("Save")+"")&&J(Ae,Ie);const pe={};f[0]&4096|f[1]&16&&(pe.$$scope={dirty:f,ctx:o}),!Le&&f[0]&128&&(Le=!0,pe.show=o[7],We(()=>Le=!1)),Y.$set(pe)},i(o){Q||(O(e.$$.fragment,o),O(w.$$.fragment,o),O(k.$$.fragment,o),O(g.$$.fragment,o),O(U),O(F.$$.fragment,o),O(H.$$.fragment,o),O(Y.$$.fragment,o),Q=!0)},o(o){L(e.$$.fragment,o),L(w.$$.fragment,o),L(k.$$.fragment,o),L(g.$$.fragment,o),L(U),L(F.$$.fragment,o),L(H.$$.fragment,o),L(Y.$$.fragment,o),Q=!1},d(o){o&&(d(u),d(a),d(Ne)),ee(e,o),ee(w),ee(k),ee(g),ne[P].d(),ee(F),s[27](null),ee(H),s[28](null),ee(Y,o),Oe=!1,mt(ze)}}}function Ut(s,e,t){let n,u;rt(s,Tt,l=>t(11,n=l));const a=ht("i18n");rt(s,a,l=>t(12,u=l));let i=null,p=!1,v=!1,{edit:b=!1}=e,{clone:y=!1}=e,{onSave:N=()=>{}}=e,{id:w=""}=e,{name:E=""}=e,{meta:T={description:""}}=e,{content:k=""}=e,{accessControl:V=null}=e,I="";const C=()=>{t(9,I=k)};let g,D=`import os
import requests
from datetime import datetime


class Tools:
    def __init__(self):
        pass

    # Add your custom tools using pure Python code here, make sure to add type hints
    # Use Sphinx-style docstrings to document your tools, they will be used for generating tools specifications
    # Please refer to function_calling_filter_pipeline.py file from pipelines project for an example

    def get_user_name_and_email_and_id(self, __user__: dict = {}) -> str:
        """
        Get the user name, Email and ID from the user object.
        """

        # Do not include :param for __user__ in the docstring as it should not be shown in the tool's specification
        # The session user object will be passed as a parameter when the function is called

        print(__user__)
        result = ""

        if "name" in __user__:
            result += f"User: {__user__['name']}"
        if "id" in __user__:
            result += f" (ID: {__user__['id']})"
        if "email" in __user__:
            result += f" (Email: {__user__['email']})"

        if result == "":
            result = "User: Unknown"

        return result

    def get_current_time(self) -> str:
        """
        Get the current time in a more human-readable format.
        :return: The current time.
        """

        now = datetime.now()
        current_time = now.strftime("%I:%M:%S %p")  # Using 12-hour format with AM/PM
        current_date = now.strftime(
            "%A, %B %d, %Y"
        )  # Full weekday, month name, day, and year

        return f"Current Date and Time = {current_date}, {current_time}"

    def calculator(self, equation: str) -> str:
        """
        Calculate the result of an equation.
        :param equation: The equation to calculate.
        """

        # Avoid using eval in production code
        # https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
        try:
            result = eval(equation)
            return f"{equation} = {result}"
        except Exception as e:
            print(e)
            return "Invalid equation"

    def get_current_weather(self, city: str) -> str:
        """
        Get the current weather for a given city.
        :param city: The name of the city to get the weather for.
        :return: The current weather information or an error message.
        """
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return (
                "API key is not set in the environment variable 'OPENWEATHER_API_KEY'."
            )

        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",  # Optional: Use 'imperial' for Fahrenheit
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            data = response.json()

            if data.get("cod") != 200:
                return f"Error fetching weather data: {data.get('message')}"

            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            return f"Weather in {city}: {temperature}°C"
        except requests.RequestException as e:
            return f"Error fetching weather data: {str(e)}"
`;const M=async()=>{N({id:w,name:E,meta:T,content:k,access_control:V})},$=async()=>{if(g){t(1,k=I),await Fe();const l=await g.formatPythonCodeHandler();await Fe(),t(1,k=I),await Fe(),l&&(console.log("Code formatted successfully"),M())}};function j(l){v=l,t(8,v)}function se(l){V=l,t(4,V)}const S=()=>{bt("/workspace/tools")};function P(){E=this.value,t(0,E)}const U=()=>{t(8,v=!0)};function me(){w=this.value,t(2,w),t(0,E),t(5,b),t(16,y)}function F(){T.description=this.value,t(3,T)}const we=l=>{t(9,I=l)},oe=async()=>{i&&i.requestSubmit()};function H(l){De[l?"unshift":"push"](()=>{g=l,t(10,g)})}function be(l){De[l?"unshift":"push"](()=>{i=l,t(6,i)})}const G=()=>{b?$():t(7,p=!0)};function ae(l){p=l,t(7,p)}const B=()=>{$()};return s.$$set=l=>{"edit"in l&&t(5,b=l.edit),"clone"in l&&t(16,y=l.clone),"onSave"in l&&t(17,N=l.onSave),"id"in l&&t(2,w=l.id),"name"in l&&t(0,E=l.name),"meta"in l&&t(3,T=l.meta),"content"in l&&t(1,k=l.content),"accessControl"in l&&t(4,V=l.accessControl)},s.$$.update=()=>{s.$$.dirty[0]&2&&k&&C(),s.$$.dirty[0]&65569&&E&&!b&&!y&&t(2,w=E.replace(/\s+/g,"_").toLowerCase())},[E,k,w,T,V,b,i,p,v,I,g,n,u,a,D,$,y,N,j,se,S,P,U,me,F,we,oe,H,be,G,ae,B]}class Ft extends _t{constructor(e){super(),pt(this,e,Ut,St,ft,{edit:5,clone:16,onSave:17,id:2,name:0,meta:3,content:1,accessControl:4},null,[-1,-1])}}export{Ft as T};
//# sourceMappingURL=CgCWMnmx.js.map
