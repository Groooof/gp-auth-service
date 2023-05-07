

class Api {
    constructor() {
        this.api_prefix = '/api/v1'
        this.base_headers = {'Content-Type': 'application/json;charset=utf-8'};
    };

    async register(username, password) {
        const body = {
            'username': username,
            'password': password
        };
        const options = {
            method: 'POST',
            body: JSON.stringify(body),
            headers: this.base_headers
        };
        const response = await fetch(this.api_prefix + '/register', options);
        return response;
    };

    async login(username, password) {
        const body = {
            'username': username,
            'password': password
        };
        const options = {
            method: 'POST',
            body: JSON.stringify(body),
            headers: this.base_headers
        };
        const response = await fetch(this.api_prefix + '/login', options);
        return response;
    };

    async logout() {
        const options = {
            method: 'POST',
            headers: this.base_headers
        };
        const response = await fetch(this.api_prefix + '/logout', options);
        return response;
    };

    async addApp(name, host) {
        const body = {
            'name': name,
            'host': host
        };
        const options = {
            method: 'POST',
            body: JSON.stringify(body),
            headers: this.base_headers
        };
        const response = await fetch(this.api_prefix + '/admin/apps', options);
        return response;
    };

    async delApp(appId) {
        const options = {
            method: 'DELETE',
            headers: this.base_headers
        };
        const response = await fetch(this.api_prefix + `/admin/apps/${appId}`, options);
        return response;
    };

    async createAppUser(appId, username, password) {
        const body = {
            'username': username,
            'password': password
        };
        const options = {
            method: 'POST',
            body: JSON.stringify(body),
            headers: this.base_headers
        };
        const response = await fetch(this.api_prefix + `/admin/apps/${appId}/users`, options);
        return response;
    };

    async delAppUser(appId, username) {
        const queryParams = new URLSearchParams({ username: username }).toString()
        const options = {
            method: 'DELETE',
            headers: this.base_headers
        };
        const response = await fetch(this.api_prefix + `/admin/apps/${appId}/users?` + queryParams, options);
        return response;
    };


    async authenticate(username,
                       step2Selection,
                       step3Selection,
                       step1GridArray,
                       step2GridArray,
                       step3GridArray,
                       url) {
        
        const body = {
            'username': username,
            'step_2_selection': step2Selection,
            'step_3_selection': step3Selection,
            'step_1_images': step1GridArray,
            'step_2_images': step2GridArray,
            'step_3_images': step3GridArray
        };
        const options = {
            method: 'POST',
            body: JSON.stringify(body),
            headers: this.base_headers
        };
        const response = await fetch(this.api_prefix + url, options);
        return response;
    };

}


