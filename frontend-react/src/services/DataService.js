import { BASE_API_URL } from "./Common";

const axios = require('axios');

const DataService = {
    Init: function () {
        // Any application initialization logic comes here
    },
    GetLeaderboard: async function () {
        return await axios.get(BASE_API_URL + "/leaderboard");
    },
    GetCurrentmodel: async function () {
        return await axios.get(BASE_API_URL + "/best_model");
    },

    GetLatentMatch: async function (formData) {
        return await axios.post(BASE_API_URL + "/match_latent", formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    },
}

export default DataService;