$(function() {
  function randomPercentage() {
    //return Math.floor(Math.random() * 100);
    return 25;
  }
  var num = randomPercentage();
  var controlBar = $('#sample-pb .number-pb').NumberProgressBar({
    duration:10000,
    percentage: num
  });
  var $controls = $('#sample-pb .control');
  $('.water-btn').click(function() {
    animate(100);
    $(".flower_none").animate({opacity:'0'},5000,function(){
       $(".flower_open").animate({opacity:'1'},5000);
    });
  });
  function animate(val) {
    if (val < 0) {
      num = 0;
    } else if (val > 100) {
      num = 100;
    } else {
      num = val
    }
    controlBar.reach(num);
  }
});