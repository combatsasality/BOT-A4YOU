document.querySelector(".v-test-result-new-head").remove(); 
for (let i of document.querySelectorAll(".v-test-count")) { i.remove(); } 
for (let i of document.getElementsByTagName("img")) { i.src = Object.assign({}, i.dataset).src; } 
for (let i of document.getElementsByTagName("image")) {i.href.animVal = Object.assign({}, i.dataset).src; i.href.baseVal = Object.assign({}, i.dataset).src;}
for (let i of document.getElementsByTagName("ellipse")) {if (i.attributes.fill.textContent == "red") {i.remove();} else if(i.attributes.fill.textContent == "green") {i.remove();}}
for (let i of document.querySelectorAll("div.v-correct-answer")) { i.remove(); } 
for (let i of document.querySelectorAll(".v-test-questions-radio-block")) { i.remove(); } 
for (let i of document.querySelectorAll(".v-test-questions-checkbox-block")) { i.remove(); } 
for (let i of document.querySelectorAll(".v-col-12.v-col-last")) { i.remove(); }
for (let i of document.getElementsByTagName("li")) {if (i.outerHTML.match("<p>") == null) {i.innerText = i.innerText.replace(/;/g, "\nили\n");}}
for (let i of document.querySelectorAll(".rk-selected__pair")) {i.innerText = i.innerText.replace(/\n/g, " - ");}
for (let i of document.querySelectorAll(".vr-control > strong")) {if (i.innerHTML.match(/color: red;/) == null) {if (i.innerHTML.match('<span style=\\"color:green;\\">(.+)</span>') != null) {i.innerHTML = i.innerHTML.match('<span style=\\"color:green;\\">(.+)</span>')[0]+" ";}} else {i.remove();}}
for (let i of document.querySelectorAll(".v-block-answers-cross-block")) {i.children[0].innerHTML = i.children[0].innerText; i.children[0].innerHTML = i.children[0].innerHTML+i.children[1].innerHTML;i.children[1].remove();i.children[0].innerHTML = i.children[0].innerHTML.replace(/\n/g, " ");var check = i.children[0].innerHTML.match("<p>(.+)</p>");if (check != null){i.children[0].innerHTML = i.children[0].innerHTML.replace(check[0], " - "+check[1]+"<br><br>");}}