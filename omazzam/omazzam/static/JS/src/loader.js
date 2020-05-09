// Code goes here

angular.module('omazzam', [])
  .directive('loading', function () {
      return {
        restrict: 'E',
        replace:true,
        template: '<div id="loaderDiv"><img class="ajax-loader" src="http://www.nasa.gov/multimedia/videogallery/ajax-loader.gif" /></div>',
        link: function (scope, element, attr) {
              scope.$watch('loading', function (val) {
                  if (val)
                      $(element).show();
                  else
                      $(element).hide();
              });
        }
      }
  })
  .controller('omazzamController', function($scope, $http) {


      $scope.clickMe = function() {
        $scope.loading = true;
        $http.success(function(data) {

            $scope.loading = false;
        });
      }

  });
