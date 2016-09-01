var app = angular.module('testApp', ['angular-toArrayFilter']);

//CONTROLLERS:
app.controller('searchCtrl', function($scope, $http){

	$scope.init = function () {
    // function implementation
    	$scope.loaded = false;
    	$http.get('http://127.0.0.1:5000/superJapi/api/v1.0/searchResult')
		.then(function(response){
			$scope.data = response.data;
			$scope.loaded = true;
			
			/*console.log(response.data.length)
			for (var i = 0; i < response.data.length; i ++) {
				console.log(response.data[i]['Tienda']);
			}*/			
		});
};
	
});


// DIRECTIVES:
app.directive('errSrc', function() {
  return {
    link: function(scope, element, attrs) {
      element.bind('error', function() {
        if (attrs.src != attrs.errSrc) {
          attrs.$set('src', attrs.errSrc);
        }
      });
    }
  }
});
