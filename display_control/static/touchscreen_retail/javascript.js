/* Copyright 2010 Google Inc.
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *    http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/*
 * @fileoverview Handles AJAX requests and display restrictions for the 
 * Liquid Galaxy touchscreen that is run via a webserver.
 */

// To prevent users from causing right menu windows showing up
// we disable the ability to right click using the example
// code provided by Reconn.us at the following URL
//  http://www.reconn.us/content/view/36/45/
var isNS = (navigator.appName == 'Netscape') ? 1 : 0;
if (navigator.appName == 'Netscape') {
  document.captureEvents(Event.MOUSEDOWN || Event.MOUSEUP);
}

function mischandler() {
  return false;
}

function mousehandler(e) {
  var myevent = (isNS) ? e : event;
  var eventbutton = (isNS) ? myevent.which : myevent.button;
  if ((eventbutton == 2) || (eventbutton == 3)) return false;
}

document.oncontextmenu = mischandler;
document.onmousedown = mousehandler;
document.onmouseup = mousehandler;

// To prevent users from causing images to start moving
// around as they're trying to interact with the touchscreen
// we disable image dragging using the example code provided
// by Redips at the following URL
// http://www.redips.net/firefox/disable-image-dragging/
window.onload = function (e) {
  var evt = e || window.event;
  var imgs;
  if (evt.preventDefault) {
    imgs = document.getElementsByTagName('img');
    for (var i = 0; i < imgs.length; i++) {
      imgs[i].onmousedown = disableDragging;
    }
  }
}

function disableDragging(e) {
  e.preventDefault();
}

function createRequest() {
  if (window.XMLHttpRequest) {
    var req = new XMLHttpRequest();
    return req;
  }
}

function quietRequest(url) {
  var req = createRequest();
  req.open('GET', url, true);
  req.send(null);
}

function submitRequest(url) {
  var req = createRequest();
  req.onreadystatechange = function() {
    if (req.readyState == 4) {
      if (req.status == 200) {
        document.getElementById('status').innerHTML = req.responseText;
      }
    }
  }
  req.open('GET', url, true);
  req.send(null);
}

function xchangePlanet(planet) {
    return;
}

function changePlanet(planet) {
  submitRequest('http://localhost:81/change.php?planet=' + planet);
  showAndHideStatus();
}

function changeQuery(query, name) {
  submitRequest('http://localhost:81/change.php?query=' + query + '&name=' + name);
  showAndHideStatus();
}

function quietQuery(query, name) {
  quietRequest('http://localhost:81/change.php?query=' + query + '&name=' + name);
}

function changeLayer(layer, name) {
  submitRequest('http://localhost:81/change.php?layer=' + layer + '&name=' + name);
  showAndHideStatus();
}

function syncKml(action, url) {
  submitRequest('http://localhost:81/sync_touchscreen.php?touch_action=' + action + '&touch_kml=' + url);
  showAndHideStatus();
}

function toggleKml(obj, url) {
  if (obj.className == 'kml_off') {
    submitRequest('http://localhost:81/sync_touchscreen.php?touch_action=add&touch_kml=' + url);
    obj.className='kml_on';
  }
  else if (obj.className == 'kml_on') {
    
    submitRequest('http://localhost:81/sync_touchscreen.php?touch_action=delete&touch_kml=' + url);
    obj.className='kml_off';
  }
  showAndHideStatus();
}

function showAndHideStatus() {
  var status = document.getElementById('status');
  status.style.opacity = 1;
  window.setTimeout('document.getElementById("status").style.opacity = 0;', 2000);
}

function searchKey() {
  var keyboardEntry = document.getElementById('keyboardEntry');

  if (keyboardEntry.value) {
    var val = encodeURIComponent(keyboardEntry.value);

    changeQuery('search=' + val, val);
  }
}

function toggleExpand(on_obj){
  noneExpand();
  document.getElementById(on_obj).className='expand_active';
}
function noneExpand(){
  clearSearch();
  $("[id^=e_]").each(function(i, val) {
    val.className='expand_inactive';
  });
}

function resumeEarth() {
  quietQuery('resume-earth', 'Google Earth');
}
function switchToPeruse() {
  quietQuery('launch-peruse', 'Google Street View');
  window.location.href = 'http://lg-head:8086/touchscreen/';
}

$(function() {
  jsKeyboard.init('virtual-keyboard');
  var field = $('#keyboardEntry');
  field.focus();
  jsKeyboard.currentElement = field;
  jsKeyboard.currentElementCursorPosition = 0;

  $(".key_enter").live("click", function(e){
    searchKey();
  });
});

function clearSearch() {
  $('#keyboardEntry').val("");
}
