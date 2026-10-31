// Loads the YouTube player only when the visitor presses play (keeps the page light and cookie-free until then).
document.querySelectorAll('.trailer[data-yt]').forEach(function (box) {
  box.querySelector('.play').addEventListener('click', function () {
    var f = document.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(box.dataset.yt) + '?autoplay=1&rel=0';
    f.title = 'Trailer';
    f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    f.allowFullscreen = true;
    box.replaceChildren(f);
  });
});
