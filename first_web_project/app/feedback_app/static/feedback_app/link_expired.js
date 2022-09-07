var $elem = $(".smile"),
  l = $elem.length,
  i = 0;
var $elem2 = $(".uhoh"),
  l = $elem2.length,
  i = 0;

var $elem = $(".smile");
var $elem2 = $(".uhoh");

function comeOn() {
  for (var i = 0; i < 3; i++) {
    if (i % 2) {
      $elem.fadeIn(700);
      // $elem2.fadeOut(700);
    } else {
      $elem.fadeOut(700);
      $elem2.hide().delay(700).fadeIn(700);
    }
  }
}
comeOn();
