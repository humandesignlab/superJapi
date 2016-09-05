var app = angular.module('testApp', ['angular-toArrayFilter']);

//CONTROLLERS:
app.controller('searchCtrl', function($scope, $http){

	$scope.init = function(input) {
    // function implementation
    	$scope.loaded = false;
    		if  (!input) {
    			return input;
    		}

    		$http({
    			url: 'http://127.0.0.1:5000/superJapi/api/v1.0/searchResult',
    			method: 'POST',
    			param: {userInput: $scope.input}

    		}).success(function(response){
    			$scope.data = response.data;
    			$scope.loaded = true;
    			console.log(response);
    		});

	    	/*$http.get('http://127.0.0.1:5000/superJapi/api/v1.0/searchResult')
			.then(function(response){
				$scope.data = response.data;
				$scope.loaded = true;*/
				
				/*console.log(response.data.length)
				for (var i = 0; i < response.data.length; i ++) {
					console.log(response.data[i]['Tienda']);
				}		
		});*/	
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
