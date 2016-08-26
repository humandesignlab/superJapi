var app = angular.module('testApp', ['angular-toArrayFilter']);

app.controller('searchCtrl', function($scope, $http){

	$http.get('http://127.0.0.1:5000/superJapi/api/v1.0/searchResult')
		.then(function(response){
			$scope.data = response.data;
			
			console.log(response.data.length)
			for (var i = 0; i < response.data.length; i ++) {
				console.log(response.data[i]['Tienda']);
			}
			
		});

});
