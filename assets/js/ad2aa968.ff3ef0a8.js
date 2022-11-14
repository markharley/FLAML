"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[7026],{3905:(e,t,a)=>{a.d(t,{Zo:()=>u,kt:()=>d});var n=a(7294);function r(e,t,a){return t in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}function i(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),a.push.apply(a,n)}return a}function o(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?i(Object(a),!0).forEach((function(t){r(e,t,a[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):i(Object(a)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))}))}return e}function s(e,t){if(null==e)return{};var a,n,r=function(e,t){if(null==e)return{};var a,n,r={},i=Object.keys(e);for(n=0;n<i.length;n++)a=i[n],t.indexOf(a)>=0||(r[a]=e[a]);return r}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(n=0;n<i.length;n++)a=i[n],t.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(r[a]=e[a])}return r}var l=n.createContext({}),c=function(e){var t=n.useContext(l),a=t;return e&&(a="function"==typeof e?e(t):o(o({},t),e)),a},u=function(e){var t=c(e.components);return n.createElement(l.Provider,{value:t},e.children)},m={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},p=n.forwardRef((function(e,t){var a=e.components,r=e.mdxType,i=e.originalType,l=e.parentName,u=s(e,["components","mdxType","originalType","parentName"]),p=c(a),d=r,f=p["".concat(l,".").concat(d)]||p[d]||m[d]||i;return a?n.createElement(f,o(o({ref:t},u),{},{components:a})):n.createElement(f,o({ref:t},u))}));function d(e,t){var a=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var i=a.length,o=new Array(i);o[0]=p;var s={};for(var l in t)hasOwnProperty.call(t,l)&&(s[l]=t[l]);s.originalType=e,s.mdxType="string"==typeof e?e:r,o[1]=s;for(var c=2;c<i;c++)o[c]=a[c];return n.createElement.apply(null,o)}return n.createElement.apply(null,a)}p.displayName="MDXCreateElement"},8957:(e,t,a)=>{a.r(t),a.d(t,{contentTitle:()=>o,default:()=>u,frontMatter:()=>i,metadata:()=>s,toc:()=>l});var n=a(7462),r=(a(7294),a(3905));const i={},o="Getting Started",s={unversionedId:"Getting-Started",id:"Getting-Started",isDocsHomePage:!1,title:"Getting Started",description:"FLAML is a lightweight Python library that finds accurate machine",source:"@site/docs/Getting-Started.md",sourceDirName:".",slug:"/Getting-Started",permalink:"/FLAML/docs/Getting-Started",editUrl:"https://github.com/microsoft/FLAML/edit/main/website/docs/Getting-Started.md",tags:[],version:"current",frontMatter:{},sidebar:"docsSidebar",next:{title:"Installation",permalink:"/FLAML/docs/Installation"}},l=[{value:"Main Features",id:"main-features",children:[],level:3},{value:"Quickstart",id:"quickstart",children:[{value:"Task-oriented AutoML",id:"task-oriented-automl",children:[],level:4},{value:"Tune user-defined function",id:"tune-user-defined-function",children:[],level:4},{value:"Zero-shot AutoML",id:"zero-shot-automl",children:[],level:4}],level:3},{value:"Where to Go Next?",id:"where-to-go-next",children:[],level:3}],c={toc:l};function u(e){let{components:t,...a}=e;return(0,r.kt)("wrapper",(0,n.Z)({},c,a,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("h1",{id:"getting-started"},"Getting Started"),(0,r.kt)("p",null,"FLAML is a lightweight Python library that finds accurate machine\nlearning models automatically, efficiently and economically. It frees users from selecting learners and hyperparameters for each learner."),(0,r.kt)("h3",{id:"main-features"},"Main Features"),(0,r.kt)("ol",null,(0,r.kt)("li",{parentName:"ol"},(0,r.kt)("p",{parentName:"li"},"For common machine learning tasks like classification and regression, it quickly finds quality models for user-provided data with low computational resources. It supports both classical machine learning models and deep neural networks.")),(0,r.kt)("li",{parentName:"ol"},(0,r.kt)("p",{parentName:"li"},"It is easy to customize or extend. Users can find their desired customizability from a smooth range: minimal customization (computational resource budget), medium customization (e.g., scikit-style learner, search space and metric), or full customization (arbitrary training and evaluation code). Users can customize only when and what they need to, and leave the rest to the library.")),(0,r.kt)("li",{parentName:"ol"},(0,r.kt)("p",{parentName:"li"},"It supports fast and economical automatic tuning, capable of handling large search space with heterogeneous evaluation cost and complex constraints/guidance/early stopping. FLAML is powered by a new, ",(0,r.kt)("a",{parentName:"p",href:"Use-Cases/Tune-User-Defined-Function#hyperparameter-optimization-algorithm"},"cost-effective\nhyperparameter optimization"),"\nand learner selection method invented by Microsoft Research."))),(0,r.kt)("h3",{id:"quickstart"},"Quickstart"),(0,r.kt)("p",null,"Install FLAML from pip: ",(0,r.kt)("inlineCode",{parentName:"p"},"pip install flaml"),". Find more options in ",(0,r.kt)("a",{parentName:"p",href:"Installation"},"Installation"),"."),(0,r.kt)("p",null,"There are several ways of using flaml:"),(0,r.kt)("h4",{id:"task-oriented-automl"},(0,r.kt)("a",{parentName:"h4",href:"Use-Cases/task-oriented-automl"},"Task-oriented AutoML")),(0,r.kt)("p",null,"For example, with three lines of code, you can start using this economical and fast AutoML engine as a scikit-learn style estimator."),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'from flaml import AutoML\nautoml = AutoML()\nautoml.fit(X_train, y_train, task="classification", time_budget=60)\n')),(0,r.kt)("p",null,"It automatically tunes the hyperparameters and selects the best model from default learners such as LightGBM, XGBoost, random forest etc. for the specified time budget 60 seconds. ",(0,r.kt)("a",{parentName:"p",href:"Use-Cases/task-oriented-automl#customize-automlfit"},"Customizing")," the optimization metrics, learners and search spaces etc. is very easy. For example,"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'automl.add_learner("mylgbm", MyLGBMEstimator)\nautoml.fit(X_train, y_train, task="classification", metric=custom_metric, estimator_list=["mylgbm"], time_budget=60)\n')),(0,r.kt)("h4",{id:"tune-user-defined-function"},(0,r.kt)("a",{parentName:"h4",href:"Use-Cases/Tune-User-Defined-Function"},"Tune user-defined function")),(0,r.kt)("p",null,"You can run generic hyperparameter tuning for a custom function (machine learning or beyond). For example,"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'from flaml import tune\nfrom flaml.model import LGBMEstimator\n\ndef train_lgbm(config: dict) -> dict:\n    # convert config dict to lgbm params\n    params = LGBMEstimator(**config).params\n    # train the model\n    train_set = lightgbm.Dataset(csv_file_name)\n    model = lightgbm.train(params, train_set)\n    # evaluate the model\n    pred = model.predict(X_test)\n    mse = mean_squared_error(y_test, pred)\n    # return eval results as a dictionary\n    return {"mse": mse}\n\n# load a built-in search space from flaml\nflaml_lgbm_search_space = LGBMEstimator.search_space(X_train.shape)\n# specify the search space as a dict from hp name to domain; you can define your own search space same way\nconfig_search_space = {hp: space["domain"] for hp, space in flaml_lgbm_search_space.items()}\n# give guidance about hp values corresponding to low training cost, i.e., {"n_estimators": 4, "num_leaves": 4}\nlow_cost_partial_config = {\n    hp: space["low_cost_init_value"]\n    for hp, space in flaml_lgbm_search_space.items()\n    if "low_cost_init_value" in space\n}\n# run the tuning, minimizing mse, with total time budget 3 seconds\nanalysis = tune.run(\n    train_lgbm, metric="mse", mode="min", config=config_search_space,\n    low_cost_partial_config=low_cost_partial_config, time_budget_s=3, num_samples=-1,\n)\n')),(0,r.kt)("p",null,"Please see this ",(0,r.kt)("a",{parentName:"p",href:"https://github.com/microsoft/FLAML/blob/main/test/tune_example.py"},"script")," for the complete version of the above example."),(0,r.kt)("h4",{id:"zero-shot-automl"},(0,r.kt)("a",{parentName:"h4",href:"Use-Cases/Zero-Shot-AutoML"},"Zero-shot AutoML")),(0,r.kt)("p",null,"FLAML offers a unique, seamless and effortless way to leverage AutoML for the commonly used classifiers and regressors such as LightGBM and XGBoost. For example, if you are using ",(0,r.kt)("inlineCode",{parentName:"p"},"lightgbm.LGBMClassifier")," as your current learner, all you need to do is to replace ",(0,r.kt)("inlineCode",{parentName:"p"},"from lightgbm import LGBMClassifier")," by:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"from flaml.default import LGBMClassifier\n")),(0,r.kt)("p",null,"Then, you can use it just like you use the original ",(0,r.kt)("inlineCode",{parentName:"p"},"LGMBClassifier"),". Your other code can remain unchanged. When you call the ",(0,r.kt)("inlineCode",{parentName:"p"},"fit()")," function from ",(0,r.kt)("inlineCode",{parentName:"p"},"flaml.default.LGBMClassifier"),", it will automatically instantiate a good data-dependent hyperparameter configuration for your dataset, which is expected to work better than the default configuration."),(0,r.kt)("h3",{id:"where-to-go-next"},"Where to Go Next?"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"Understand the use cases for ",(0,r.kt)("a",{parentName:"li",href:"Use-Cases/task-oriented-automl"},"Task-oriented AutoML"),", ",(0,r.kt)("a",{parentName:"li",href:"Use-Cases/Tune-User-Defined-Function"},"Tune user-defined function")," and ",(0,r.kt)("a",{parentName:"li",href:"Use-Cases/Zero-Shot-AutoML"},"Zero-shot AutoML"),"."),(0,r.kt)("li",{parentName:"ul"},'Find code examples under "Examples": from ',(0,r.kt)("a",{parentName:"li",href:"Examples/AutoML-Classification"},"AutoML - Classification")," to ",(0,r.kt)("a",{parentName:"li",href:"Examples/Tune-PyTorch"},"Tune - PyTorch"),"."),(0,r.kt)("li",{parentName:"ul"},"Find ",(0,r.kt)("a",{parentName:"li",href:"https://www.youtube.com/channel/UCfU0zfFXHXdAd5x-WvFBk5A"},"talks")," and ",(0,r.kt)("a",{parentName:"li",href:"https://github.com/microsoft/FLAML/tree/tutorial/tutorial"},"tutorials")," about FLAML."),(0,r.kt)("li",{parentName:"ul"},"Learn about ",(0,r.kt)("a",{parentName:"li",href:"Research"},"research")," around FLAML."),(0,r.kt)("li",{parentName:"ul"},"Refer to ",(0,r.kt)("a",{parentName:"li",href:"reference/automl"},"SDK")," and ",(0,r.kt)("a",{parentName:"li",href:"FAQ"},"FAQ"),".")),(0,r.kt)("p",null,"If you like our project, please give it a ",(0,r.kt)("a",{parentName:"p",href:"https://github.com/microsoft/FLAML/stargazers"},"star")," on GitHub. If you are interested in contributing, please read ",(0,r.kt)("a",{parentName:"p",href:"Contribute"},"Contributor's Guide"),"."),(0,r.kt)("iframe",{src:"https://ghbtns.com/github-btn.html?user=microsoft&repo=FLAML&type=star&count=true&size=large",frameborder:"0",scrolling:"0",width:"170",height:"30",title:"GitHub"}))}u.isMDXComponent=!0}}]);