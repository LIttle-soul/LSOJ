import { createStore } from 'vuex';
import userSettings from './modules/userSettings';
import admin from './modules/admin';


export default createStore({
  modules: {
    userSettings: userSettings,
    admin: admin
  }
})
