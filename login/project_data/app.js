var app = angular.module('plunker', []);

app.controller('MainCtrl', function($scope) {
   $scope.items = [ ];
    
    $scope.addToCart = function(item)
    {
      $scope.items.push(item);
    }

     $scope.removeToCart = function(item)
    {
      $scope.items.pop(item);
    }
});
