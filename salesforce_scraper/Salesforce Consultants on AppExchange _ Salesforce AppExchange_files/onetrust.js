var SfdcWwwBase=SfdcWwwBase||{},oneTrustComponent=function(){"use strict";var e,t=0;return{init:function(){var n;n=setInterval((function(){null!=(e=document.querySelector("#onetrust-pc-sdk"))&&e&&(function(){var t=!(!e||!e.querySelectorAll(".category-menu-switch-handler"))&&e.querySelectorAll(".category-menu-switch-handler"),n=!(!e||!e.querySelector(".save-preference-btn-handler"))&&e.querySelector(".save-preference-btn-handler"),o=!(!e||!e.querySelector("#accept-recommended-btn-handler"))&&e.querySelector("#accept-recommended-btn-handler"),r=!(!e||!e.querySelector("#ot-tab-desc"))&&e.querySelector("#ot-tab-desc"),c=!(!e||!e.querySelector("#ot-pc-lst"))&&e.querySelector("#ot-pc-lst"),s=!(!c||!c.querySelector("#ot-lst-title"))&&c.querySelector("#ot-lst-title"),a=!(!s||!s.querySelector(".back-btn-handler"))&&s.querySelector(".back-btn-handler"),u=!(!s||!s.getElementsByTagName("span"))&&s.getElementsByTagName("span");function l(e){n&&o&&(void 0===e.parentElement.dataset.optanongroupid?(n.classList.contains("visible")&&n.classList.remove("visible"),o.classList.contains("optanon-ghost-button")&&o.classList.remove("optanon-ghost-button")):(n.classList.add("visible"),o.classList.add("optanon-ghost-button")))}a&&u&&a.appendChild(u[0]);for(let e=0;e<t.length;e++)t[e].addEventListener("click",(function(e){l(e.currentTarget)})),t[e].addEventListener("keydown",(function(e){37!==e.keyCode&&39!==e.keyCode||i()}));if(r&&n&&o&&t.length)for(let e=0;e<t.length;e++)0===e?t[0].addEventListener("keydown",(function(e){!0===e.shiftKey&&9===e.keyCode&&setTimeout((function(){o.focus()}),100),!1===e.shiftKey&&9===e.keyCode&&setTimeout((function(){r.focus()}),100)})):t[e].addEventListener("keydown",(function(e){!0===e.shiftKey&&9===e.keyCode&&setTimeout((function(){o.focus()}),100)}));function i(){for(let e=0;e<t.length;e++)t[e].classList.contains("ot-active-menu")&&l(t[e])}}(),clearInterval(n)),t++>120&&clearInterval(n)}),500)},oneTrustComponent}}();function runOneTrustComponent(){oneTrustComponent.init()}"loading"!=document.readyState?runOneTrustComponent():document.addEventListener?document.addEventListener("DOMContentLoaded",runOneTrustComponent):document.attachEvent("onreadystatechange",(function(){"complete"==document.readyState&&runOneTrustComponent()}));