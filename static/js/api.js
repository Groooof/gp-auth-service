

class Api {
    constructor() {
        this.api_prefix = '/api/v1'
        this.base_headers = {'Content-Type': 'application/json;charset=utf-8'};
    };
    // запрос на регистрацию пользователя сервиса
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
    // запрос на аутентификацию пользователя сервиса
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
    // запрос на выход из системы пользователя сервиса
    async logout() {
        const options = {
            method: 'POST',
            headers: this.base_headers
        };
        const response = await fetch(this.api_prefix + '/logout', options);
        return response;
    };
    // запрос на создание приложения
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
    // запрос на удаление приложения
    async delApp(appId) {
        const options = {
            method: 'DELETE',
            headers: this.base_headers
        };
        const response = await fetch(this.api_prefix + `/admin/apps/${appId}`, options);
        return response;
    };
    // запрос на создание пользователя приложения
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
    // запрос на удаление пользователя приложения
    async delAppUser(appId, username) {
        const queryParams = new URLSearchParams({ username: username }).toString()
        const options = {
            method: 'DELETE',
            headers: this.base_headers
        };
        const response = await fetch(this.api_prefix + `/admin/apps/${appId}/users?` + queryParams, options);
        return response;
    };
    // запрос на аутентификацию пользователя приложения
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
            headers: this.base_headers,
            credentials: 'include'
        };
        const response = await fetch(this.api_prefix + url, options);
        return response;
    };
}


