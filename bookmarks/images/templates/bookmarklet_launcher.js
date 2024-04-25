// (function () {
//     if (window.myBookmarklet !== undefined) {
//         myBookmarklet();
//     } else {
//         var script = document.createElement('script');
//         script.src = 'https://127.0.0.1:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999);
//         document.body.appendChild(script);
//     }
// })

(function(){
    if (window.myBookmarklet !== undefined){
        myBookmarklet();
    }
    else {
        console.log('aaaaaaaaaaaaa')
        // document.body.appendChild() 方法返回的是被添加的节点，也就是新的 <script> 元素。这个返回的元素就是你可以操作的 DOM 对象，你可以用它来设置属性，添加事件监听器，等等
        document.body.appendChild(document.createElement('script')).src='https://127.0.0.1:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999);
    }
})();