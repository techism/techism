var Techism = {};

var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-19569985-1']);
_gaq.push(['_gat._anonymizeIp']);
_gaq.push(['_setDomainName', 'techism.de']);
_gaq.push(['_trackPageview']);
(function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
}) ();

var _paq = _paq || [];
_paq.push(["setDocumentTitle", document.domain + "/" + document.title]);
_paq.push(["trackPageView"]);
_paq.push(["enableLinkTracking"]);
(function() {
    var u="/piwik/";
    _paq.push(["setTrackerUrl", u+"track"]);
    _paq.push(["setSiteId", "13"]);
    var d=document, g=d.createElement("script"), s=d.getElementsByTagName("script")[0]; g.type="text/javascript";
    g.defer=true; g.async=true; g.src=u+"piwik.js"; s.parentNode.insertBefore(g,s);
})();
