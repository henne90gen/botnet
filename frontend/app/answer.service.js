export default function AnswerService() {

    this.BASE_URL = "http://localhost:8080";

    this.defaultHeader = function () {
        return {
            Accept: 'application/json', 'Content-Type': 'application/json;charset=UTF-8',
            Origin: 'localhost'
        };
    };

    this.getRequest = function (resource) {
        return fetch(`${this.BASE_URL}${resource}`, {
            method: 'GET',
            headers: this.defaultHeader()
        }).then(result => result);
    };

    this.postRequest = function (resource, data) {
        let body;

        try {
            body = JSON.stringify(data);
        } catch (e) {
            // Ignore
        }

        return fetch(`${this.BASE_URL}${resource}`, {
            method: 'POST',
            headers: this.defaultHeader(),
            body
        }).then(result => result);
    };

    this.ask = function (question) {
        return this.getRequest('/question?q=' + question) //
            .then(response => response.json());
    };
}
