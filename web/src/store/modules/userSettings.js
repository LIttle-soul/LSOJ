import userSettings from '@/config/userSettings'
import { getItem, setItem } from '@/utils/storage'

export default {
    namespaced: true,
    state: getItem('userSettings') || userSettings,
    mutations: {
        SAVE_SETTINGS(state, data) {
            Object.entries(data).forEach(([key, value]) => {
                state[key] = value
            })
            setItem('userSettings', data)
        },
    },
}