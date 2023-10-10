window.addEventListener('DOMContentLoaded', init, false);
var originalBackground;
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
