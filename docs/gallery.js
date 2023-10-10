window.addEventListener('DOMContentLoaded', init, false);
/*  var originalBackground;
function toggleHighlight() {
    var pos = this.getAttribute('value');
    var color;
    switch (pos) {
        case 'pp':
        color = 'yellow';
        break;
        case 'coll':
        color = 'orange';
        break;
        case 'assign':
        color = 'teal';
        break;
        
    }
    var status = this.checked;
    var spans = document.getElementsByClassName(pos);
    for (var i = 0; i < spans.length; i++) {
        if (status == true) {
            spans[i].style.backgroundColor = color;
        } else {
            spans[i].style.backgroundColor = originalBackground;
        }
    }
}
function init() {
    originalBackground = document.body.style.backgroundColor;
    var checkboxes = document.getElementsByTagName('input');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].addEventListener('click', toggleHighlight, false);
    }
}
function init() {
    var fieldset = document.getElementsByTagName('input');
    for (var i = 0; i < fieldset.length; i++) {
        fieldset[i].addEventListener('click', toggle, false);
    }
}
*/
function init() {
    var fieldset = document.getElementsByTagName('input');
    for (var i = 0; i < fieldset.length; i++) {
        fieldset[i].addEventListener('click', toggle, false);
    }
}
function toggle() {
    var id = this.id;
    switch (id) {
        case "pp": {
            var pp = document.getElementsByClassName("pp");
            for (var i = 0; i < pp.length; i++) {
                pp[i].classList.toggle("on")
            }
        };
        break;
        case "coll": {
            var coll = document.getElementsByClassName("coll");
            for (var i = 0; i < coll.length; i++) {
                coll[i].classList.toggle("on")
            }
        };
        break;
        case "assign": {
            var assign = document.getElementsByClassName("assign");
            for (var i = 0; i < assign.length; i++) {
                assign[i].classList.toggle("on")
            }
        };
        break;
    }
  }