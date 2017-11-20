import angular from 'angular'
import ngRoute from 'angular-route'
import ngCookies from 'angular-cookies'

// bootstrap dependencies
import 'jquery'
import 'bootstrap/dist/js/bootstrap'

import './styles.css'

import HomeController from './controllers/home.controller'
import AnswerService from './answer.service'

angular.module('SmartBotnet', [ngRoute, ngCookies]). //
controller('HomeCtrl', HomeController). //
service('AnswerService', AnswerService). //
config(function($routeProvider) {
    $routeProvider. //
    when('/', {
        templateUrl: 'views/home.html',
        controller: 'HomeCtrl',
        controllerAs: '$ctrl'
    }). //
    otherwise({redirectTo: '/'})
});
