function TrailblazerIdentityHeader(urls){
    "use strict";

    this.urls = urls;

    this.isUserLoggedInToSiteOrCommunity = function () {
        var isLoggedInEl = document.getElementById("tbid-is-logged-into-site-or-community");
        return isLoggedInEl.innerText === "true";
    };

    this.bindEvents = function () {
        var autoLoginIframe = document.getElementById("autoLoginTrailblazerIdentityIframe");
        if(autoLoginIframe) {
            autoLoginIframe.addEventListener("load", function () {
                //Check that a different SSO Auth Provider is present.
                if (autoLoginIframe.getAttribute("src") !== null && autoLoginIframe.getAttribute("data-has-refreshed") !== "true") {
                    //Set a data attribute to avoid recursive page loading if src is set for whatever reason.
                    autoLoginIframe.setAttribute("data-has-refreshed", "true");
                    //Refresh the page to avoid running into errors with Javascript remoting when the session changes.
                    window.location.reload(false);
                }
            });
        }
    };

    this.init = function () {
        this.bindEvents();
    };

    this.onInitWithTrailblazerIdentity = function () {
        if(this.isUserLoggedInToSiteOrCommunity() === false) {
            var unauthenticatedSectionEl = document.getElementById('unauthenticated-button-section');
            //In the Collaboration tab there is no unauthenticated mode.
            if (unauthenticatedSectionEl && unauthenticatedSectionEl.classList.contains('slds-hide')) {
                unauthenticatedSectionEl.classList.remove('slds-hide');
                document.getElementById('login-menu-section').classList.add('slds-hide');
            }
            document.getElementById('login-anchor').href = 'javascript:SFIDWidget.login()';
            document.getElementById('signup-anchor').href = 'javascript:SFIDWidget.signup()';
        }else{
            //Workaround for Safari not calling onLogin - still show avatar.
            document.getElementById('login-menu-section').classList.remove('slds-hide');
        }
    };

    this.onLoginWithTrailblazerIdentity = function (identityInfo){
        if(this.isUserLoggedInToSiteOrCommunity() === false){
            document.getElementById('autoLoginTrailblazerIdentityIframe').src = this.urls["loginSsoUrl"];
        }else{
            var unauthenticatedSectionEl = document.getElementById('unauthenticated-button-section');
            //In the Collaboration tab there is no unauthenticated mode.
            if(unauthenticatedSectionEl && !unauthenticatedSectionEl.classList.contains('slds-hide')) {
                unauthenticatedSectionEl.classList.add('slds-hide');
            }
            document.getElementById('login-menu-section').classList.remove('slds-hide');
            document.getElementById('widget-bg').style.backgroundImage = 'url(' + identityInfo.backgroundImageUrl + ')';
        }
    };

    this.onLogoutWithTrailblazerIdentity = function () {
        document.getElementById('autoLoginTrailblazerIdentityIframe').src = this.urls["logoutSsoUrl"];
        SFIDWidget.init();
    };
}

function toggleDropdown(){
    var menuIcon = $('#nav-group-phone').data('data-menuIcon');
    if(window.innerWidth < 768 && isTargetButton(event.target, 'header-user-avatar') && (menuIcon != null)){
        document.getElementById('my-profile').click();
        return;
    }
    var targetMenu = getTargetMenu(event.target);
    if(targetMenu.length > 0){
        if(targetMenu[0].classList.contains('slds-is-open')){
            targetMenu[0].classList.remove('slds-is-open');
            window.removeEventListener('click', closeMenu);
        } else {
            targetMenu[0].classList.add('slds-is-open');
            if(targetMenu[1]) targetMenu[1].classList.remove('slds-is-open');
            event.stopImmediatePropagation();
            window.addEventListener('click', closeMenu);
        }
    }
}

function closeMenu(){
    if(isTargetMenu(event.target)) return;
    var appLauncher = document.getElementById('app-launcher');
    if(appLauncher) appLauncher.classList.remove('slds-is-open');
    var loginMenuSection = document.getElementById('login-menu-section');
    if(loginMenuSection) loginMenuSection.classList.remove('slds-is-open');
    window.removeEventListener('click', closeMenu);
    return;
}

function isTargetMenu(el){
    while (el.parentNode && el.parentNode.tagName != 'BODY') {
        el = el.parentNode;
        if(el.id === 'login-menu-section' || el.id === 'app-launcher') return true;
    }
    return false;
}

function isTargetButton(el, buttonId){
    while (el.parentNode && el.parentNode.tagName != 'BODY') {
        if(el.id === buttonId) return true;
        el = el.parentNode;
    }
    return false;
}

function getTargetMenu(el){
    var menuArray = [];
    var appLauncher = document.getElementById('app-launcher');
    var userAvatarMenu = document.getElementById('login-menu-section');
    if(isTargetButton(el, 'app-launcher-button')){
        menuArray[0] = appLauncher;
        if(userAvatarMenu) menuArray[1] = userAvatarMenu;
    } else if (isTargetButton(el, 'header-user-avatar')){
        menuArray[0] = userAvatarMenu;
        if(appLauncher) menuArray[1] = appLauncher;
    }
    return menuArray;
}