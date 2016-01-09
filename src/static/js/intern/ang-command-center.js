/**
 * Created by Savion on 11/26/2015.
 */
(function() {
    var banana = angular.module('internApp', []);
    banana.config(['$interpolateProvider', function($interpolateProvider){
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}');
    }]);

    banana.controller('tabController', function(){
        this.current = 1;

        this.isCurrent = function (tabNum) {
            return this.current === tabNum;
        };

        this.setTab = function (newTab) {
            this.current = newTab;
        };

        this.banana = 6;


    });

    banana.controller('orgController', ['$scope', '$http', function($scope, $http){
        $scope.pageData = this;

        $scope.pageData.organizations =[];

        $http.get('/api/command-center').success(function(data){
            $scope.pageData.organizations = data['organizations'];
        });

    }]);

    banana.controller('electionsController', ['$scope', '$http', function($scope, $http){
        $scope.pageData = this;

        $scope.pageData.elections =[];

        $http.get('/api/command-center').success(function(data){
            $scope.pageData.elections = data['elections'];
        });

        $scope.isElections = $scope.pageData.elections;
        $scope.election_statuses = {'Voting has ended': 'warning', 'Results computed':'success'}
        $scope.date = new Date();


    }]);

    //internApp.controller('addOrgController', function(){
    //    this.newOrg = {};
    //
    //    this.addOrg = function(organization) {
    //
    //    };
    //});

})();

