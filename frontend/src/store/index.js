import Vue from "vue";
import vuex from "vuex";

Vue.use(vuex);

import app from "./modules/app";
import user from "./modules/user";
import menu from "./modules/menu";
import iframe from "./modules/iframe";
import tab from "./modules/tab";
import sprintCaseSuite from "./modules/sprintCaseSuite";
import sprintCaseTable from "./modules/sprintCaseTable";
import apiProjectGroup from "./modules/apiProjectGroup";
import apiProjectTable from "./modules/apiProjectTable";
import apiGroup from "./modules/apiGroup";

const store = new vuex.Store({
  modules: {
    app: app,
    user: user,
    menu: menu,
    iframe: iframe,
    tab: tab,
    sprintCaseSuite: sprintCaseSuite,
    sprintCaseTable: sprintCaseTable,
    apiProjectGroup: apiProjectGroup,
    apiProjectTable: apiProjectTable,
    apiGroup: apiGroup
  }
});

export default store;
