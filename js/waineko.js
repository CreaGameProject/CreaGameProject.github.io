
window.onload = function () {
    document.body.addEventListener("mousemove", function (e) {
        var mx = e.x;
        var my = e.y;

        var bdy = document.getElementsByClassName('wainekobody')[0];
        var wx = bdy.clientWidth;
        var wy = bdy.clientHeight;
        var rect = bdy.getBoundingClientRect();
        var px = rect.left;
        var py = rect.top;
        var eyes = document.getElementsByClassName('wainekoeye');
        eyes[0].style.width=wx*0.030+'px';
        eyes[0].style.height=wy*0.041+'px';
        eyes[1].style.width=wx*0.028+'px';
        eyes[1].style.height=wy*0.056+'px';

        var x = mx - px - wx * 0.2;
        var y = my - py - wy * 0.32;
        var r = Math.sqrt(x * x + y * y);
        eyes[0].style.left = wx * (0.03 * x / r + 0.2) + 'px';
        eyes[0].style.top = wy * (0.03 * y / r + 0.32) + 'px';

        x = mx - px - wx * 0.36;
        y = my - py - wy * 0.32;
        r = Math.sqrt(x * x + y * y);
        eyes[1].style.left = wx * (0.03 * x / r + 0.36) + 'px';
        eyes[1].style.top = wy * (0.03 * y / r + 0.32) + 'px';
    });
}