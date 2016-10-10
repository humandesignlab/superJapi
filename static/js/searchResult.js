var app = angular.module('testApp', ['angular-toArrayFilter']);
$('#progressBar').hide();
//CONTROLLERS:
app.controller('searchCtrl', function($scope, $http, $log){


	$scope.init = function(input) {
    // function implementation
    	$scope.loaded = false;
        $('#progressBar').show();
    		if  (!input) {
    			return input;
    		}
        
    		$http({
    			url: 'http://127.0.0.1:5000/superJapi/api/v1.0/searchResult',
    			method: 'POST',
    			data: JSON.stringify({userInput : $scope.input}),
    			headers: {'Content-Type': 'application/json'}

    		}).success(function(response){
    			$scope.data = response;
    			$scope.loaded = true;
    			$log.info(response)
    			//console.log(response);
    		});
        	//console.log($scope.input)
				
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

app.directive('ngEnter', function() {
        return function(scope, element, attrs) {
            element.bind("keydown keypress", function(event) {
                if(event.which === 13) {
                    scope.$apply(function(){
                        scope.$eval(attrs.ngEnter, {'event': event});
                    });

                    event.preventDefault();
                }
            });
        };
    });
